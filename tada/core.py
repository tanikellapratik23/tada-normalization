"""Shared lossless mapping primitives; no provider semantics live here."""

from copy import deepcopy
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from urllib.parse import quote
import hashlib
import json

MISSING = object()


def dumps(value, **kwargs):
    def encode(item):
        if isinstance(item, Decimal):
            return str(item)
        raise TypeError("Unsupported JSON value type: " + type(item).__name__)

    return json.dumps(value, default=encode, **kwargs)


def loads(value):
    return json.loads(
        value,
        parse_float=Decimal,
        parse_constant=lambda x: (_ for _ in ()).throw(
            ValueError("Nonfinite JSON number")
        ),
    )


def identity(provider, tenant, company, kind, source_id):
    parts = [provider, tenant, company, kind, source_id]
    if any(x is None or str(x) == "" for x in parts):
        raise ValueError(
            "Identity requires provider, tenant, company, entity and source identifier"
        )
    return ":".join(quote(str(x), safe="") for x in parts)


def get(obj, path):
    for part in path.split("."):
        if not isinstance(obj, dict) or part not in obj:
            return MISSING
        obj = obj[part]
    return obj


def leaves(value, prefix=""):
    if isinstance(value, dict) and value:
        for key, child in value.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            yield from leaves(child, prefix + "/" + escaped)
    elif isinstance(value, list) and value:
        for index, child in enumerate(value):
            yield from leaves(child, prefix + "/" + str(index))
    else:
        yield prefix, value


def decimal(value):
    if isinstance(value, bool):
        raise ValueError("Boolean is not a number")
    try:
        number = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("Invalid decimal") from exc
    if not number.is_finite():
        raise ValueError("Number must be finite")
    return format(number, "f")


def iso_date(value):
    # Preserve time/offset: converting a timestamp to a date loses information.
    if not isinstance(value, str):
        raise ValueError("Expected ISO date or timestamp")
    if "T" in value:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    else:
        date.fromisoformat(value)
    return value


class Mapper:
    def __init__(self, provider, kind, raw, context, source_id):
        self.raw = deepcopy(raw)
        self.provider = provider
        self.context = context
        self.used = {}
        self.out = {
            "schema_version": "1.0",
            "entity": kind,
            "id": identity(
                provider, context["tenant_id"], context["company_id"], kind, source_id
            ),
            "company_id": identity(
                provider,
                context["tenant_id"],
                context["company_id"],
                "company",
                context["company_id"],
            ),
            "source": {
                "provider": provider,
                "tenant_id": str(context["tenant_id"]),
                "company_id": str(context["company_id"]),
                "record_id": str(source_id),
            },
            "data": {},
            "diagnostics": [],
        }
        employee_id = context.get("employee_id")
        if employee_id is not None:
            self.out["employee_id"] = identity(
                provider,
                context["tenant_id"],
                context["company_id"],
                "employee",
                employee_id,
            )

    def warn(self, code, path, message):
        self.out["diagnostics"].append({"code": code, "path": path, "message": message})

    def set(self, target, value):
        dest = self.out["data"]
        parts = target.split(".")
        for part in parts[:-1]:
            dest = dest.setdefault(part, {})
        dest[parts[-1]] = value

    def field(self, source, target, transform=None):
        value = get(self.raw, source)
        if value is MISSING:
            return
        pointer = "/" + source.replace(".", "/")
        if value is not None and transform:
            try:
                value = transform(value)
            except (ValueError, TypeError, InvalidOperation, OverflowError):
                self.warn(
                    "invalid_value",
                    pointer,
                    "Cannot convert source value; retained in extensions",
                )
                return
        self.set(target, deepcopy(value))
        self.used[pointer] = (
            "/data/"
            + target.replace(".", "/")
            + (
                "/source_value"
                if isinstance(value, dict) and "source_value" in value and transform
                else ""
            )
        )

    def enum(self, source, target, mapping):
        value = get(self.raw, source)
        if value is MISSING:
            return
        canonical = mapping.get(str(value), "unknown") if value is not None else None
        if target in ("employment.status", "status") and canonical not in (
            None,
            "active",
            "inactive",
            "pending",
            "on_leave",
            "terminated",
            "cancelling",
            "prenote",
            "unknown",
        ):
            raise ValueError("Invalid canonical status in supplied lookup map")
        if canonical == "unknown":
            self.warn(
                "unknown_enum",
                "/" + source.replace(".", "/"),
                "No verified canonical meaning for this source code",
            )
        self.field(source, target, lambda v: {"value": canonical, "source_value": v})

    def finish(self):
        extensions, coverage = {}, {}
        for pointer, value in leaves(self.raw):
            match = next(
                (p for p in self.used if pointer == p or pointer.startswith(p + "/")),
                None,
            )
            if match:
                coverage[pointer] = self.used[match] + pointer[len(match) :]
            else:
                extensions[pointer] = value
                coverage[pointer] = "extensions"
        self.out["extensions"] = extensions
        self.out["field_coverage"] = coverage
        # Source snapshot supports audit/reprocessing, extensions are explicitly NOT semantically normalized.
        self.out["source_record"] = self.raw
        return self.out


def record_id(raw, context, key="id"):
    value = get(raw, key)
    if value is not MISSING and value is not None and str(value) != "":
        return value
    value = context.get("record_id")
    if value is not None and str(value) != "":
        return value
    raise ValueError(
        "Missing source record ID; supply context.record_id when endpoint has no ID"
    )


def digest(value):
    return hashlib.sha256(
        dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

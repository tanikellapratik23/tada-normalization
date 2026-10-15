"""Pinned evidence and fixture schema validation (optional jsonschema dependency)."""

from functools import lru_cache
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ISOL = "AOS.PayrollOffice.RestAPI.Models."
SCHEMAS = {
    "prismhr": {
        "company": "ClientMaster",
        "employee": "Employee",
        "direct_deposit": "AchVoucher",
        "deduction": "EmployeeDeductions-Deduction",
        "payroll_run": "PayrollHistory",
        "paycheck": "PayrollVoucher",
    },
    "isolved": {
        "company": "LegalModel",
        "employee": "EmployeeModel",
        "direct_deposit": "EmployeeDirectDepositModel",
        "deduction": "EmployeePayItemModel",
        "payroll_run": "PayrollRunHistoryModel",
        "paycheck": "CheckModel",
    },
    "ukg-ready": {
        "employee": 106,
        "direct_deposit": 137,
        "deduction": 133,
        "payroll_run": 358,
        "paycheck": 364,
        "compensation": 33,
        "pay_info": 159,
        "demographics": 134,
    },
}
FILES = {
    "prismhr": "prismhr/openapi/prismhr-2025.09.openapi.json",
    "isolved": "isolved/openapi/isolved-v6.swagger.json",
    "ukg-ready": "ukg-ready/reference-schemas.json",
}


@lru_cache(maxsize=3)
def document(provider):
    return json.loads((ROOT / "contracts" / FILES[provider]).read_text())


def schema_for(provider, entity):
    doc = document(provider)
    name = SCHEMAS[provider].get(entity)
    if name is None:
        return {"type": "object"}, {}, "caller context (not provider contract)"
    if provider == "ukg-ready":
        entry = doc["schemas"][name]
        root = entry["schema"]
        schema = root
        if entity in ("direct_deposit", "payroll_run"):
            schema = root["properties"][
                "deposits" if entity == "direct_deposit" else "payrolls"
            ]["items"]
        return (
            schema,
            root,
            f"contracts/{FILES[provider]}#/schemas/{name}/schema ({entry['source_page']}#{entry['source_schema_anchor']})",
        )
    name = ISOL + name if provider == "isolved" else name
    key = "definitions" if provider == "isolved" else "components"
    schema = doc[key][name] if key == "definitions" else doc[key]["schemas"][name]
    pointer = (
        f"#/definitions/{name}"
        if key == "definitions"
        else f"#/components/schemas/{name}"
    )
    return schema, doc, "contracts/" + FILES[provider] + pointer


def resolve(schema, root):
    if "$ref" not in schema:
        return schema
    ref = schema["$ref"]
    if not ref.startswith("#/"):
        raise ValueError("Only bundled local schema references are supported")
    value = root
    for part in ref[2:].split("/"):
        value = value[part.replace("~1", "/").replace("~0", "~")]
    return value


def source_errors(provider, entity, record):
    from jsonschema import Draft4Validator, FormatChecker

    schema, root, _ = schema_for(provider, entity)
    # Keep local reference namespaces with the selected object schema. This avoids
    # network resolution and the deprecated RefResolver API without modifying evidence.
    validation_schema = dict(schema)
    for namespace in ("definitions", "components"):
        if namespace in root:
            validation_schema[namespace] = root[namespace]
    validator = Draft4Validator(validation_schema, format_checker=FormatChecker())
    # Message values can contain PII: return paths and validator names only.
    return [
        {"path": "/" + "/".join(map(str, e.absolute_path)), "rule": e.validator}
        for e in validator.iter_errors(record)
    ]

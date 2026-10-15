"""Generate auditable field inventory from the pinned employee contracts."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tada.contracts import schema_for, resolve
from tada.adapters import EMPLOYEE


def walk(schema, root, path="", seen=()):
    ref = schema.get("$ref")
    if ref and ref in seen:
        yield path, "recursive object"
        return
    seen = seen + (ref,) if ref else seen
    schema = resolve(schema, root)
    if "properties" in schema:
        for name, child in schema["properties"].items():
            yield from walk(child, root, path + "." + name if path else name, seen)
    elif schema.get("type") == "array":
        yield from walk(schema.get("items", {}), root, path + "[]", seen)
    else:
        yield path, schema.get("type", "unspecified")


rows = [
    "# Employee field inventory",
    "",
    "This report distinguishes common semantic mappings from lossless provider extensions. Extensions are not claimed as normalized equivalents. Every received field is also preserved in `source_record`. Array element schemas are listed even when synthetic arrays are empty. Regenerate with `python scripts/build_mapping_report.py`.",
    "",
]
for provider, bindings in EMPLOYEE.items():
    schema, root, evidence = schema_for(provider, "employee")
    rows.extend(
        [
            "## " + provider,
            "",
            f"Source: `{evidence}`",
            "",
            "| Source path | Destination / treatment |",
            "| --- | --- |",
        ]
    )
    mappings = {v: k for k, v in bindings.items()}
    if provider == "prismhr":
        mappings.update(
            {
                "client.statusClass": "employment.status",
                "compensation.payMethod": "compensation.basis",
            }
        )
    else:
        mappings["employmentStatus" if provider == "isolved" else "status"] = (
            "employment.status (tenant lookup)"
        )
    for path, _ in walk(schema, root):
        match = next(
            (
                p
                for p in mappings
                if path == p or path.startswith(p + ".") or path.startswith(p + "[]")
            ),
            None,
        )
        target = (
            "data." + mappings[match] + path[len(match) :]
            if match
            else "extensions (provider-specific, unchanged)"
        )
        if path == "id":
            target = "data.source_id + scoped identity"
        rows.append(f"| `{path}` | `{target}` |")
    rows.append("")
Path("docs/EMPLOYEE_FIELD_COVERAGE.md").write_text("\n".join(rows) + "\n")

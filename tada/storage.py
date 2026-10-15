"""Transactional, idempotent storage with deferred foreign-key checks."""

import sqlite3
from pathlib import Path
from .core import dumps, loads

DDL = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS records (
 id TEXT PRIMARY KEY, provider TEXT NOT NULL, entity TEXT NOT NULL,
 company_id TEXT NOT NULL REFERENCES records(id) DEFERRABLE INITIALLY DEFERRED,
 employee_id TEXT REFERENCES records(id) DEFERRABLE INITIALLY DEFERRED,
 payroll_run_id TEXT REFERENCES records(id) DEFERRABLE INITIALLY DEFERRED,
 document TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS records_filter ON records(provider,entity,company_id);
CREATE TABLE IF NOT EXISTS imports (
 id INTEGER PRIMARY KEY, imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 record_count INTEGER NOT NULL, warning_count INTEGER NOT NULL
);
"""


def connect(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.executescript(DDL)
    return db


def ingest(db, records):
    seen = set()
    for record in records:
        if record["id"] in seen:
            raise ValueError("Duplicate record ID in import batch")
        seen.add(record["id"])
    with db:
        for r in records:
            db.execute(
                """INSERT INTO records VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET provider=excluded.provider,entity=excluded.entity,
            company_id=excluded.company_id,employee_id=excluded.employee_id,
            payroll_run_id=excluded.payroll_run_id,document=excluded.document""",
                (
                    r["id"],
                    r["source"]["provider"],
                    r["entity"],
                    r["company_id"],
                    r.get("employee_id"),
                    r.get("payroll_run_id"),
                    dumps(r, sort_keys=True),
                ),
            )
        for col, kind in [
            ("company_id", "company"),
            ("employee_id", "employee"),
            ("payroll_run_id", "payroll_run"),
        ]:
            bad = db.execute(
                f"""SELECT 1 FROM records a JOIN records b ON a.{col}=b.id
              WHERE b.entity!=? OR a.provider!=b.provider OR a.company_id!=b.company_id LIMIT 1""",
                (kind,),
            ).fetchone()
            if bad:
                raise ValueError("Relationship has wrong entity type or company scope")
        db.execute(
            "INSERT INTO imports(record_count,warning_count) VALUES (?,?)",
            (len(records), sum(len(r["diagnostics"]) for r in records)),
        )
    return len(records)


def query(db, provider=None, entity=None, company_id=None, limit=100, offset=0):
    if not 1 <= limit <= 1000 or offset < 0:
        raise ValueError("limit must be 1..1000; offset must be nonnegative")
    where = []
    params = []
    for name, value in [
        ("provider", provider),
        ("entity", entity),
        ("company_id", company_id),
    ]:
        if value is not None:
            where.append(name + "=?")
            params.append(value)
    sql = (
        "SELECT document FROM records"
        + (" WHERE " + " AND ".join(where) if where else "")
        + " ORDER BY id LIMIT ? OFFSET ?"
    )
    return [loads(row[0]) for row in db.execute(sql, params + [limit, offset])]

import copy
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from tada.adapters import normalize, EMPLOYEE
from tada.core import decimal, identity, leaves, loads
from tada.fixtures import generate
from tada.contracts import source_errors, schema_for, resolve
from tada.storage import connect, ingest, query
from tada.__main__ import transform

CTX = {"tenant_id": "test", "company_id": "1", "employee_id": "101", "record_id": "201"}


class NormalizationTests(unittest.TestCase):
    def test_source_contract_validation(self):
        for f in generate():
            with self.subTest(provider=f["provider"], entity=f["entity"]):
                self.assertEqual(
                    [], source_errors(f["provider"], f["entity"], f["record"])
                )

    def test_deterministic_generation(self):
        self.assertEqual(generate(42), generate(42))
        self.assertNotEqual(generate(42), generate(43))
        checked = json.loads(Path("fixtures/synthetic.json").read_text())
        self.assertEqual(checked, generate(42))

    def test_all_source_leaves_accounted_for(self):
        for f in generate():
            original = copy.deepcopy(f["record"])
            n = normalize(f["provider"], f["entity"], f["record"], f["context"])
            self.assertEqual(original, f["record"])
            self.assertEqual(original, n["source_record"])
            self.assertEqual(set(dict(leaves(original))), set(n["field_coverage"]))
            for path, value in n["extensions"].items():
                self.assertEqual(dict(leaves(original))[path], value)

    def test_employee_mapping_paths_exist_in_contracts(self):
        for provider, bindings in EMPLOYEE.items():
            root_schema, root, _ = schema_for(provider, "employee")
            for path in bindings.values():
                schema = root_schema
                for key in path.split("."):
                    schema = resolve(schema, root)
                    self.assertIn(key, schema.get("properties", {}), (provider, path))
                    schema = schema["properties"][key]

    def test_decimal_precision(self):
        data = loads('{"amount":1234567890.123456789}')
        self.assertEqual(decimal(data["amount"]), "1234567890.123456789")
        for invalid in ("NaN", "Infinity", "-Infinity", True, "oops"):
            with self.assertRaises(ValueError):
                decimal(invalid)

    def test_missing_null_zero_and_false_remain_distinct(self):
        r = normalize(
            "isolved",
            "employee",
            {"id": 101, "hourlyRate": 0, "isRemoteWorker": False, "emailAddress": None},
            CTX,
        )
        self.assertEqual(r["data"]["compensation"]["hourly_rate"], "0")
        self.assertIs(r["data"]["employment"]["remote_worker"], False)
        self.assertIsNone(r["data"]["contact"]["email"])
        self.assertNotIn("profile", r["data"])

    def test_unknown_enum_retained(self):
        r = normalize(
            "prismhr",
            "employee",
            {"id": "101", "client": {"statusClass": "NEW_TENANT_CODE"}},
            CTX,
        )
        self.assertEqual(
            r["data"]["employment"]["status"],
            {"value": "unknown", "source_value": "NEW_TENANT_CODE"},
        )
        self.assertIn("unknown_enum", [d["code"] for d in r["diagnostics"]])

    def test_status_domains_not_confused(self):
        r = normalize(
            "prismhr", "employee", {"id": "101", "client": {"employeeStatus": "A"}}, CTX
        )
        self.assertNotIn("status", r["data"]["employment"])

    def test_tenant_status_dictionary(self):
        r = normalize(
            "isolved",
            "employee",
            {"id": 101, "employmentStatus": "Working"},
            dict(CTX, employment_status_map={"Working": "active"}),
        )
        self.assertEqual(r["data"]["employment"]["status"]["value"], "active")

    def test_names_not_swapped_due_to_doc_typo(self):
        r = normalize(
            "prismhr",
            "employee",
            {"id": "101", "firstName": "Avery", "lastName": "Example"},
            CTX,
        )
        self.assertEqual(r["data"]["profile"]["first_name"], "Avery")

    def test_invalid_date_retained_with_diagnostic(self):
        r = normalize("isolved", "employee", {"id": 101, "hireDate": "2026-02-30"}, CTX)
        self.assertEqual(r["extensions"]["/hireDate"], "2026-02-30")
        self.assertEqual(r["diagnostics"][0]["code"], "invalid_value")

    def test_timestamp_keeps_offset(self):
        value = "2026-01-01T23:30:00-05:00"
        r = normalize("isolved", "employee", {"id": 101, "hireDate": value}, CTX)
        self.assertEqual(r["data"]["employment"]["hire_date"], value)

    def test_identity_namespaces_and_escaping(self):
        self.assertNotEqual(
            identity("p", "t", "c:1", "employee", "2"),
            identity("p", "t:c", "1", "employee", "2"),
        )
        self.assertNotEqual(
            identity("p", "t1", "c", "employee", "2"),
            identity("p", "t2", "c", "employee", "2"),
        )
        with self.assertRaises(ValueError):
            identity("p", "", "c", "employee", "2")

    def test_missing_id_rejected(self):
        with self.assertRaises(ValueError):
            normalize("prismhr", "employee", {}, {"tenant_id": "t", "company_id": "1"})

    def test_prism_deposit_methods_distinct(self):
        methods = {
            "F": "fixed",
            "FS": "fixed_skip_if_insufficient",
            "P": "percentage",
            "PN": "percentage_of_remainder",
            "B": "remainder",
        }
        for code, expected in methods.items():
            raw = {"method": code, "accountNum": "000001", "accountType": "C"}
            if code != "B":
                raw["amount"] = 25
            r = normalize("prismhr", "direct_deposit", raw, CTX)
            self.assertEqual(r["data"]["allocation"]["method"]["value"], expected)
            self.assertEqual(r["data"]["account"]["number"], "000001")
            self.assertNotIn("priority", r["data"])

    def test_balance_cannot_have_amount(self):
        r = normalize("prismhr", "direct_deposit", {"method": "B", "amount": 10}, CTX)
        self.assertIn("conflicting_allocation", [d["code"] for d in r["diagnostics"]])

    def test_isolved_net_pay_sequence_zero(self):
        r = normalize("isolved", "direct_deposit", {"id": 1, "sequenceNumber": 0}, CTX)
        self.assertEqual(r["data"]["allocation"]["method"]["value"], "remainder")
        self.assertEqual(r["data"]["priority"], 0)

    def test_isolved_conflicting_allocation(self):
        r = normalize(
            "isolved", "direct_deposit", {"id": 1, "amount": 10, "percent": 20}, CTX
        )
        self.assertIn("conflicting_allocation", [d["code"] for d in r["diagnostics"]])

    def test_out_of_range_percentage(self):
        r = normalize("isolved", "direct_deposit", {"id": 1, "percent": 101}, CTX)
        self.assertIn("percentage_out_of_range", [d["code"] for d in r["diagnostics"]])

    def test_ukg_reserve_check_not_bank_deposit(self):
        r = normalize(
            "ukg-ready",
            "direct_deposit",
            {
                "id": 1,
                "type": "RESERVE_LIVE_CHECK",
                "active": False,
                "calc_method": {"type": "FULL"},
            },
            CTX,
        )
        self.assertEqual(r["data"]["payment_type"]["value"], "reserve_live_check")
        self.assertEqual(r["data"]["status"]["value"], "inactive")

    def test_ukg_known_millisecond_conversion(self):
        r = normalize("ukg-ready", "pay_info", {"standard_work_day": 28800000}, CTX)
        self.assertEqual(r["data"]["compensation"]["standard_day_hours"], "8")

    def test_paycheck_hours_not_guessed(self):
        r = normalize(
            "ukg-ready",
            "paycheck",
            {
                "id": 1,
                "employee": {"account_id": 101},
                "earnings": [{"hours": 3600000, "ee_amount": 100}],
            },
            CTX,
        )
        self.assertEqual(r["data"]["earnings"][0]["source_hours"], 3600000)
        self.assertNotIn("gross_pay", r["data"])
        self.assertNotIn("net_pay", r["data"])

    def test_current_and_ytd_not_double_counted(self):
        r = normalize(
            "isolved",
            "paycheck",
            {
                "id": 1,
                "employeeId": 101,
                "earnings": [
                    {
                        "checkDollars": 100,
                        "currentDollars": 200,
                        "ytdDollars": 1200,
                        "checkHours": 4,
                    }
                ],
            },
            CTX,
        )
        self.assertEqual(r["data"]["earnings"][0]["amount"], "100")
        self.assertEqual(r["data"]["earnings"][0]["source_record"]["ytdDollars"], 1200)

    def test_negative_adjustments_preserved(self):
        r = normalize(
            "isolved",
            "paycheck",
            {"id": 1, "employeeId": 101, "grossPay": -100, "netPay": -80},
            CTX,
        )
        self.assertEqual(r["data"]["gross_pay"], "-100")

    def test_payroll_run_number_is_not_run_id(self):
        r = normalize(
            "isolved",
            "paycheck",
            {"id": 1, "employeeId": 101, "payrollRunNumber": 1},
            CTX,
        )
        self.assertNotIn("payroll_run_id", r)
        self.assertIn("missing_run_link", [d["code"] for d in r["diagnostics"]])

    def test_conflicting_employee_context_rejected(self):
        with self.assertRaises(ValueError):
            normalize("isolved", "paycheck", {"id": 1, "employeeId": 999}, CTX)

    def test_strict_mode_rejects_warnings(self):
        with self.assertRaises(ValueError):
            transform(generate(), strict=True)

    def test_unknown_fields_and_pointer_escaping(self):
        r = normalize(
            "isolved",
            "employee",
            {"id": 101, "future/key": {"~x": [0, None, False]}},
            CTX,
        )
        self.assertEqual(r["extensions"]["/future~1key/~0x/2"], False)

    def test_stored_relations_idempotency_and_filter(self):
        with tempfile.TemporaryDirectory() as directory:
            db = connect(Path(directory) / "test.sqlite")
            try:
                records = transform(generate())
                ingest(db, records)
                ingest(db, records)
                self.assertEqual(
                    db.execute("SELECT count(*) FROM records").fetchone()[0], 21
                )
                self.assertEqual(
                    len(query(db, provider="prismhr", entity="employee")), 1
                )
                self.assertEqual(len(query(db, limit=2, offset=2)), 2)
                self.assertEqual(query(db, provider="' OR 1=1 --"), [])
            finally:
                db.close()

    def test_transaction_rollback_for_orphan(self):
        with tempfile.TemporaryDirectory() as directory:
            db = connect(Path(directory) / "test.sqlite")
            try:
                orphan = normalize("isolved", "employee", {"id": 101}, CTX)
                with self.assertRaises(sqlite3.IntegrityError):
                    ingest(db, [orphan])
                self.assertEqual(
                    db.execute("SELECT count(*) FROM records").fetchone()[0], 0
                )
                self.assertEqual(
                    db.execute("SELECT count(*) FROM imports").fetchone()[0], 0
                )
            finally:
                db.close()

    def test_duplicate_batch_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            db = connect(Path(directory) / "test.sqlite")
            try:
                records = transform(generate())
                with self.assertRaises(ValueError):
                    ingest(db, records + records)
                self.assertEqual(
                    db.execute("SELECT count(*) FROM records").fetchone()[0], 0
                )
            finally:
                db.close()


if __name__ == "__main__":
    unittest.main()

import json
import unittest
from unittest.mock import patch
from tada.adapters import normalize
from tada.core import leaves
from tada.live_check import Check, NoRedirect

CTX = {
    "tenant_id": "t",
    "company_id": "1",
    "employee_id": "101",
    "record_id": "same-slot",
}


class AuditRegressions(unittest.TestCase):
    def test_employee_scoped_records_never_collide(self):
        for entity in (
            "direct_deposit",
            "deduction",
            "compensation",
            "pay_info",
            "demographics",
        ):
            provider = "ukg-ready"
            a = normalize(provider, entity, {"id": 1}, CTX)
            b = normalize(provider, entity, {"id": 1}, dict(CTX, employee_id="102"))
            self.assertNotEqual(a["id"], b["id"], entity)
            self.assertEqual(a["source"]["record_id"], b["source"]["record_id"])

    def test_prism_deduction_code_is_scoped_to_employee(self):
        raw = {"deductionCode": "401K", "amount": 5, "usePercent": True}
        a = normalize("prismhr", "deduction", raw, dict(CTX, record_id="401K"))
        b = normalize(
            "prismhr", "deduction", raw, dict(CTX, record_id="401K", employee_id="102")
        )
        self.assertNotEqual(a["id"], b["id"])

    def test_company_does_not_gain_employee_relationship(self):
        record = normalize("isolved", "company", {"id": 1}, CTX)
        self.assertNotIn("employee_id", record)

    def test_isolved_benefit_contributions_not_ytd(self):
        raw = {
            "id": 1,
            "employeeId": 101,
            "benefits": [
                {
                    "benefitTitle": "RETIREMENT",
                    "checkEmployeeDeduction": 12.34,
                    "checkEmployerContribution": 6.17,
                    "checkEmployeeCatchUp": 1,
                    "ytdEmployerContribution": 999,
                }
            ],
        }
        r = normalize("isolved", "paycheck", raw, CTX)
        benefit = r["data"]["benefits"][0]
        self.assertEqual(benefit["amount"], "12.34")
        self.assertEqual(benefit["employer_amount"], "6.17")
        self.assertEqual(benefit["employee_catch_up"], "1")
        self.assertEqual(benefit["source_record"]["ytdEmployerContribution"], 999)

    def test_prism_secondary_payroll_lines_normalized(self):
        raw = {
            "voucherId": "1",
            "employeeId": "101",
            "companyTax": [{"comTaxDeductCode": "FICA", "comTaxAmount": 10}],
            "otherDeduction": [{"otherDeductCode": "LOAN", "otherDeductAmount": 20}],
            "otherEarningsDetail": [{"otherEarnCode": "BONUS", "otherEarnAmount": 30}],
            "benefit": [
                {"planId": "MED", "empDeduct": 15, "empContrib": 5, "premiumAmt": 20}
            ],
        }
        r = normalize("prismhr", "paycheck", raw, CTX)
        self.assertEqual(r["data"]["employer_taxes"][0]["amount"], "10")
        self.assertEqual(r["data"]["other_deductions"][0]["amount"], "20")
        self.assertEqual(r["data"]["other_earnings"][0]["amount"], "30")
        self.assertEqual(r["data"]["benefits"][0]["employee_contribution"], "5")
        self.assertEqual(set(r["field_coverage"]), set(dict(leaves(raw))))

    def test_isolved_personal_contact_not_lost(self):
        r = normalize(
            "isolved",
            "employee",
            {
                "id": 101,
                "emailAddress": "general@example.invalid",
                "personal": {
                    "personalEmailAddress": "personal@example.invalid",
                    "mobilePhone": "0000000000",
                },
            },
            CTX,
        )
        self.assertEqual(r["data"]["contact"]["email"], "general@example.invalid")
        self.assertEqual(
            r["data"]["contact"]["personal_email"], "personal@example.invalid"
        )
        self.assertEqual(r["data"]["contact"]["mobile_phone"], "0000000000")

    def test_ukg_primary_email_not_assumed_personal(self):
        r = normalize(
            "ukg-ready",
            "employee",
            {"id": 101, "primary_email": "work@example.invalid"},
            CTX,
        )
        self.assertEqual(r["data"]["contact"]["email"], "work@example.invalid")
        self.assertNotIn("personal_email", r["data"]["contact"])

    def test_invalid_use_percent_does_not_guess_amount(self):
        r = normalize("prismhr", "deduction", {"amount": 12, "usePercent": "T"}, CTX)
        self.assertNotIn("amount", r["data"])
        self.assertNotIn("percentage", r["data"])
        self.assertEqual(r["extensions"]["/amount"], 12)
        self.assertIn("invalid_discriminator", [d["code"] for d in r["diagnostics"]])

    def test_non_deduction_pay_item_rejected(self):
        with self.assertRaises(ValueError):
            normalize("isolved", "deduction", {"id": 1, "payItemType": "Earning"}, CTX)

    def test_live_report_does_not_contain_source_records(self):
        session = {
            "tenant_id": "secret-tenant",
            "context": {"companies": [{"client_id": "1"}]},
            "base_url": "https://example.invalid",
            "auth": {"sessionId": "secret-token"},
            "usage": {"header_name": "sessionId", "header_prefix": ""},
        }
        check = Check("prismhr", session)
        result = {"endpoint": "test", "result": "ok"}
        check.verify(
            result,
            "employee",
            [
                {
                    "id": "101",
                    "firstName": "Private Name",
                    "contactInformation": {"emailAddress": "secret@example.invalid"},
                }
            ],
        )
        encoded = json.dumps(result)
        for secret in (
            "Private Name",
            "secret@example.invalid",
            "secret-token",
            "secret-tenant",
        ):
            self.assertNotIn(secret, encoded)
        self.assertEqual(result["normalized"], 1)
        self.assertTrue(result["field_coverage_valid"])

    def test_live_empty_is_not_successful_record_validation(self):
        check = Check("isolved", {"context": {"companies": [{"legal_id": "1"}]}})
        result = {"endpoint": "test", "result": "ok"}
        check.verify(result, "paycheck", [])
        self.assertEqual(result["result"], "empty")
        self.assertEqual(result["normalized"], 0)

    def test_live_redirects_never_forward_credentials(self):
        self.assertIsNone(
            NoRedirect().redirect_request(
                None, None, 302, "", {}, "https://other.invalid"
            )
        )

    def test_live_http_error_stays_failure(self):
        session = {
            "base_url": "https://example.invalid",
            "auth": {"sessionId": "secret"},
            "context": {"companies": [{"client_id": "1"}]},
            "usage": {"header_name": "sessionId", "header_prefix": ""},
        }
        check = Check("prismhr", session)
        with patch(
            "tada.live_check.request_json", return_value=(404, None, "http_error")
        ):
            body, result = check.get("GET /template/{id}", "/record/real-id")
        self.assertIsNone(body)
        self.assertEqual(result["result"], "failed")
        self.assertNotIn("real-id", json.dumps(result))

    def test_live_prism_error_envelope_is_not_success(self):
        session = {
            "base_url": "https://example.invalid",
            "auth": {"sessionId": "secret"},
            "context": {"companies": [{"client_id": "1"}]},
            "usage": {"header_name": "sessionId", "header_prefix": ""},
        }
        check = Check("prismhr", session)
        with patch(
            "tada.live_check.request_json",
            return_value=(200, {"errorCode": "500", "errorMessage": "private"}, None),
        ):
            body, result = check.get("GET /template", "/record")
        self.assertIsNone(body)
        self.assertEqual(result["reason"], "provider_error_envelope")
        self.assertNotIn("private", json.dumps(result))


if __name__ == "__main__":
    unittest.main()

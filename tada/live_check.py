"""Opt-in, read-only demo API smoke tests. Never writes tokens or provider records."""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

from .adapters import normalize
from .core import loads, leaves

SIGNIN = "https://tada-demo-provider-signin.onrender.com/signin"
TENANTS = {"prismhr": "prism", "isolved": "isol", "ukg-ready": "ukg"}
PRISM_OPTIONS = ",".join(
    [
        "Person",
        "Client",
        "Compensation",
        "DirectDeposit",
        "EmployeeEvents",
        "Health",
        "Skills",
        "AbsenceJournal",
        "BenefitEnrollStatus",
        "ScheduledDeductions",
        "NewHireQuestions",
        "EnrollmentInprogress",
        "ContactInformation",
        "HSA",
    ]
)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward a token to a redirect target.
        return None


def request_json(url, headers, body=None, timeout=45):
    if urlparse(url).scheme != "https":
        return None, None, "https_required"
    opener = build_opener(NoRedirect())
    for attempt in range(3):
        try:
            req = Request(
                url,
                headers=headers,
                data=json.dumps(body).encode() if body is not None else None,
            )
            with opener.open(req, timeout=timeout) as response:
                return response.status, loads(response.read().decode()), None
        except HTTPError as error:
            code = error.code
            retry = error.headers.get(
                "Retry-After", error.headers.get("X-CallLimit-TimeToWait", "1")
            )
            error.close()
            if code in (429, 503) and attempt < 2:
                try:
                    delay = min(5, max(0, float(retry)))
                except ValueError:
                    delay = 1
                time.sleep(delay)
                continue
            return code, None, "http_error"
        except (URLError, TimeoutError, ValueError, OSError):
            # Exception messages can contain URLs, identifiers or response content.
            return None, None, "transport_or_json_error"
    return None, None, "retry_exhausted"


def signin(provider, key):
    return request_json(
        SIGNIN,
        {"X-API-Key": key, "Content-Type": "application/json"},
        {"tenant": TENANTS[provider]},
        timeout=90,
    )


class Check:
    def __init__(self, provider, session):
        self.provider = provider
        self.session = session
        self.results = []
        self.company = session["context"]["companies"][0]
        self.company_id = self.company.get(
            "legal_id", self.company.get("company_id", self.company.get("client_id"))
        )

    def get(self, template, path, params=None):
        base = self.session["base_url"].rstrip("/")
        token = self.session["auth"].get(
            "sessionId", self.session["auth"].get("access_token")
        )
        usage = self.session["usage"]
        headers = {
            usage["header_name"]: usage["header_prefix"] + token,
            "Accept": "application/json",
        }
        if self.provider == "ukg-ready":
            headers["X-End-of-Support-Timeline"] = "2026-01-29"
        url = base + path + ("?" + urlencode(params) if params else "")
        status, body, error = request_json(url, headers)
        result = {
            "endpoint": template,
            "http_status": status,
            "result": "failed" if error else "ok",
        }
        if error:
            result["reason"] = error
        if (
            self.provider == "prismhr"
            and isinstance(body, dict)
            and body.get("errorCode") not in (None, "", "0", 0)
        ):
            result.update(result="failed", reason="provider_error_envelope")
            body = None
        self.results.append(result)
        return body, result

    def verify(self, result, entity, records, employee_id=None, run_id=None):
        if records is None:
            return
        if not isinstance(records, list):
            result.update(result="failed", reason="unexpected_response_shape")
            return
        result.update(
            entity=entity,
            records_seen=len(records),
            normalized=0,
            field_coverage_valid=True,
        )
        diagnostics = Counter()
        schema_differences = 0
        try:
            from .contracts import source_errors
            import jsonschema  # noqa: F401

            result["source_validation"] = "performed"
        except ImportError:
            source_errors = None
            result["source_validation"] = "not_installed"
        for index, raw in enumerate(records[:2]):
            context = {
                "tenant_id": str(self.session["tenant_id"]),
                "company_id": str(self.company_id),
            }
            if employee_id is not None:
                context["employee_id"] = str(employee_id)
            if run_id is not None:
                context["payroll_run_id"] = str(run_id)
            if entity in ("direct_deposit", "deduction", "pay_info", "demographics"):
                context["record_id"] = str(
                    raw.get("deductionCode", f"smoke-test-slot-{index}")
                )
            try:
                canonical = normalize(self.provider, entity, raw, context)
                valid = canonical["source_record"] == raw and set(
                    canonical["field_coverage"]
                ) == set(dict(leaves(raw)))
                result["field_coverage_valid"] &= valid
                if not valid:
                    result.update(result="failed", reason="source_loss")
                diagnostics.update(d["code"] for d in canonical["diagnostics"])
                result["normalized"] += 1
                if source_errors:
                    schema_differences += len(source_errors(self.provider, entity, raw))
            except (ValueError, KeyError, TypeError):
                result.update(result="failed", reason="normalization_error")
        result["diagnostics_by_code"] = dict(diagnostics)
        if source_errors:
            result["source_schema_differences"] = schema_differences
        if not records:
            result["result"] = "empty"

    def prism(self, year):
        cid = self.company_id
        body, result = self.get(
            "GET /clientMaster/v1/getClientMaster",
            "/clientMaster/v1/getClientMaster",
            {"clientId": cid},
        )
        if body:
            self.verify(result, "company", [body["clientMaster"]])
        body, result = self.get(
            "GET /employee/v1/getEmployeeList",
            "/employee/v1/getEmployeeList",
            {"clientId": cid},
        )
        ids = (body or {}).get("employeeList", {}).get("employeeId", [])
        result["records_seen"] = len(ids)
        if ids:
            eid = ids[0]
            body, result = self.get(
                "GET /employee/v1/getEmployee (all documented sections)",
                "/employee/v1/getEmployee",
                {"clientId": cid, "employeeId": eid, "options": PRISM_OPTIONS},
            )
            employees = (body or {}).get("employee", [])
            self.verify(result, "employee", employees if body else None)
            if employees:
                deposits = (employees[0].get("directDeposit") or {}).get(
                    "achVoucher", []
                )
                deposit_result = {
                    "endpoint": "employee.directDeposit.achVoucher[]",
                    "result": "ok",
                    "http_status": result["http_status"],
                }
                self.results.append(deposit_result)
                self.verify(deposit_result, "direct_deposit", deposits, eid)
            body, result = self.get(
                "GET /deductions/v1/getDeductions",
                "/deductions/v1/getDeductions",
                {"clientId": cid, "employeeId": eid},
            )
            self.verify(
                result,
                "deduction",
                (body or {}).get("employeeDeductions", {}).get("deduction", [])
                if body
                else None,
                eid,
            )
        body, result = self.get(
            "GET /payroll/v1/getPayrollSummary",
            "/payroll/v1/getPayrollSummary",
            {"clientId": cid, "year": year},
        )
        runs = (body or {}).get("payrollHistory", [])
        self.verify(result, "payroll_run", runs if body else None)
        if runs:
            body, result = self.get(
                "GET /payroll/v1/getPayrollVoucherForBatch (page 0)",
                "/payroll/v1/getPayrollVoucherForBatch",
                {
                    "clientId": cid,
                    "batchId": runs[0]["batchId"],
                    "count": 2,
                    "startpage": 0,
                    "options": "EmployerContribution,Retirement,TaxFilingStatus,WCInformation,Arrears",
                },
            )
            self.verify(
                result,
                "paycheck",
                (body or {}).get("payrollVoucher", []) if body else None,
            )

    def isolved(self, year):
        cid, lid = self.company["client_id"], self.company["legal_id"]
        base = f"/api/clients/{cid}/legals/{lid}"
        template = "GET /api/clients/{clientId}/legals/{legalId}"
        company, result = self.get(template, base, {"includeDetails": "true"})
        if company:
            self.verify(result, "company", [company])
        body, result = self.get(
            template + "/employees",
            base + "/employees",
            {
                "page": 1,
                "pageSize": 2,
                "includeOrganizations": "true",
                "includeMiscFields": "true",
                "includeLabors": "true",
                "includeAlternateRates": "true",
                "includeTaxes": "true",
            },
        )
        employees = (body or {}).get("results", [])
        self.verify(result, "employee", employees if body else None)
        if employees:
            eid = employees[0]["id"]
            body, result = self.get(
                template + "/employees/{employeeId}/directdeposits",
                base + f"/employees/{eid}/directdeposits",
            )
            self.verify(result, "direct_deposit", body, eid)
            body, result = self.get(
                template + "/employees/{employeeId}/payItems",
                base + f"/employees/{eid}/payItems",
            )
            deductions = (
                [r for r in body if r.get("payItemType") == "Deduction"]
                if isinstance(body, list)
                else None
            )
            self.verify(result, "deduction", deductions, eid)
            body, result = self.get(
                template + "/employees/{employeeId}/checks",
                base + f"/employees/{eid}/checks",
                {"includeDetails": "true", "yearFilter": year},
            )
            self.verify(
                result,
                "paycheck",
                (body or {}).get("results", []) if body else None,
                eid,
            )
        groups = (company or {}).get("payGroups", [])
        if groups:
            body, result = self.get(
                template + "/paygroupId/{paygroupId}/payrollRunHistory",
                base + f"/paygroupId/{groups[0]['id']}/payrollRunHistory",
            )
            self.verify(
                result,
                "payroll_run",
                body
                if isinstance(body, list)
                else (body or {}).get("results")
                if body
                else None,
            )

    def ukg(self, year):
        base = f"/rest/v2/companies/{self.company_id}"
        template = "GET /rest/v2/companies/{cid}"
        body, result = self.get(
            template + "/employees", base + "/employees", {"page": 0, "size": 2}
        )
        employees = (body or {}).get("employees", [])
        result["records_seen"] = len(employees)
        if employees:
            eid = employees[0]["id"]
            body, result = self.get(
                template + "/employees/{aid}", base + f"/employees/{eid}"
            )
            if body:
                self.verify(result, "employee", [body])
            body, result = self.get(
                template + "/employees/{aid}/pay-info",
                base + f"/employees/{eid}/pay-info",
            )
            if body:
                self.verify(result, "pay_info", [body], eid)
            body, result = self.get(
                template + "/employees/{aid}/direct-deposits",
                base + f"/employees/{eid}/direct-deposits",
            )
            self.verify(
                result,
                "direct_deposit",
                (body or {}).get("deposits", []) if body else None,
                eid,
            )
            body, result = self.get(
                template + "/employees/{aid}/deductions",
                base + f"/employees/{eid}/deductions",
            )
            deductions = (body or {}).get("deductions", [])
            result["records_seen"] = len(deductions)
            if deductions:
                body, result = self.get(
                    template + "/employees/{aid}/deductions/{id}",
                    base + f"/employees/{eid}/deductions/{deductions[0]['id']}",
                )
                if body:
                    self.verify(result, "deduction", [body], eid)
        body, result = self.get(template + "/payrolls", base + "/payrolls")
        runs = (body or {}).get("payrolls", [])
        self.verify(result, "payroll_run", runs if body else None)
        # Probe at most three recent runs; an empty list is not a paycheck validation.
        for run in runs[-3:][::-1]:
            rid = run["id"]
            body, result = self.get(
                template + "/payrolls/{id}/pay-statements",
                base + f"/payrolls/{rid}/pay-statements",
            )
            statements = (body or {}).get("pay_statements", [])
            result["records_seen"] = len(statements)
            if not statements:
                if result["result"] == "ok":
                    result["result"] = "empty"
                continue
            body, result = self.get(
                template + "/payrolls/{id}/pay-statements/{id}",
                base + f"/payrolls/{rid}/pay-statements/{statements[0]['id']}",
            )
            if body:
                self.verify(result, "paycheck", [body], run_id=rid)
            break

    def run(self, year):
        try:
            {"prismhr": self.prism, "isolved": self.isolved, "ukg-ready": self.ukg}[
                self.provider
            ](year)
        except (KeyError, TypeError, ValueError):
            self.results.append(
                {
                    "endpoint": "response processing",
                    "result": "failed",
                    "reason": "unexpected_response_shape",
                }
            )
        return {"provider": self.provider, "checks": self.results}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=["all", *TENANTS], default="all")
    parser.add_argument("--year", type=int, default=datetime.now(timezone.utc).year)
    parser.add_argument("--report", default="local/live-check.json")
    args = parser.parse_args(argv)
    key = os.environ.get("DEMO_SIGNIN_API_KEY")
    if not key:
        parser.error(
            "Set DEMO_SIGNIN_API_KEY locally; never put it in a command argument or Git"
        )
    providers = list(TENANTS) if args.provider == "all" else [args.provider]

    def check(provider):
        status, session, error = signin(provider, key)
        if error:
            return {
                "provider": provider,
                "checks": [
                    {
                        "endpoint": "POST /signin",
                        "http_status": status,
                        "result": "failed",
                        "reason": error,
                    }
                ],
            }
        return Check(provider, session).run(args.year)

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, providers))
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "year": args.year,
        "scope": "Bounded read-only smoke test; first company, sample employees and paychecks. Not a complete sync.",
        "contains_provider_records_or_tokens": False,
        "providers": results,
    }
    path = Path(args.report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n")
    failed = sum(c["result"] == "failed" for r in results for c in r["checks"])
    print(
        f"Live checks complete: {failed} unavailable/failed checks. Sanitized report: {path}"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

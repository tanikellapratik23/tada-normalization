"""Explicit provider bindings. See docs/MAPPINGS.md for evidence and units."""

from decimal import Decimal
from .core import Mapper, MISSING, decimal, get, identity, iso_date, record_id, leaves

PROVIDERS = ("prismhr", "isolved", "ukg-ready")
ENTITIES = (
    "company",
    "employee",
    "direct_deposit",
    "deduction",
    "payroll_run",
    "paycheck",
    "compensation",
    "pay_info",
    "demographics",
)

# Canonical destination -> provider source. Unlisted fields remain individually accounted for.
EMPLOYEE = {
    "prismhr": {
        "profile.first_name": "firstName",
        "profile.last_name": "lastName",
        "profile.middle_name": "middleInitial",
        "profile.preferred_name": "preferredName",
        "profile.birth_date": "person.birthDate",
        "profile.marital_status_code": "person.maritalStatus",
        "profile.gender_code": "person.gender",
        "profile.pronouns": "client.preferredPronoun",
        "profile.language": "person.preferredLanguage",
        "contact.personal_email": "contactInformation.emailAddress",
        "contact.work_email": "client.workEmail",
        "contact.home_phone": "contactInformation.homePhone",
        "contact.mobile_phone": "contactInformation.mobilePhone",
        "contact.work_phone": "client.workPhone",
        "contact.work_phone_extension": "client.workPhoneExt",
        "address.line1": "contactInformation.addressLine1",
        "address.line2": "contactInformation.addressLine2",
        "address.city": "contactInformation.city",
        "address.region": "contactInformation.state",
        "address.postal_code": "contactInformation.zipcode",
        "address.postal_suffix": "contactInformation.zipSuffix",
        "employment.employee_number": "client.clientEmployeeId",
        "employment.status_code": "client.employeeStatus",
        "employment.type_code": "client.employeeType",
        "employment.first_hire_date": "client.firstHireDate",
        "employment.hire_date": "client.lastHireDate",
        "employment.status_date": "client.statusDate",
        "employment.seniority_date": "client.seniorityDate",
        "employment.return_date": "client.returnDate",
        "employment.termination_reason_code": "client.termReasonCode",
        "job.code": "client.jobCode",
        "job.start_date": "client.jobStartDate",
        "job.flsa_exempt": "client.flsaExempt",
        "organization.department_code": "client.homeDepartment",
        "organization.division_code": "client.homeDivision",
        "organization.location_code": "client.homeLocation",
        "organization.manager_source_id": "client.manager",
        "organization.union_code": "client.unionCode",
        "organization.shift_code": "client.workShift",
        "compensation.hourly_rate": "compensation.hourlyPay",
        "compensation.period_salary": "compensation.salary",
        "compensation.annual_salary": "compensation.annualPay",
        "compensation.standard_hours": "compensation.standardHours",
        "compensation.effective_date": "compensation.effectiveDate",
        "compensation.pay_group": "compensation.payGroup",
        "compensation.pay_period_code": "compensation.payPeriod",
        "emergency_contacts": "person.emergencyContact",
        "skills_education": "skillsAndEducation",
    },
    "isolved": {
        "profile.first_name": "nameAddress.firstName",
        "profile.last_name": "nameAddress.lastName",
        "profile.middle_name": "nameAddress.middleName",
        "profile.preferred_name": "nameAddress.preferredName",
        "profile.pronouns": "nameAddress.preferredPronouns",
        "profile.birth_date": "birthDate",
        "profile.gender_code": "gender",
        "profile.marital_status_code": "maritalStatus",
        "contact.personal_email": "emailAddress",
        "address.line1": "nameAddress.address1",
        "address.line2": "nameAddress.address2",
        "address.city": "nameAddress.city",
        "address.region": "nameAddress.state",
        "address.postal_code": "nameAddress.zipCode",
        "employment.employee_number": "employeeNumber",
        "employment.status_code": "employmentStatus",
        "employment.first_hire_date": "originalHireDate",
        "employment.hire_date": "hireDate",
        "employment.rehire_date": "rehireDate",
        "employment.termination_date": "terminationDate",
        "employment.status_date": "statusDate",
        "employment.termination_reason_code": "terminationReason",
        "employment.type_code": "employmentCategoryCode",
        "employment.eligible_for_rehire": "eligibleForRehire",
        "employment.remote_worker": "isRemoteWorker",
        "job.code": "jobCode",
        "job.title": "jobTitle",
        "job.flsa_exempt": "jobFLSAExempt",
        "job.start_date": "jobEffectiveDate",
        "organization.assignments": "organizations",
        "organization.labor_assignments": "labors",
        "organization.location_code": "workLocation",
        "organization.team": "team",
        "compensation.hourly_rate": "hourlyRate",
        "compensation.period_salary": "perPaySalary",
        "compensation.annual_salary": "annualSalary",
        "compensation.standard_hours": "normalHours",
        "compensation.effective_date": "salaryEffectiveDate",
        "compensation.periods_per_year": "payFrequency",
        "compensation.pay_group": "payGroup",
        "compensation.alternate_rates": "payRates",
        "tax_settings": "taxes",
        "custom_fields": "miscFields",
        "custom_data_sets": "miscDataSets",
    },
    "ukg-ready": {
        "profile.first_name": "first_name",
        "profile.last_name": "last_name",
        "profile.middle_name": "middle_name",
        "profile.preferred_name": "nickname",
        "profile.birth_date": "dates.birthday",
        "contact.personal_email": "primary_email",
        "contact.secondary_email": "secondary_email",
        "contact.home_phone": "phones.home_phone",
        "contact.mobile_phone": "phones.cell_phone",
        "contact.work_phone": "phones.work_phone",
        "address.line1": "address.address_line_1",
        "address.line2": "address.address_line_2",
        "address.line3": "address.address_line_3",
        "address.city": "address.city",
        "address.region": "address.state",
        "address.postal_code": "address.zip",
        "address.country": "address.country",
        "employment.employee_number": "employee_id",
        "employment.status_code": "status",
        "employment.hire_date": "dates.hired",
        "employment.rehire_date": "dates.re_hired",
        "employment.termination_date": "dates.terminated",
        "employment.seniority_date": "dates.seniority",
        "employment.start_date": "dates.started",
        "organization.managers": "managers",
        "organization.cost_centers": "cost_centers_info",
        "organization.ein": "ein",
        "custom_fields": "account_extra_fields",
        "custom_dates": "dates.custom_dates",
    },
}


def mapped(m, bindings):
    for target, source in bindings.items():
        conv = iso_date if target.endswith("_date") else None
        if target.split(".")[-1] in (
            "hourly_rate",
            "period_salary",
            "annual_salary",
            "standard_hours",
            "gross_pay",
            "net_pay",
            "amount",
            "percentage",
            "limit",
            "maximum",
        ):
            conv = decimal
        m.field(source, target, conv)


def line_items(m, source, target, bindings):
    raw = get(m.raw, source)
    if raw is MISSING or raw is None:
        m.field(source, target)
        return
    if not isinstance(raw, list) or any(not isinstance(x, dict) for x in raw):
        m.warn("invalid_value", "/" + source, "Expected an array of objects")
        return
    items = []
    for i, item in enumerate(raw):
        normalized = {}
        for name, key in bindings.items():
            value = get(item, key)
            if value is not MISSING:
                if value is not None and name in (
                    "amount",
                    "employer_amount",
                    "hours",
                    "rate",
                    "taxable_wages",
                ):
                    try:
                        value = decimal(value)
                    except (ValueError, TypeError):
                        m.warn(
                            "invalid_value",
                            f"/{source}/{i}/{key}",
                            "Invalid line amount retained in source record",
                        )
                        value = None
                normalized[name] = value
        normalized["source_record"] = item
        items.append(normalized)
    # Arrays keep their complete source records, including accumulations, flags and unsupported units.
    m.set(target, items)
    for index, item in enumerate(raw):
        for pointer, _ in leaves(item):
            original = "/" + source + "/" + str(index) + pointer
            mapped_name = next(
                (
                    name
                    for name, key in bindings.items()
                    if pointer == "/" + key.replace(".", "/")
                ),
                None,
            )
            destination = (
                "/" + mapped_name if mapped_name else "/source_record" + pointer
            )
            m.used[original] = (
                "/data/" + target.replace(".", "/") + "/" + str(index) + destination
            )


def normalize(provider, entity, raw, context):
    if provider not in PROVIDERS or entity not in ENTITIES:
        raise ValueError("Unsupported provider or entity")
    if not isinstance(raw, dict) or not isinstance(context, dict):
        raise ValueError("record and context must be objects")
    for key in ("tenant_id", "company_id"):
        if key not in context or context[key] is None or str(context[key]) == "":
            raise ValueError("Missing context." + key)
    if (
        entity
        in ("direct_deposit", "deduction", "compensation", "pay_info", "demographics")
        and context.get("employee_id") is None
    ):
        raise ValueError("Employee-scoped entity requires context.employee_id")
    id_key = (
        {"payroll_run": "batchId", "paycheck": "voucherId"}.get(entity, "id")
        if provider == "prismhr"
        else "id"
    )
    source_id = record_id(raw, context, id_key)
    if entity == "company" and str(source_id) != str(context["company_id"]):
        raise ValueError("Company ID conflicts with context.company_id")
    m = Mapper(provider, entity, raw, context, source_id)
    m.field(id_key, "source_id", str)
    if entity == "company":
        bindings = {
            "prismhr": {
                "name": "clientName",
                "legal_name": "legalName",
                "tax_id": "federalIdNumber",
                "address.line1": "addressLine1",
                "address.city": "city",
                "address.region": "stateCode",
                "address.postal_code": "zipCode",
            },
            "isolved": {
                "name": "dbaName",
                "legal_name": "legalName",
                "tax_id": "federalEIN",
                "address": "legalAddress",
            },
            "ukg-ready": {"name": "name"},
        }
        mapped(m, bindings[provider])
        if provider == "prismhr":
            m.enum(
                "statusClass",
                "status",
                {
                    "A": "active",
                    "P": "pending",
                    "I": "inactive",
                    "C": "cancelling",
                    "T": "terminated",
                },
            )
        if provider == "ukg-ready":
            m.warn(
                "context_only_company",
                "/",
                "Company ID/name imported from caller context; no company response schema in selected UKG bundle",
            )
    elif entity == "employee":
        mapped(m, EMPLOYEE[provider])
        if provider == "prismhr":
            m.enum(
                "client.statusClass",
                "employment.status",
                {"A": "active", "L": "on_leave", "T": "terminated"},
            )
            m.enum(
                "compensation.payMethod",
                "compensation.basis",
                {"S": "salary", "H": "hourly", "C": "commission", "D": "driver"},
            )
        else:
            # Tenant-configured labels are deliberately not guessed from text.
            source = "employmentStatus" if provider == "isolved" else "status"
            m.enum(
                source, "employment.status", context.get("employment_status_map", {})
            )
        manager = get(m.out["data"], "organization.manager_source_id")
        if manager is not MISSING and manager not in (None, ""):
            m.set(
                "organization.manager_id",
                identity(
                    provider,
                    context["tenant_id"],
                    context["company_id"],
                    "employee",
                    manager,
                ),
            )
    elif entity == "direct_deposit":
        deposit(m)
    elif entity == "deduction":
        deduction(m)
    elif entity in ("payroll_run", "paycheck"):
        payroll(m, entity)
    elif provider == "ukg-ready" and entity == "compensation":
        mapped(
            m,
            {
                "amount": "amount",
                "hourly_rate": "hourly_pay",
                "currency": "currency",
                "effective_date": "effective_from",
                "periods_per_year": "num_pp_in_year",
                "auto_pay": "auto_pay",
            },
        )
        m.enum(
            "amount_period",
            "basis",
            {
                "YEAR": "year",
                "MONTH": "month",
                "WEEK": "week",
                "HOUR": "hour",
                "PAY_PERIOD": "pay_period",
            },
        )
        m.field(
            "time",
            "standard_hours",
            lambda v: decimal(Decimal(str(v)) / Decimal(3600000)),
        )
        m.field("time_period", "hours_period")
    elif provider == "ukg-ready" and entity == "pay_info":
        mapped(
            m,
            {
                "job.source_id": "default_job.id",
                "job.effective_date": "job_last_changed",
                "employment.type_code": "employee_type.id",
                "compensation.pay_type_code": "pay_type.id",
                "organization.union_id": "union.id",
                "organization.pay_grade": "pay_grade",
                "workers_comp_code": "workers_comp_code.external_id",
                "payroll_classification": "payroll_classification",
            },
        )
        m.field(
            "standard_work_day",
            "compensation.standard_day_hours",
            lambda v: decimal(Decimal(str(v)) / Decimal(3600000)),
        )
    elif provider == "ukg-ready" and entity == "demographics":
        for key in raw:
            m.field(key, "profile." + key)
    else:
        raise ValueError("Supplement entity only supported for UKG Ready")
    return m.finish()


def deposit(m):
    p = m.provider
    if p == "prismhr":
        mapped(
            m,
            {
                "account.number": "accountNum",
                "account.routing_number": "transitNum",
                "account.bank_name": "bankName",
                "limit": "limit",
                "voucher_types": "voucherTypeOverride",
            },
        )
        m.enum(
            "accountType",
            "account.type",
            {"C": "checking_or_pay_card", "S": "savings", "IP": "instant_pay"},
        )
        methods = {
            "F": "fixed",
            "FS": "fixed_skip_if_insufficient",
            "P": "percentage",
            "PN": "percentage_of_remainder",
            "B": "remainder",
        }
        m.enum("method", "allocation.method", methods)
        m.enum("status", "status", {"P": "prenote", "D": "active", "I": "inactive"})
        method = m.raw.get("method")
        if method in ("F", "FS"):
            m.field("amount", "allocation.amount", decimal)
        elif method in ("P", "PN"):
            m.field("amount", "allocation.percentage", decimal)
        elif method == "B" and "amount" in m.raw:
            m.warn(
                "conflicting_allocation",
                "/amount",
                "Balance method must not specify amount",
            )
        m.warn(
            "priority_unavailable",
            "/",
            "AchVoucher has no documented priority; array order is not asserted to be priority",
        )
    elif p == "isolved":
        mapped(
            m,
            {
                "account.number": "accountNumber",
                "account.routing_number": "routingNumber",
                "account.bank_name": "bankName",
                "priority": "sequenceNumber",
                "frequency_code": "frequency",
            },
        )
        m.enum(
            "accountType",
            "account.type",
            {"Checking": "checking", "Savings": "savings"},
        )
        m.enum("status", "status", m.context.get("deposit_status_map", {}))
        amount, percent = m.raw.get("amount"), m.raw.get("percent")
        if amount is not None and percent is not None:
            m.warn(
                "conflicting_allocation",
                "/",
                "Amount and percent are mutually exclusive",
            )
            method = "unknown"
        elif m.raw.get("sequenceNumber") == 0:
            method = "remainder"
        elif amount is not None:
            method = "fixed"
        elif percent is not None:
            method = "percentage"
        else:
            method = "unknown"
        m.set(
            "allocation.method",
            {"value": method, "source_value": m.raw.get("sequenceNumber")},
        )
        m.field("amount", "allocation.amount", decimal)
        m.field("percent", "allocation.percentage", decimal)
    else:
        mapped(
            m,
            {
                "account.number": "account_number",
                "account.routing_number": "routing_number",
                "account.routing_type": "routing_type",
                "priority": "sequence",
                "effective_start_date": "active_from",
                "effective_end_date": "active_to",
                "currency": "currency",
                "allocation.amount": "amount",
                "allocation.percentage": "percentage",
                "frequency": "payroll_frequency",
                "prenote_status": "pre_note_status",
                "underfunding_rule": "arrearage_function",
            },
        )
        m.enum(
            "account_type",
            "account.type",
            {"CHECKING": "checking", "SAVINGS": "savings"},
        )
        m.enum(
            "type",
            "payment_type",
            {
                "DIRECT_DEPOSIT": "direct_deposit",
                "RESERVE_LIVE_CHECK": "reserve_live_check",
            },
        )
        m.field(
            "active",
            "status",
            lambda v: {
                "value": "active"
                if v is True
                else "inactive"
                if v is False
                else "unknown",
                "source_value": v,
            },
        )
        m.enum(
            "calc_method.type",
            "allocation.method",
            {
                "FULL": "remainder",
                "FLAT_AMOUNT": "fixed",
                "GROSS_EARNING": "percentage_of_gross",
                "NET_PAY": "percentage_of_net",
                "DIRECT_DEPOSIT_PER_OF_REMAINDER": "percentage_of_remainder",
            },
        )
    percentage = get(m.out["data"], "allocation.percentage")
    if (
        percentage is not MISSING
        and percentage is not None
        and not Decimal(0) <= Decimal(percentage) <= Decimal(100)
    ):
        m.warn(
            "percentage_out_of_range",
            "/allocation/percentage",
            "Percentage points must lie between 0 and 100",
        )


def deduction(m):
    if m.provider == "prismhr":
        mapped(
            m,
            {
                "code": "deductionCode",
                "description": "description",
                "effective_start_date": "startDate",
                "effective_end_date": "stopDate",
                "limit": "limit",
                "maximum": "maximum",
                "maximum_basis_code": "basis",
                "schedule_code": "period",
                "rules.track_arrears": "trackArrears",
                "rules.mandatory": "mandatory",
                "rules.match_method": "matchMethod",
                "rules.match_amount": "matchAmount",
            },
        )
        m.field(
            "amount",
            "percentage" if m.raw.get("usePercent") is True else "amount",
            decimal,
        )
        m.enum(
            "deductionType",
            "type",
            {
                "V": "voluntary",
                "C": "section_125",
                "P": "post_tax_benefit",
                "F": "flexible_spending",
                "G": "garnishment",
                "L": "employee_loan",
                "K": "pretax_retirement",
                "KC": "retirement_catch_up",
                "KE": "posttax_retirement",
                "KL": "retirement_loan",
                "KR": "roth_401k",
                "KCR": "roth_catch_up",
            },
        )
        m.field("usePercent", "is_percentage")
    elif m.provider == "isolved":
        mapped(
            m,
            {
                "code": "payItemCode",
                "description": "payItemName",
                "source_type": "payItemType",
                "effective_start_date": "startDate",
                "effective_end_date": "stopDate",
                "schedule_code": "scheduleOverride",
                "calculation_parameters": "calcParams",
            },
        )
        m.warn(
            "tenant_calculation_rules",
            "/calcParams",
            "Parameter types require tenant configuration; no amount or percentage inferred",
        )
    else:
        mapped(
            m,
            {
                "code": "deduction.code",
                "description": "deduction.name",
                "effective_start_date": "effective_from",
                "effective_end_date": "effective_to",
                "priority": "sequence",
                "amount": "ee_calc_method.amount",
                "percentage": "ee_calc_method.percent",
                "calculation_method_code": "ee_calc_method.method.type",
                "rules.maximum": "annual_max_amount",
                "rules.employer_maximum": "er_annual_max_amount",
                "rules.employee_frequency": "ee_frequency",
                "rules.employer_frequency": "er_frequency",
                "rules.minimum": "ee_min_calc_method",
                "rules.maximum_calculation": "ee_max_calc_method",
                "vendor": "vendor",
                "organization.cost_centers": "cost_centers",
            },
        )
        m.warn(
            "deduction_units_unverified",
            "/ee_calc_method",
            "Cached deduction schema does not establish currency scaling or percentage basis; numeric values preserved without scaling",
        )


def payroll(m, entity):
    p = m.provider
    if entity == "payroll_run":
        mapped(
            m,
            {
                "prismhr": {
                    "description": "description",
                    "pay_date": "payDate",
                    "gross_pay": "grossEarnings",
                },
                "isolved": {
                    "pay_date": "payDate",
                    "period_start_date": "periodBeginDate",
                    "period_end_date": "periodEndDate",
                    "run_number": "runNumber",
                    "status_code": "status",
                    "type_code": "payrollRunType",
                },
                "ukg-ready": {
                    "description": "name",
                    "pay_date": "pay_date",
                    "period_start_date": "start_date",
                    "period_end_date": "end_date",
                    "type_code": "type.id",
                    "status_code": "status",
                    "ein": "ein",
                },
            }[p],
        )
        if p == "prismhr":
            m.enum(
                "type",
                "type",
                {
                    "R": "scheduled",
                    "S": "special",
                    "J": "adjustment",
                    "V": "reversal",
                    "M": "manual",
                },
            )
        return
    emp_path = "employee.account_id" if p == "ukg-ready" else "employeeId"
    employee = get(m.raw, emp_path)
    if employee is MISSING or employee is None:
        raise ValueError("Paycheck requires employee identifier")
    if m.context.get("employee_id") is not None and str(
        m.context["employee_id"]
    ) != str(employee):
        raise ValueError("Conflicting employee identifier")
    m.out["employee_id"] = identity(
        p, m.context["tenant_id"], m.context["company_id"], "employee", employee
    )
    m.field(emp_path, "employee_source_id", str)
    run = m.raw.get("batchId") if p == "prismhr" else m.context.get("payroll_run_id")
    if run is not None:
        m.out["payroll_run_id"] = identity(
            p, m.context["tenant_id"], m.context["company_id"], "payroll_run", run
        )
    else:
        m.warn(
            "missing_run_link",
            "/",
            "Supply context.payroll_run_id; run sequence numbers are not unique run IDs",
        )
    mapped(
        m,
        {
            "prismhr": {
                "gross_pay": "totalEarnings",
                "net_pay": "netPay",
                "pay_date": "payDate",
                "period_start_date": "payPeriodStart",
                "period_end_date": "payPeriodEnd",
                "check_number": "checkNumber",
                "void_date": "voidDate",
            },
            "isolved": {
                "gross_pay": "grossPay",
                "net_pay": "netPay",
                "pay_date": "checkDate",
                "period_start_date": "periodBeginDate",
                "period_end_date": "periodEndDate",
                "check_number": "checkNumber",
                "run_number": "payrollRunNumber",
            },
            "ukg-ready": {
                "pay_date": "pay_date",
                "period_start_date": "pay_period_start",
                "period_end_date": "pay_period_end",
                "status_code": "status",
                "type_code": "type.id",
            },
        }[p],
    )
    if p == "prismhr":
        line_items(
            m,
            "earning",
            "earnings",
            {
                "code": "payCode",
                "description": "payClassDescription",
                "hours": "hoursWorked",
                "rate": "payAmount",
                "units": "hoursUnits",
            },
        )
        line_items(
            m,
            "deduction",
            "deductions",
            {
                "code": "deductCode",
                "description": "deductDescription",
                "amount": "deductAmount",
                "type_code": "deductType",
            },
        )
        line_items(
            m,
            "employeeTax",
            "employee_taxes",
            {
                "code": "empTaxDeductCode",
                "amount": "empTaxAmount",
                "taxable_wages": "empTaxableAmount",
            },
        )
        line_items(
            m,
            "employerContributions",
            "employer_contributions",
            {"code": "code", "description": "description", "amount": "amount"},
        )
        for source, target in [
            ("otherEarningsDetail", "other_earnings"),
            ("companyTax", "employer_taxes"),
            ("otherDeduction", "other_deductions"),
            ("benefit", "benefits"),
        ]:
            m.field(source, target)
        m.warn(
            "earnings_amount_ambiguous",
            "/earning",
            "payAmount is described as pay per hour or unit, so mapped as rate; line totals are not inferred",
        )
    elif p == "isolved":
        for source in ("earnings", "deductions", "garnishments", "benefits", "taxes"):
            bindings = {
                "code": "itemCode",
                "description": "itemDescription",
                "amount": "checkDollars",
            }
            if source == "earnings":
                bindings.update({"hours": "checkHours", "units": "checkUnits"})
            if source == "taxes":
                bindings.update(
                    {
                        "is_employee_tax": "isEmployeeTax",
                        "taxable_wages": "checkTaxableWages",
                    }
                )
            line_items(m, source, source, bindings)
        m.warn(
            "accumulation_basis",
            "/",
            "checkDollars/checkHours selected for this paycheck; current/YTD fields retained separately in source records",
        )
    else:
        for source, singular in [
            ("earnings", "earning"),
            ("deductions", "deduction"),
            ("taxes", "company_tax"),
        ]:
            bindings = {
                "code": singular + ".code",
                "description": singular + ".name",
                "amount": "ee_amount",
                "employer_amount": "er_amount",
            }
            if source == "earnings":
                bindings.update({"source_hours": "hours", "rate": "base_rate"})
            line_items(m, source, source, bindings)
        m.field("payments", "payments")
        m.warn(
            "totals_unavailable",
            "/",
            "UKG cached pay statement schema has no gross/net totals; not inferred from potentially incomplete lines",
        )
        m.warn(
            "hours_unit_unverified",
            "/earnings",
            "Pay statement hours unit is undocumented; kept as source_hours, not assumed milliseconds",
        )

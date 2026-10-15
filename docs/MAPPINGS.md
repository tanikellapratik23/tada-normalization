# Mapping evidence

Reference pack: [Niwant/tada-ai-normalization-take-home](https://github.com/Niwant/tada-ai-normalization-take-home), pinned at `4034f3347cba0abedb75443e8f782364ad108331`. Original contracts, notices, licenses and audit are retained unchanged in `contracts/` and `docs/REFERENCE_AUDIT.md`. No alternate isolved schema is loaded by the code.

## Source object bindings

The importer takes **individual source objects**, not arbitrary HTTP response wrappers. The `evidence` on each synthetic envelope specifies its exact selected schema. `tada/contracts.py` is the machine-readable binding registry.

| Provider | Entity | Source object / extraction |
| --- | --- | --- |
| PrismHR | company | `ClientMaster`, from `/clientMaster/v1/getClientMaster` |
| PrismHR | employee | `Employee`, from `/employee/v1/getEmployee`; request all permitted employee sections |
| PrismHR | direct_deposit | Each `Employee.directDeposit.achVoucher[]` / `AchVoucher`; supply stable `context.record_id` and `employee_id` |
| PrismHR | deduction | `EmployeeDeductions-Deduction`, deduction setup; not a payroll deduction line |
| PrismHR | payroll_run | `PayrollHistory` |
| PrismHR | paycheck | `PayrollVoucher`; embedded earning, deduction, tax and employer contribution arrays |
| isolved | company | `AOS.PayrollOffice.RestAPI.Models.LegalModel` (legal entity, not parent client) |
| isolved | employee | `EmployeeModel`; optional expansions include organizations, labor, tax, miscellaneous fields |
| isolved | direct_deposit | `EmployeeDirectDepositModel` |
| isolved | deduction | `EmployeePayItemModel`; select deduction pay items upstream, retain tenant calculation parameters |
| isolved | payroll_run | `PayrollRunHistoryModel` |
| isolved | paycheck | `CheckModel`, from legal/employee checks endpoints; no CheckPreview models mixed in |
| UKG Ready | employee | GET `/v2/companies/{cid}/employees/{aid}`, bundle index 106 |
| UKG Ready | direct_deposit | GET `/v2/companies/{cid}/employees/{aid}/direct-deposits`, `deposits[]`, index 137 |
| UKG Ready | deduction | GET `/v2/companies/{cid}/employees/{aid}/deductions/{id}`, index 133; list index 132 is only a summary |
| UKG Ready | payroll_run | GET `/v2/companies/{cid}/payrolls`, `payrolls[]`, index 358 |
| UKG Ready | paycheck | GET `/v2/companies/{cid}/payrolls/{id}/pay-statements/{id}`, index 364; list index 362 omits line details |
| UKG Ready | compensation | GET `/v2/companies/{cid}/compensation/history/{id}`, index 33 |
| UKG Ready | pay_info | GET `/v2/companies/{cid}/employees/{aid}/pay-info`, index 159 |
| UKG Ready | demographics | GET `/v2/companies/{cid}/employees/{aid}/demographics`, index 134 |
| UKG Ready | company | Caller context metadata; no company response contract asserted |

UKG HTML was inspected for endpoint binding and response details. The employee direct-deposit endpoint is deprecated; its cached page specifies `X-End-of-Support-Timeline: 2026-01-29`, pagination (`page`, `size`), 401/403, and 503 rate limiting with `X-CallLimit-TimeToWait`. These materials do **not** establish that the endpoint still works live. XML/opaque schema blocks are not treated as JSON response contracts. This project consumes exported JSON, not a production live connector.

## Semantic decisions with field evidence

| Source field | Canonical meaning | Evidence / constraint |
| --- | --- | --- |
| Prism `Client.statusClass` | active / on_leave / terminated | Schema description A/L/T. `employeeStatus` is a separate tenant-defined code. |
| Prism `Compensation.payMethod` | salary / hourly / commission / driver | S/H/C/D in description. Salary is per pay period; `hourlyPayRate` has its own basis and is preserved as an extension. |
| Prism `AchVoucher.accountType` | checking_or_pay_card / savings / instant_pay | C explicitly combines checking and pay card; no unsupported distinction invented. |
| Prism `AchVoucher.method` | fixed / fixed_skip_if_insufficient / percentage / percentage_of_remainder / remainder | F/FS/P/PN/B. P and PN percentages are kept in percentage points. No priority field is documented. |
| Prism `AchVoucher.status` | prenote / active / inactive | P/D/I. Employee-level ACH status and voucher eligibility remain in the employee source snapshot. |
| Prism `EmployeeDeductions-Deduction.usePercent` | amount versus percentage | Boolean discriminator; retain limit, maximum/basis, schedule, dates, match and arrears settings. |
| Prism `PayrollVoucher.totalEarnings`, `netPay` | gross_pay, net_pay | Reported totals, not recomputed. Negative adjustments retained. |
| Prism `Earning.payAmount` | rate | Description says pay per hour or unit. Never presented as line earnings amount. `hoursWorked` is hours; `hoursUnits` stays units. |
| isolved `sequenceNumber` | priority; 0 means net pay/remainder | Documented special value. Zero is not missing. |
| isolved `percent` | percentage points | Schema minimum 0, maximum 100; mutually exclusive with amount. |
| isolved `calcParams` | preserved calculation parameters | No parameter type dictionary; do not assume paramValue is dollars or percent. |
| isolved `Check*.checkDollars/checkHours` | current paycheck amount/hours | Chosen over current/YTD/MTD fields; the choice is explicit and emits a basis diagnostic because descriptions are sparse. All accumulations retained. |
| isolved `payrollRunNumber` | run sequence only | Not equivalent to `PayrollRunHistoryModel.id`; explicit `context.payroll_run_id` links them. |
| UKG `calc_method.type` | fixed / remainder / percentage_of_gross / percentage_of_net / percentage_of_remainder | FLAT_AMOUNT/FULL/GROSS_EARNING/NET_PAY/DIRECT_DEPOSIT_PER_OF_REMAINDER. |
| UKG `type=RESERVE_LIVE_CHECK` | reserve_live_check | Not represented as a bank direct deposit. |
| UKG `standard_work_day`, compensation `time` | hours = milliseconds / 3,600,000 | Both descriptions explicitly state milliseconds. |
| UKG paycheck `earnings[].hours` | source_hours, units unverified | Integer type alone does not prove milliseconds or hours. No guessed conversion. |
| UKG `ee_amount`, `er_amount` | employee / employer amounts | Preserved separately; employer deductions are benefit contributions, not employee withholding. |
| UKG `ee_calc_method.amount/percent` | unscaled numeric strings plus warning | Cached deduction schema does not document scaling/basis. No cents conversion inferred from integer type. |

The employee mapping registry maps name, contact, addresses, employment dates/status, organization, job and compensation consistently. [EMPLOYEE_FIELD_COVERAGE.md](EMPLOYEE_FIELD_COVERAGE.md) lists the entire reachable employee field inventory, including fields intentionally kept as provider extensions. UKG supplement records link to employees without overwriting the employee profile or discarding compensation history.

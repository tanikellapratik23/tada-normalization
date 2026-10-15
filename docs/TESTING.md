# Verification results

## Offline and local API checks

The automated suite has **48 tests**. It covers:

- All 21 generated source fixtures against their selected provider schemas.
- Canonical envelope/status/financial constraints and every coverage destination.
- Exact decimal parsing, negative adjustments, missing/null/zero/false, invalid dates, unknown enums and tenant status dictionaries.
- Different deposit allocation methods, remaining-balance rules, invalid amount/percent combinations and percentage bounds.
- Employee-scoped identity collisions, transactional foreign keys, rollback, duplicate batches and repeat imports.
- Paycheck amounts versus accumulations; employee versus employer benefits; Prism secondary earnings/deductions/taxes; UKG unit uncertainty.
- Isolved personal contact fields and rejection of earnings mistakenly submitted as deduction setup.
- Local HTTP health, statistics, filters, invalid parameters and missing routes.
- Live-check result sanitization, empty-result handling, HTTP failures, Prism error envelopes and blocking credential-bearing redirects.

Run `python -m unittest discover -s tests -v`. GitHub Actions runs on Python 3.10, 3.12 and 3.13. Fixture regeneration is checked for a clean diff. The source-schema checks do not establish that every optional field or provider business rule is exercised.

The browser explorer was also tested by filtering provider/entity and expanding a paycheck. The local API test uses an actual loopback HTTP server, not only mocked handlers.

## Live demo APIs — October 15, 2026

I used the organizer's sign-in endpoint for all three tenants, then made bounded read-only provider requests. The repeatable checker is `tada/live_check.py`. The machine-readable [result snapshot](LIVE_API_RESULTS.json) contains endpoint templates, HTTP statuses, counts and diagnostic counts only. No credentials or downloaded records are included.

The recorded checker examined **21 endpoint/extraction results**: 15 were `ok`, four were `empty`, and two were `failed` because the documented routes returned 404. It normalized **16 sampled records**, preserving every input field. `records_seen` can be larger than `normalized`: the checker intentionally normalizes at most two records from each response.

| Provider | Verified on returned data | Limits observed |
| --- | --- | --- |
| PrismHR | Company, employee with all documented sections requested, payroll history and a paycheck; all returned 200 | Sample employee deposit/deduction setup lists empty. Some blank/masked values and unknown payroll type codes remained diagnostics; live responses differ from the static schema's nullability. |
| isolved | Company, employee, direct-deposit setup and deduction pay items; all returned 200 | Sample employee check list empty. Documented payrollRunHistory route returned 404. Earlier exploration of the legal-level checks route also returned 404. |
| UKG Ready | Employee detail, pay-info, payroll runs and a detailed paycheck including earnings/deductions/taxes/payments; all returned 200 | Sample direct-deposit list empty. Employee deduction-list route returned 404. The deprecated deposit route still responded in this demo; future support is not assumed. |

Source-schema differences are reported separately from normalization failures. The live data includes nulls and extra properties that conflict with the reference snapshots. These observations do not justify changing the pinned evidence or pretending strict source validation passed. The adapters retained all fields, and mapped invalid/ambiguous values were flagged.

Exploration also verified two operational details: Prism pagination starts at zero, and `getPayrollSummary` cannot use `includeDetails=true` without a batch ID. The checker uses those corrected request shapes. An expired isolved token produced 401; a fresh sign-in restored access. The repeatable CLI signs in afresh on each run.

An empty response proves endpoint access, not that the adapter was exercised on that entity's live data. A 404 is an unresolved live-access gap, not a passing test. Synthetic fixtures cover those entities locally. The checker exits **1** for the recorded run because of the two 404 responses; this is intentional failure reporting, not a hidden successful exit.

## Repeating the live test

Install `.[test]`, set `DEMO_SIGNIN_API_KEY` locally, and run:

```bash
python -m tada.live_check --year 2026 --report local/live-check.json
```

Use `--provider prismhr`, `--provider isolved`, or `--provider ukg-ready` to scope the run. The script does not exhaust pagination, download a complete tenant, create/update provider records, or write tokens and response bodies. Its report includes a UTC timestamp, so live results are intentionally not deterministic and are not part of CI.

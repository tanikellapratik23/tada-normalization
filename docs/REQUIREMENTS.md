# Assignment audit

I checked the implementation against the assignment README at upstream commit `4034f3347cba0abedb75443e8f782364ad108331`, including the employee-completeness requirement and the distinction between mandatory work and optional write-back.

| Requirement | Implementation and evidence | Status / boundary |
| --- | --- | --- |
| Local platform | Python CLI, SQLite persistence, JSON API and browser explorer; README quick start | Implemented and tested from a clean clone |
| PrismHR, isolved, UKG Ready | Explicit adapters and pinned reference bindings | Implemented for all three |
| Company relationships | Provider/tenant/company identity and transactional foreign keys | Implemented; UKG company metadata is caller context because selected reference has no company detail schema |
| Complete employee data | Broad profile/contact/address/employment/job/organization/pay mappings; complete source snapshot, leaf coverage and extension inventory; UKG pay-info/demographics/compensation supplements | All received fields retained. Provider-specific fields without verified equivalent semantics remain explicit extensions, not claimed as shared normalized meanings |
| Direct-deposit setup | Account type, fixed/percentage/remainder methods, priority where documented, status and dates where exposed | Implemented; Prism priority unavailable in selected schema; no money movement |
| Deduction setup | Codes/types, amounts/percentages where interpretable, limits, dates and calculation rules | Implemented; isolved tenant calculation parameters and UKG undocumented units are preserved with diagnostics |
| Deductions in payroll | Paycheck deduction and benefit lines, employee/employer amounts | Implemented; tested separately from setup records |
| Payroll runs/periods/paychecks | Run links, dates, earnings, hours, reported gross/net, employee/employer taxes, deductions and benefits | Implemented; UKG unsupported gross/net totals and undocumented hours units stay absent/unconverted with diagnostics |
| Canonical schemas/enums | `schemas/canonical-v1.schema.json`, provider mappings and status/allocation enums | Implemented; unknown values preserved, no tenant meaning guessed |
| Discover mappings from references | `docs/MAPPINGS.md`, `tada/contracts.py`, full employee inventory | Implemented; isolved primary snapshot only; UKG cached HTML explicitly distinguished from OpenAPI |
| Generate own synthetic data | Seeded generator, 21 checked-in source fixtures, generation manifest | Implemented; deterministic and schema-validated, not copied from live records |
| Tests run locally without credentials | 48 unit/integration tests; multi-version CI | Implemented |
| Optional live discovery | `python -m tada.live_check`; sanitized result snapshot | Performed; empty results and two 404 routes documented, not counted as nonempty retrieval success |
| README with approach/setup | First-person explanation, commands, architecture, API usage, AI assistance | Included |
| Assumptions/decisions/limitations Markdown | `ASSUMPTIONS.md` plus mapping and testing reports | Included |
| Own repository | https://github.com/tanikellapratik23/tada-normalization | Published |
| Keep keys/tokens/live records out of submission | Environment-based live key; sanitized report only; ignored local files | Checked before push |
| Optional provider write-back | Not implemented | Optional extension intentionally omitted |
| Send repository link to organizer by Friday night, October 16 | Repository and documentation are ready to share | Submission email is a separate user action; no email sent by this project |

The scope is a local normalization platform and a live verification tool, not a production payroll integration service. The explicit extension policy, unavailable fields and live endpoint gaps are part of the submitted limitations, not hidden behind a claim of universal API support.

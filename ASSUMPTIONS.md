# Assumptions, decisions, and limitations

## Architecture and scope

Python 3.10+ and SQLite keep local setup small. The runtime has no third-party dependencies; optional `jsonschema` validates fixtures against the supplied evidence. The application is a JSON import/normalization platform with a CLI and a read-only local explorer. A bounded, read-only live API smoke checker is included and was run against all three demo providers. It validates sample records in memory and writes only a sanitized status report. Full live synchronization and provider write-back are not implemented. The API key is supplied through an environment variable for live checks and is not included in this submission. Offline operation needs no credentials.

The implementation was built with AI assistance. Provider mappings were derived from the supplied contracts, then checked with deterministic synthetic fixtures and semantic tests. All test employee names, identifiers and bank information are fictional. Reference-pack illustrative examples are retained unchanged as documentation and are not the test corpus.

## Employee completeness and extension policy

Every received field is preserved, including nested structures, arrays, nulls, unknown future fields and provider-specific details. Common concepts have explicit canonical fields. The full source record and a per-leaf coverage map make loss detectable. Fields without a verified common semantic mapping are retained as JSON Pointer keyed `extensions`; they are **not claimed to be semantically normalized**. This is a deliberate limit: a generic canonical equivalent for every provider-specific tax, benefit, onboarding or custom field would invent meaning. The generated field inventory makes that boundary reviewable.

The selected employee contracts are Prism Employee (including its nested sections), isolved EmployeeModel, and UKG employee detail plus separate pay-info, demographics and compensation detail records. Arbitrary employee subresources such as documents, attendance, all benefits endpoints, and history endpoints outside these contracts are not automatically fetched or interpreted. Upstream callers must request all needed expansions and import the resulting objects. Missing fields mean “not supplied,” not “does not exist in this provider.” Some nested arrays are empty in generated fixtures; schema inventory covers those fields but semantic test coverage is not exhaustive across every optional subresource.

## Identity and relationships

IDs are escaped components: provider, tenant, company/legal entity, entity kind, source ID. For employee-scoped setup/supplement entities, the final component encodes the pair `[employee_id, source_id]`; this prevents identical deduction codes or deposit slots on different employees from colliding. Original source IDs remain unchanged in metadata. During the final audit I fixed this scoping and added regression tests. If using a demo database created before that fix, create a fresh database before re-importing; no migration of the earlier development-only IDs is provided. No cross-provider person merge is attempted using names, email or SSN. For isolved, `tenant_id` should include the parent client identity and `company_id` is the legal entity ID. UKG company scope is the company ID; EIN information is retained. Employee numbers are not primary keys.

Some source objects have no stable ID (notably Prism ACH vouchers and deduction setup). Callers must supply `context.record_id` using a stable tenant-owned identifier, e.g. an integration-maintained slot key. Array order is not a durable identity, and account numbers should not be used as record IDs. Synthetic fixture slot IDs are demo-only. Stable identity across upstream reordering needs an integration identity store.

SQLite imports are atomic, reject duplicate IDs within a batch, and upsert deterministically across repeated imports. Company, employee and paycheck-run references are foreign keys, checked at transaction commit so input ordering is irrelevant. Referenced parents must be included in the batch or already stored. Manager relationships remain informational because managers may be outside an export. Deletes, tombstones, change history, and incremental cursor synchronization are not implemented.

## Money, dates, status and units

Money/rates/percentages use decimal strings. JSON input decimals are parsed with Decimal to avoid floating-point rounding. Integer zeros, false, missing and null remain distinct. No implicit USD default, rounding, cents conversion, tax calculation, annualization or FX conversion is applied. Raw Decimal values serialize as strings in source snapshots to preserve exact decimal digits; this preserves numeric information but not original JSON numeric token types or lexical formatting. The original input file is the byte-level archive.

ISO dates and timestamps are validated without converting time zones or discarding time components. Sentinel dates such as UKG 9999-12-31 remain explicit values. Historical or future dates are not rejected merely based on today's date. Invalid mapped dates/numbers remain in extensions with diagnostics.

Prism firstName's description says “family name,” conflicting with field naming and lastName's surname description. We map firstName to first_name and document this source inconsistency. Prism courtOrderMedical is typed boolean but its description lists string codes; it is preserved without coercion. Strict source schema validation may reject such real-world drift; the normalization CLI does not pretend to repair it.

Tenant-configured codes remain unknown unless an explicit per-import status lookup is supplied. Unknown values retain their source value and emit a diagnostic. Benefit enrollment, company status, employee status and deposit status are separate domains. A payroll history selector “A = All Types” is not accepted as a persisted run type.

Prism C account type does not distinguish checking from pay card. Its ACH record does not document priority. Deposit rules are normalized as configuration, not executed to move money. Conflicting amount/percent inputs and out-of-range percentages generate warnings; no automatic choice silently changes source intent. Parent-level ACH status, voucher eligibility and checksums remain in the complete employee source record and must be consulted for any future execution/write feature.

isolved calcParams require tenant-specific knowledge. The live response contained Deduction, Earning and Memo Calc pay items. The checker selects only Deduction items, and the deduction adapter rejects explicitly different pay-item types. Missing types remain a caller responsibility. Benefit checkEmployeeDeduction and checkEmployerContribution are mapped separately; all-time/current/check amounts are never summed together.

UKG pay statement gross/net totals are absent in the cached selected schema. We leave them absent, since summing incomplete line items or payments could fabricate payroll totals. UKG earnings hours have undocumented units, whereas pay-info standard_work_day and compensation time explicitly use milliseconds. Only documented millisecond fields are converted. Integer deduction amounts do not establish cents units; no scaling is guessed.

## Evidence and validation limits

The bundled contracts are pinned snapshots, not promises about current live APIs. Only isolved's primary v6 artifact is used. UKG is cached HTML plus extracted JSON Schema, not OpenAPI. The cached employee direct-deposit route is deprecated and has an end-of-support header; the demo route returned HTTP 200 during the live check, with an empty list for the sampled employee. This is not a guarantee of future availability. UKG company metadata is supplied explicitly by the caller because this selected bundle has no company detail schema.

The live checks found nullable fields and extra properties that differ from the pinned contracts. Normalization preserves these values and emits diagnostics for ambiguous mapped values, rather than treating reference drift as data loss. The documented isolved payroll-history and UKG employee deduction-list routes returned 404; sampled isolved checks and Prism/UKG deposit or deduction lists were empty. These cases remain covered by synthetic tests but are not claimed as successful nonempty live retrievals. See docs/TESTING.md and docs/LIVE_API_RESULTS.json. An isolved session expired during exploratory testing; signing in again restored employee/company access.

Source validation uses JSON Schema Draft 4 semantics with local references and format checks. OpenAPI/Swagger-specific prose requirements, XML, tenant dictionaries, and opaque blocks are not automatically enforceable. Known schema-valid data can still be semantically inconsistent; diagnostics handle selected cases. Generated fixtures exercise all selected entities, not every possible enum/optional nested field. Schema validation, semantic tests and lossless coverage checks complement each other.

## Local security and production gaps

The dashboard binds to 127.0.0.1 and only exposes GET routes. It shows full imported data to the local user. SQLite/source snapshots are unencrypted and may contain PII if real data is imported; use synthetic data for demonstrations. `local/`, environment files, virtual environments and databases are excluded from Git. This is not a production multi-user service: authentication, encryption, access control, audit retention, upload quotas, live pagination/retry/rate-limit handling, and secrets management would be required before such use.

No email submission is sent by this project. The repository link is the deliverable to send to the organizer.

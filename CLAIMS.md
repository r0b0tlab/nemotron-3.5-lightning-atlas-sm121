# Claims and evidence boundary

Status: FINAL CLAIMS PENDING FINAL REQUALIFICATION

This file must be updated in the same finalization commit as the exact source,
image, benchmark, and evidence manifests. Placeholders are not publishable.

## Claim identity

- Source SHA: `<FINAL_ATLAS_SHA>`
- Source tree: `<FINAL_ATLAS_TREE>`
- Binary SHA-256: `<FINAL_BINARY_SHA256>`
- Image manifest: `<FINAL_IMAGE_MANIFEST>`
- Model manifest: `<FINAL_MODEL_MANIFEST>`
- DSpark manifest: `<FINAL_DSPARK_MANIFEST>`
- Profile hash: `<FINAL_PROFILE_HASH>`
- Harness revision: `<FINAL_HARNESS_SHA>`
- Evidence directory: `<FINAL_EVIDENCE_DIR>`
- Evidence manifest: `<FINAL_EVIDENCE_MANIFEST_SHA>`

## Required final gates

- Exact dedicated Lightning target build.
- Exact-SHA specification PASS.
- Exact-SHA quality/security APPROVED.
- Native kernel admission with zero unresolved required lookups.
- No-spec self-determinism.
- DSpark-on versus no-spec exactness.
- C1/C2/C4/C8 mixed-prompt correctness.
- Repeated early-finish and n-reduction churn with zero corruption/ILA/503.
- Lifecycle, reuse, cancel, timeout, restart, and teardown closure.
- Complete r0b0bench `core-subset` profile with `invalid_for_publish=false`.
- Immutable runtime image and clean-room reproduction.

## Metric boundary

Historical `cd2218e` selected-lane, fixed-engine, and disqualified C32 records are
retained under evidence with their original identities. They are not relabeled as
final claims and are not mixed with the final corrective epoch.

## Publication rule

No public qualified claim is valid until every identity above is populated from
the final immutable run and independently checked from a clean clone/image pull.

# Claims and evidence boundary

Status: NOT_QUALIFIED / FULL_SUITE_INCOMPLETE

The native source/build/runtime and immutable-image gates are closed. The full
claim-bearing r0b0bench `core-subset` report is not claimable because the
official BFCL multi-turn lane stalled after 129/200 rows; its partial raw result
is diagnostic only. No public quality, BFCL, or aggregate throughput claim is
made by this package.

## Claim identity

- Source SHA: `3f9292938e7ee159bfbe3a1afd16e1de3e340b84`
- Source tree: `8b6feef75854c8a88e9b9cb35a1edafe837723ac`
- Binary SHA-256: `1111f86b201a906b427b8305f337bb654c40099df5e3e40b1dac074e05b78195`
- Image manifest: `ghcr.io/r0b0tlab/nemotron-3.5-lightning-atlas-sm121@sha256:d00a317bbe8ada857836c89bde54b75449d2b91086594db7cce1be27683483e4`
- Model manifest: `a14fad4058be6eb1bd2735148a9b94c4c2e069d1fcbf886a60de92deb3cd0a9b`
- DSpark manifest: `edfd1601716ea449ce05ed6f4edb38fa4970f07bfc5b09b52e039b674cb0fa8d`
- Profile hash: `1f96d12a86b2acdde41a5b0b6a713216d8d5d5fbd216c9521c0b5e1ce78a580f`
- Harness revision: `cf9b4de1a83beebe08ea9559655047ab83a4a18d`
- Evidence directory: `5bd1fff-r0b0bench-corrected4` (partial diagnostic; BFCL incomplete)
- Evidence manifest: `NOT_AVAILABLE_FULL_SUITE_INCOMPLETE`

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

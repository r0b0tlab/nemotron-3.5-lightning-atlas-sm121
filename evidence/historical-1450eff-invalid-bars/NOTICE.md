# NOTICE — these numbers are INVALID speed bars

The JSONs in this directory were measured BEFORE the G0 RoPE fix (`e335b00`) on the
corrupted-attention model, where the degenerate Paris probe was more predictable and
inflated DSpark acceptance (and tok/s). Bisect-proven 2026-08-15: `e335b00` "drops"
Paris-256 90.3→79.3 but step time IMPROVED (37.7 vs 41.4 ms) — only acceptance fell.

Affected: the 77.75 frozen no-spec bar and the 89.7/94.6 DSpark A/B at engine
`1450eff`. The fixed-engine reference set (same protocol) is in
`../fixed-engine-20260815/`: no-spec 74.13, DSpark K=3 89.31 (1.20x), essay 72.41.
These files are preserved for provenance only — do not cite them as bars.

# CLAIMS — Nemotron 3.5 Lightning on Atlas (fixed-engine, 2026-08-15)

Rule: every claim names its evidence artifact (SHA-256 in
`evidence/fixed-engine-20260815/MANIFEST.sha256`). Speed bars measured BEFORE the
G0 RoPE fix (`e335b00`) are INVALID (bisect-proven 2026-08-15: the corrupted-attention
model inflated acceptance; see `evidence/historical-1450eff-invalid-bars/NOTICE.md`).

## Engine correctness (G0/G1/G9/G9b, engine e9fc025)

| # | Claim | Evidence |
|---|---|---|
| 1 | No RoPE in Nemotron attention (HF reference has none); distance-decay fixed | bisect + dist sweep 0–512 exact (campaign STATUS.md, G0 section) |
| 2 | Sorted-MoE prefill 64-tile grid fix (silent-partial-compute closed) | GSM8K r0b0-exact 12/12 after fix (campaign STATUS.md, G9) |
| 3 | Marlin MoE prefill opt-in, 2.58k tok/s @44k | gated: canary, GSM8K 12/12, NIAH 2k/12k/44k (campaign STATUS.md, G9b) |
| 4 | Decode-graph 716 class closed (capture guard, replay allowed) | `fcaa1e1` + `e9fc025` |

## DSpark K=3 quality (G5, engine e9fc025, DSpark ON)

| # | Claim | Evidence |
|---|---|---|
| 5 | Canary exact (thinking-off) | campaign STATUS.md G5 |
| 6 | C1 France-2048 DSpark 89.31 vs no-spec 74.13 = 1.20x | `c1-2048-dspark-fixed-gate-a.json`, `c1-2048-nospec-fixed-gate-a.json` |
| 7 | C1 essay-2048 72.41 vs no-spec 71.82 = 1.01x (known C1 wall) | campaign STATUS.md G5 |
| 8 | GSM8K r0b0-exact 12/12 with DSpark ON | campaign STATUS.md G5 |
| 9 | NIAH 12,440 + 44,784 exact with DSpark ON (sorted prefill live) | `niah-12440-dspark-fixed.json`, `niah-44784-dspark-fixed.json` |

## Long context (AR, 1M profile, bs=1)

| # | Claim | Evidence |
|---|---|---|
| 10 | NIAH 300,000 exact (past the 262,144 config RoPE cap) | `niah-300k-ar-1m.json` (1031.6 tok/s prefill) |
| 11 | NIAH 500,000 exact | `niah-500k-ar-1m.json` (735.3 tok/s prefill) |
| 12 | NIAH 749,808 (75% window) exact, vLLM-parity | `niah-750k-ar-1m-r2.json` (586.8 tok/s prefill; r1 = 300s-deadline trap, preserved) |

## C>1 concurrency (DSpark, work in progress — NOT claims yet)

| # | Measurement | Evidence |
|---|---|---|
| 13 | Fixed-engine baseline: C1 85.59 / C2 90.67 / C4 81.95 France-2048 | `phase3-c{1,2,4}-dspark-baseline.json` |
| 14 | Multi-lane propose: accept collapses at n≥2 (lanes=4), lanes=1 healthy | `phase3-c{2,4}-multilane.json`, `ladder-c2-lanes1.json`, `ladder-c2-first.json`, `c4-lossless-lanes{1,4}.json`, PAUSE-STATE.md |
| 15 | DSpark C>1 batched verify diverges from C=1 text (4/4 prompts, near-tie class) — PRE-EXISTING, adjudication open | `c4-lossless-lanes1.json` (serial path, healthy accept [3,2]) |

No C>1 speed claim is made until the multi-lane bug is fixed and the ladder is
quality-re-gated (canary + GSM8K + NIAH 44k + accept hist).

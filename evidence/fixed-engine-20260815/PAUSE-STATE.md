# Atlas Lightning SM121 — Phase 3 pause state (2026-08-15 ~20:0xZ, session paused by user)

HEAD remains **`e9fc025`** (lightning-sm121). Working tree: the multi-lane
propose refactor (8 dflash_head files) + this session's lane fixes, ALL
UNCOMMITTED (nothing is KEEP yet — do not commit without the gates).

## This session's changes (uncommitted, compiled, running binary at pause)

- `DflashProposerState.lane_id` (round-robin at `alloc_state` via new
  `BlockDiffusionDraftHead.next_lane` AtomicUsize) — replaces the broken
  `i % lanes_n` batch-position lane assignment (batch order is not stable;
  captured graphs bake lane scratch pointers).
- `BlockDiffusionDraftHead.lanes_start_event` — recorded on the default
  stream at multi-lane `propose_batch` entry; every extra lane waits on it
  (covers default-stream drafter-ctx precompute / after_verify writes).
- `propose_batch` multi-lane branch: flush-before-reuse per lane (n > lanes
  single-slot pinned readback safety) + collect phase rework.
- `cargo fmt` ran; 4 unrelated files' fmt drift reverted; the 8-file
  refactor set stays formatted (repo fmt baseline already drifts under the
  pinned 1.93.1 rustfmt — CI fmt is not clean at HEAD, do not chase).

## A/B results (both on the SAME binary, only ATLAS_DFLASH_PROPOSE_LANES differs)

| Run | C2 ladder agg | C4 accept (log) | Lossless C4 vs C1 |
|---|---|---|---|
| lanes=1 (serial, pre-refactor path) | ~93.5 (44.3+49.2/req) — matches fixed-engine baseline 90.67 | [3,2],[3,1],[3,2] healthy | **4/4 text mismatch** |
| lanes=4 (multi-lane) | 54.7 (27.35/req) ≈ no-spec | [0,0,0] / [3,0,0,0]-class collapse | 4/4 mismatch; C4 texts differ from lanes=1 C4 texts on 3/4 prompts |

## Findings

1. **BUG (open): multi-lane propose collapses acceptance to 0.** C1 (per-seq
   path, lane 0) is fine (France-2048 87.68 tok/s, canary exact). At n>=2
   the extra-lane seqs draft garbage (prior binary showed accept=[3,0,0,0]
   = lane-0 slot works, extra lanes reject). All stream plumbing verified
   correct (layer kernels take the lane stream; streams are
   CU_STREAM_NON_BLOCKING; markov seed/scratch per lane; entry/done event
   handoff in place). Next debug step: lanes=4 + ATLAS_DFLASH_VERIFY_TRACE=1
   with TWO IDENTICAL prompts on lanes 0 and 1 — identical inputs must give
   bit-identical drafts; a diff localizes the per-lane resource bug.
2. **Pre-existing (NOT the lanes): DSpark C>1 batched verify diverges from
   C=1 text on 4/4 distinct prompts at ~char 12-58** even on the serial
   lanes=1 path with healthy accept [3,2]. G3-class near-tie ULP divergence
   (batched verify_e kernels vs serial GEMV) — but the 4/4 rate is much
   higher than AR's 1/8, so audit verify_e numerics before treating it as
   expected. This FAILS the Phase-3 "C4 text == C1 text" quality gate on
   the fixed engine baseline itself; needs user adjudication.
3. Lanes lever speed target still stands: serial C4 propose ~42ms; ceiling
   after a WORKING multi-lane propose ~15ms (~1.25x tick), Marlin decode
   is the second half of 2.5x.

## Serve state at pause

- Container `atlas-lightning` RUNNING with **ATLAS_DFLASH_PROPOSE_LANES=1**
  (healthy serial config, recreated at 19:34Z; full run command in the
  session log). Do not assume lanes=4 is healthy.
- The vllm0272rc0-wheelbuild container (other session's DSV4 work) was
  running during timing legs — disclose CPU noise on tok/s numbers.
- Evidence: results/phase3-lanes/{c1-france-2048-lanes4.json,
  c4-lossless-lanes1.json, c4-lossless-lanes4.json, ladder-c2-lanes1.json,
  ladder-c2-first.json, c4_lossless.py, ladder.py}.

## Resume

1. Recreate container with lanes=4 + ATLAS_DFLASH_VERIFY_TRACE=1; run the
   identical-prompt draft-diff experiment; localize and fix the extra-lane
   draft bug.
2. Re-gate: canary exact, C1 France-2048 ~85+, lanes=4 C4 texts == lanes=1
   C4 texts, accept hist ≈ serial (~2.4), propose ms ≤15 at C4.
3. Separately: adjudicate the pre-existing C4-vs-C1 near-tie divergence
   (audit verify_e mixed-R numerics; decide the C>1 quality bar).

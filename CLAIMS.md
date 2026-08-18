# CLAIMS — Nemotron 3.5 Lightning on Atlas (WIP)

This repository is a **work-in-progress collaboration package**, not a qualified
release. Current selected-lane metrics are bound to Atlas source
`cd2218ec426a907f681c602feb966611d6db7443` and the checksummed sanitized bundle
under `evidence/nemotron-lightning-cd2218e-20260818/`.

The r0b0bench run used
`--only latency,concurrency,throughput,gsm8k`; it is intentionally
`invalid_for_publish=true` and is not a full public core-subset claim.

## Current selected-lane measurements

| # | Measurement | Result | Evidence |
|---:|---|---:|---|
| 1 | Application start → API ready | 33.853 s | `REPORT.md`, `METRICS.json` |
| 2 | Streaming TTFT, client/server | 375.0 / 315.5 ms | `REPORT.md`, `R0B0BENCH-REPORT.json` |
| 3 | Mean ITL | 19.49 ms | same |
| 4 | C1 aggregate throughput | 84.18 tok/s | same |
| 5 | C2 aggregate throughput | 152.84 tok/s | same |
| 6 | C4 aggregate throughput | **168.42 tok/s** | same |
| 7 | C6 aggregate throughput | 155.84 tok/s | same |
| 8 | C1 2,048-token decode median | 67.78 tok/s | same |
| 9 | Actual 24,541-token prefill wall proxy | 1,697.10 prompt tok/s | same |
| 10 | GSM8K 0-shot flexible extract | **191/200 (95.5%)** | `GSM8K-200-SCORES.json` |
| 11 | Benchmark infrastructure errors | 0 | `R0B0BENCH-REPORT.json` |
| 12 | Health/CUDA/proposal/reset/panic markers | 0 | `METRICS.json`, `SERVER-SANITIZED.log` |

Concurrency used three repetitions per level, discarded the first, and produced
512 output tokens per request. C4 was the highest-throughput tested width; C6
was 7.47% below C4. The prefill harness nominally targeted 14K but produced an
exact server-reported 24,541-token prompt, so the published result is labeled
24.5K rather than 14K.

## Continuous telemetry

- 529 samples over 1,058.57 seconds.
- Actual median interval 2.006 seconds; `docker stats --no-stream` made the
  requested one-second collector blocking.
- GPU utilization median 95%, maximum 96%.
- GPU temperature median 79°C, maximum 84°C.
- Spark unified-memory process median 100,472 MiB, maximum 106,626 MiB.
- Host MemAvailable minimum 5.536 GiB.
- Zero health failures and zero container-not-running samples during traffic.

See `TELEMETRY-SUMMARY.json` for all min/median/mean/p95/max values.

## Current evidence caveats

1. Filtered selected-lane run; not public-suite eligible.
2. No model weights, raw prompts, raw responses, host paths, credentials, PIDs,
   container IDs, addresses, or device pointers are published.
3. `GSM8K-200-SCORES.json` keeps all 200 score/timing/usage records but replaces
   question/response content with SHA-256 hashes.
4. The pinned r0b0bench source assigns `report.json.started_utc` after lane
   execution; treat it as report-finalization time. Telemetry timestamps define
   the actual epoch.
5. Runtime source stays WIP even though all selected lanes passed.

## Historical evidence retained separately

Historical fixed-engine G0/G1/G5/G9/G9b and long-context 300K/500K/749,808-token
records remain under `evidence/fixed-engine-20260815/`. Pre-G0 `1450eff` speed
bars remain invalid and quarantined under
`evidence/historical-1450eff-invalid-bars/`; they are not current baselines.

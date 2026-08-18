# REPRO — Atlas Nemotron 3.5 Lightning DSpark WIP

Target: one NVIDIA GB10 / SM121. Engine: Atlas (`spark`, AGPL-3.0).
No weights are distributed in this repository.

## 1. Build the exact runtime source

```bash
git clone https://github.com/r0b0tlab/atlas.git atlas
cd atlas
git checkout cd2218ec426a907f681c602feb966611d6db7443

ATLAS_TARGET_HW=gb10 \
ATLAS_TARGET_MODEL=nemotron-3.5-lightning-30b-a3b \
ATLAS_TARGET_QUANT=nvfp4 \
CUDARC_CUDA_VERSION=13000 \
  cargo build --release -p spark-server

sha256sum target/release/spark
# benchmarked binary:
# 98affc23b5f41829049a19cf702e402edcda1d7a570443203394090095405fd4
```

The build selector must be `nemotron-3.5-lightning-30b-a3b`. Do not substitute
the Nano selector. The dedicated Lightning target may reuse compatible
hidden-2688 kernels through its registry inheritance, but product identity
remains Lightning.

## 2. Serve the WIP DSpark profile

```bash
export WEIGHTS=/path/to/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4
export DRAFT=/path/to/official-Lightning-DSpark-head
export SPARK=/path/to/atlas/target/release/spark
bash launch_serve.sh
curl -fsS http://127.0.0.1:8888/health
curl -fsS http://127.0.0.1:8888/v1/models
```

The benchmarked profile uses:

- max context 50,016;
- max batch 8;
- max prefill tokens 8,192;
- ModelOpt NVFP4 target;
- FP8 KV with high-precision target attention boundaries;
- DSpark gamma 4 / direct verify K=3;
- SWA window 1,024;
- one proposal lane;
- thinking disabled;
- exact Lightning Mamba projections/persistent recurrence;
- grouped routed-expert path;
- GPU-memory utilization 0.75.

The runtime image manifest used by `launch_serve.sh` is
`avarok/atlas-gb10@sha256:57fb3ffbc2b4d915b6a124117d478b54a257fcf47fa1f93a4f5641ebb75ccce7`.
The observed local image config in the benchmark epoch was
`sha256:542653d59a7a1140c651af1e939866dcd64b5bfe9af964fc1b6f91ce9d1c9b58`;
a config ID is not a portable registry digest.

## 3. Requested selected-lane benchmark

Pinned harness: r0b0bench `1.0.0rc2`.

```bash
export R0B0BENCH_GSM8K_DATA=/path/to/gsm8k/test.jsonl
export R0B0BENCH_CHAT_TEMPLATE_KWARGS='{"thinking":false,"enable_thinking":false}'

r0b0bench run \
  --profile core-subset \
  --only latency,concurrency,throughput,gsm8k \
  --base-url http://127.0.0.1:8888/v1 \
  --model nvidia/nemotron-3.5-lightning-30b-a3b \
  --tokenizer "$WEIGHTS" \
  --output /path/outside/repo \
  --timeout 3600
```

Protocol defaults from the pinned harness:

- latency: 5 streaming reps, first dropped, 128-token ceiling;
- concurrency: C1/C2/C4/C6, 3 reps each, first dropped, 512 output tokens;
- throughput: 5×2,048-token C1 decode plus 3 prefill proxies;
- GSM8K: deterministic 200-row subset, concurrency 2, 512-token ceiling,
  0-shot flexible extraction.

Because `--only` filters the profile, the report must say
`invalid_for_publish=true`. This is expected and must not be removed or
relabelled.

## 4. Verify published evidence

```bash
cd evidence/nemotron-lightning-cd2218e-20260818
sha256sum -c MANIFEST.sha256
```

Published files:

- `REPORT.md` — human-readable full metrics and caveats;
- `METRICS.json` — complete reduced benchmark/server/resource metrics;
- `R0B0BENCH-REPORT.json` — complete selected-lane r0b0bench report;
- `GSM8K-200-SCORES.json` — all 200 score/timing/usage rows with content hashes;
- `TELEMETRY-SUMMARY.json` — full resource statistics;
- `SERVER-SANITIZED.log` — full ANSI-stripped/redacted server log;
- `BENCHMARK-EVENTS.log` — selected-lane execution events;
- `WIP-NOTICE.md` — scope and sanitization boundary.

Prompts, responses, raw host telemetry, credentials, host paths, LAN addresses,
PIDs, container IDs, and device pointers are intentionally excluded.

## 5. Known limitations

- WIP source; not a qualified Atlas release.
- Selected-lane run, not a full public core-subset profile.
- The 24.5K prefill result is an end-to-end wall proxy with 16 output tokens,
  not a kernel-only prefill benchmark.
- C4 was best among tested widths; C6 regressed from C4.
- Historical 1M-context evidence is AR-only; 1M + DSpark is not this profile.

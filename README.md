# Nemotron 3.5 Lightning — Atlas SM121 DSpark

Public **work-in-progress** reproducibility package for serving NVIDIA Nemotron
3.5 Lightning NVFP4 with the official DSpark draft head on one NVIDIA GB10
(SM121) using the Atlas (`spark`) engine.

> **WIP / not a qualified release.** This repository publishes source,
> reproducibility material, sanitized logs, and selected-lane metrics for
> collaboration. It is not a full public r0b0bench core-subset release. Model
> weights are never included.

Authorized users need their own permitted copies of the NVIDIA target and
DSpark checkpoints.

## Status — 2026-08-18

Latest reviewed runtime source:
`cd2218ec426a907f681c602feb966611d6db7443` in
[`r0b0tlab/atlas`](https://github.com/r0b0tlab/atlas).

Exact-SHA specification review passed and quality/security review approved the
runtime source. The post-closeout benchmark intentionally selected only
latency, concurrency, throughput, and GSM8K-200, so r0b0bench correctly marks
it `invalid_for_publish=true`. The selected lanes all passed with zero
infrastructure failures.

## Latest sanitized metrics

| Metric | Result |
|---|---:|
| Startup, application → API ready | 33.853 s |
| Streaming TTFT, client/server | 375.0 / 315.5 ms |
| Mean ITL | 19.49 ms |
| C1 aggregate throughput | 84.18 tok/s |
| C2 aggregate throughput | 152.84 tok/s |
| C4 aggregate throughput | **168.42 tok/s** |
| C6 aggregate throughput | 155.84 tok/s |
| C1 2,048-token decode median | 67.78 tok/s |
| Actual 24,541-token prefill proxy | 1,697.10 prompt tok/s |
| GSM8K-200 | **191/200 (95.5%)** |
| Infrastructure / health / CUDA fault markers | 0 / 0 / 0 |

C4 was the highest-throughput tested width. The concurrency protocol used
three repetitions per width, dropped the first, and generated 512 output tokens
per request. Full methodology, resource distributions, DSpark verify/propose
latencies, acceptance, graph replay, sanitized server log, and checksums:

[`evidence/nemotron-lightning-cd2218e-20260818/`](evidence/nemotron-lightning-cd2218e-20260818/)

The 200-row score ledger omits prompts and responses, retaining per-row scores,
usage metrics, timing, status, and content hashes.

## Pins

| Surface | Value |
|---|---|
| Atlas runtime source | `cd2218ec426a907f681c602feb966611d6db7443` |
| Atlas tree | `f90190176d55b790796b05b097f96fddaf43c78b` |
| Runtime binary SHA-256 | `98affc23b5f41829049a19cf702e402edcda1d7a570443203394090095405fd4` |
| Build target | `gb10 / nemotron-3.5-lightning-30b-a3b / nvfp4` |
| Runtime image manifest | `avarok/atlas-gb10@sha256:57fb3ffbc2b4d915b6a124117d478b54a257fcf47fa1f93a4f5641ebb75ccce7` |
| Observed image config | `sha256:542653d59a7a1140c651af1e939866dcd64b5bfe9af964fc1b6f91ce9d1c9b58` |
| Profile | DSpark gamma 4 / K=3, batch 8, prefill 8192, context 50016, util 0.75 |
| Target weights | NVIDIA Nemotron 3.5 Lightning 30B-A3B ModelOpt NVFP4 |
| Draft weights | Official `Qwen3DSparkModel`, Markov rank 512 |

## Build

```bash
git clone https://github.com/r0b0tlab/atlas.git atlas
cd atlas
git checkout cd2218ec426a907f681c602feb966611d6db7443
ATLAS_TARGET_HW=gb10 \
ATLAS_TARGET_MODEL=nemotron-3.5-lightning-30b-a3b \
ATLAS_TARGET_QUANT=nvfp4 \
CUDARC_CUDA_VERSION=13000 \
  cargo build --release -p spark-server
# binary: target/release/spark
```

The dedicated Lightning target is mandatory. Do not substitute
`nemotron-3-nano-30b-a3b`; Lightning may inherit compatible hidden-2688 kernels
internally, but build and runtime identity remain the Lightning target.

## Serve

```bash
export WEIGHTS=/path/to/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4
export DRAFT=/path/to/official-Lightning-DSpark-head
export SPARK=$PWD/atlas/target/release/spark
bash launch_serve.sh
```

The launch profile is thinking-off and binds gamma 4/direct K=3, one proposal
lane, exact Mamba projection/recurrence, grouped routed experts, FP8 KV with
high-precision attention boundaries, max batch 8, and max context 50,016.

## Evidence policy

- Sanitized logs contain no credentials, host paths, addresses, PIDs, container
  IDs, prompts, responses, or device pointers.
- `METRICS.json` and `R0B0BENCH-REPORT.json` retain complete selected-lane
  metrics and methodology.
- `GSM8K-200-SCORES.json` contains all 200 score/timing/usage records with
  question/response hashes but no question or response content.
- `MANIFEST.sha256` verifies every published evidence file.
- Historical pre-G0 and failed diagnostic evidence remains clearly labeled and
  is not a current performance bar.

See [CLAIMS.md](CLAIMS.md) and [REPRO.md](REPRO.md).

## What this is not

- Not a qualified Atlas release.
- Not a full public r0b0bench profile.
- Not a model-weight distribution.
- Not a vLLM or SGLang restore.
- Not DFlash (`markov_rank=0`); this checkpoint uses DSpark with Markov rank 512.

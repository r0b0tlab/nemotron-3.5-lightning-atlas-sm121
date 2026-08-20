# NVIDIA Nemotron 3.5 Lightning on Atlas — Native DSpark

Reproducible, weights-free package for the native Atlas Rust/CUDA runtime serving
NVIDIA Nemotron 3.5 Lightning NVFP4 with the official Qwen3DSparkModel head on
one NVIDIA GB10/SM121.

Status: PUBLIC REPRODUCIBILITY WIP / NOT QUALIFIED

The native source/build/runtime gates and immutable image are complete. The full
claim-bearing r0b0bench `core-subset` run is not complete: the official BFCL
multi-turn lane stalled after 129/200 rows and was preserved as diagnostic.
This repository therefore publishes the reproducibility suite and exact runtime
identity, but makes no full-suite quality or throughput claim.

## Final identity

| Surface | Value |
|---|---|
| Atlas source SHA | `3f9292938e7ee159bfbe3a1afd16e1de3e340b84` |
| Atlas source tree | `8b6feef75854c8a88e9b9cb35a1edafe837723ac` |
| Binary SHA-256 | `1111f86b201a906b427b8305f337bb654c40099df5e3e40b1dac074e05b78195` |
| Runtime image manifest | `ghcr.io/r0b0tlab/nemotron-3.5-lightning-atlas-sm121@sha256:d00a317bbe8ada857836c89bde54b75449d2b91086594db7cce1be27683483e4` |
| Build target | `gb10 / nemotron-3.5-lightning-30b-a3b / nvfp4` |
| CUDA build family | `CUDARC_CUDA_VERSION=13000` |
| Product | DSpark gamma 4 / direct K=3 |
| Target KV | FP8 with high-precision attention boundaries |
| Drafter KV | BF16 |
| Context profile | 50,016 tokens, batch 8, prefill 8,192 |

The model and DSpark checkpoints are not distributed. Users must obtain
permitted copies from NVIDIA and provide them through read-only mounts.

## What is included

- exact source/build pin and binary verification;
- immutable-image build recipe with embedded binary and template;
- weights-free launch profile;
- full r0b0bench `core-subset` reproduction command;
- canary, lifecycle, churn, restart, and correctness probes;
- sanitized benchmark evidence and raw reduced JSON records;
- checksums, claims, privacy boundary, and third-party notices;
- CI for syntax, manifest, and public-safety checks.

## Quick reproduction

```bash
export IMAGE='ghcr.io/r0b0tlab/nemotron-3.5-lightning-atlas-sm121@sha256:d00a317bbe8ada857836c89bde54b75449d2b91086594db7cce1be27683483e4'
export WEIGHTS=/path/to/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4
export DRAFT=/path/to/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4-DSpark
bash launch_serve.sh
python3 scripts/canary.py http://127.0.0.1:8888/v1/chat/completions
```

See `REPRO.md` for clean build, image, endpoint, benchmark, and evidence
verification. See `CLAIMS.md` for the exact claim boundary.

## AR concurrency profile

The canonical Lightning AR profile enables native Nemotron multi-sequence decode
by default. It shares Mamba in/out projection and MoE weight work across active
sequences while retaining per-sequence recurrent state updates.

- production AR default: batched multi-sequence decode;
- diagnostic serial fallback: `ATLAS_LIGHTNING_DECODE_MULTI=0`;
- component diagnostic overrides: `ATLAS_LIGHTNING_MAMBA_MULTI=0` and
  `ATLAS_LIGHTNING_MOE_MULTI=0`;
- the serial fallback is not an optimization baseline to publish as the default.

The final candidate's diagnostic gate reached 2.62× aggregate decode throughput
at C16 versus C1 with exact mixed-prompt C1/C16 text equality. See the final
campaign evidence before copying a number into a public claim.

## Important limitations

- One GB10/SM121 is the qualified topology.
- No model weights are included.
- Historical diagnostic evidence is retained but is not silently promoted.
- A filtered benchmark run is diagnostic; public claims require the complete
  declared profile with `invalid_for_publish=false`.
- The final image digest and final source SHA must agree with the evidence
  manifest before any release claim is made.

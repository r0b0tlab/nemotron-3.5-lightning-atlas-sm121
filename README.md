# NVIDIA Nemotron 3.5 Lightning on Atlas — Native DSpark

Reproducible, weights-free package for the native Atlas Rust/CUDA runtime serving
NVIDIA Nemotron 3.5 Lightning NVFP4 with the official Qwen3DSparkModel head on
one NVIDIA GB10/SM121.

Status: FINAL RELEASE CANDIDATE — replace all `<FINAL_...>` values during the
same finalization commit; do not publish this tree while placeholders remain.

## Final identity

| Surface | Value |
|---|---|
| Atlas source SHA | `<FINAL_ATLAS_SHA>` |
| Atlas source tree | `<FINAL_ATLAS_TREE>` |
| Binary SHA-256 | `<FINAL_BINARY_SHA256>` |
| Runtime image manifest | `<FINAL_IMAGE_MANIFEST>` |
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
export IMAGE='<FINAL_IMAGE_MANIFEST>'
export WEIGHTS=/path/to/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4
export DRAFT=/path/to/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4-DSpark
bash launch_serve.sh
python3 scripts/canary.py http://127.0.0.1:8888/v1/chat/completions
```

See `REPRO.md` for clean build, image, endpoint, benchmark, and evidence
verification. See `CLAIMS.md` for the exact claim boundary.

## Important limitations

- One GB10/SM121 is the qualified topology.
- No model weights are included.
- Historical diagnostic evidence is retained but is not silently promoted.
- A filtered benchmark run is diagnostic; public claims require the complete
  declared profile with `invalid_for_publish=false`.
- The final image digest and final source SHA must agree with the evidence
  manifest before any release claim is made.

---
license: other
license_name: NVIDIA model license; see upstream checkpoint card
base_model: nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4
tags:
  - nvfp4
  - gb10
  - sm121
  - speculative-decoding
  - dspark
library_name: other
---

# Nemotron 3.5 Lightning — Native Atlas DSpark Runtime

This repository distributes a weights-free native inference runtime and
reproducibility package. It does not distribute NVIDIA model or DSpark weights.
Users must obtain and use their own permitted checkpoint copies.

## Credits and attribution

- NVIDIA — Nemotron 3.5 Lightning model, ModelOpt NVFP4 checkpoint, and official
  DSpark checkpoint.
- NVIDIA — CUDA, GB10/SM121 hardware, and related runtime tooling.
- Avarok-Cybersecurity — Atlas `spark` engine, AGPL-3.0-only.
- DeepSeek AI — DeepSpec/DSpark algorithm and research reference.
- r0b0tlab — native Lightning integration, correctness repairs, benchmarking,
  reproducibility packaging, and evidence publication.
- r0b0bench — MIT benchmark harness and official BFCL integration.

## Runtime identity

- Atlas source: `3f9292938e7ee159bfbe3a1afd16e1de3e340b84`
- Build target: `gb10 / nemotron-3.5-lightning-30b-a3b / nvfp4`
- DSpark: Qwen3DSparkModel, gamma 4, direct K=3, Markov rank 512
- Target KV: FP8 with high-precision attention boundaries
- Drafter KV: BF16

## Limitations

This card is a runtime recipe card, not a weight upload and not a claim that the
runtime supports arbitrary hardware or topologies. See `CLAIMS.md` for exact
qualified metrics and disqualified/diagnostic evidence.

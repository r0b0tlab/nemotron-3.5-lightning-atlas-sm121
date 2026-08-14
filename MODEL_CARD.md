---
license: other
license_name: nvidia-license
base_model: nvidia/Nemotron-3.5-Lightning-30B-A3B
tags:
  - nvfp4
  - speculative-decoding
  - dspark
library_name: other
---

# Nemotron 3.5 Lightning — Atlas SM121 DSpark (recipe card)

This is a **runtime recipe card**, not a weight upload. Get the NVFP4
checkpoint and official DSpark head from NVIDIA. Serve with Atlas SHA
`1450eff` as documented in this repository.

## Credits

- NVIDIA — Nemotron 3.5 Lightning weights and DSpark head
- DeepSeek — DSpark algorithm (arXiv 2607.05147)
- Avarok / Atlas — AGPL-3.0 `spark` engine
- r0b0tlab — SM121 bring-up, kernels, evidence

No weights are distributed from this card.

# Nemotron 3.5 Lightning — Atlas SM121 DSpark

Private reproducibility package for serving NVIDIA Nemotron 3.5 Lightning
NVFP4 with the official DSpark draft head on a single NVIDIA GB10 (SM121)
using the Atlas (`spark`) engine.

This repository does **not** ship model weights. Authorized collaborators
need this private repo, the Atlas source commit below, and their own
permitted copy of the NVIDIA checkpoints.

## Headline (claim-bearing C1)

Frozen no-spec Atlas C1 (Paris / 2048 / ignore_eos / T=0): **77.75 tok/s**.

Atlas DSpark K=3 at engine SHA `1450eff`:

| Gate | Protocol | tok/s | vs 77.75 |
|---|---|---:|---|
| A | Paris 2048 ignore_eos T=0 | **89.73** (confirm **94.60**) | PASS |
| B | hard-prose essay 2048 | **93.91** | PASS |
| Canary | thinking-off chat | exact `The sum of 7 and 5 is 12.` | PASS |
| verify / propose | STEP_TIMING | **27.4 / 9.9 ms** | |

Lossless argmax. Live accept counters present. Not Gumbel.

## Pins

| Surface | Value |
|---|---|
| Engine SHA | `1450efffc08de10035d4f64e74240d78c9712dee` |
| Atlas source (private) | `am423/nemotron-lightning-atlas-sm121` @ that SHA |
| Runtime image | `avarok/atlas-gb10@sha256:57fb3ffbc2b4d915b6a124117d478b54a257fcf47fa1f93a4f5641ebb75ccce7` |
| GHCR (private) | `ghcr.io/r0b0tlab/nemotron-3.5-lightning-atlas-sm121@sha256:02a85b48ab3efd14e15aed10a9ea0c007a3d0ee2695d8721dd93cdce0432d162` |
| `spark` binary sha256 | `a92553f9481bca89c29af3ca1577ef792806ef58ee7baf64e8b8b479aa391e54` |
| Profile | DSpark K=3 (`--dflash-gamma 4`), util 0.75, `max_model_len=50016`, FP8 KV |
| Target weights | NVIDIA Nemotron 3.5 Lightning 30B-A3B NVFP4 |
| Draft weights | official Lightning DSpark head (`Qwen3DSparkModel`, Markov rank 512) |

## Quick start

```bash
# 1. Build spark at the pin (kernel target is nano, not the HF name)
git clone <atlas-source> atlas && cd atlas && git checkout 1450efffc08de10035d4f64e74240d78c9712dee
ATLAS_TARGET_HW=gb10 ATLAS_TARGET_MODEL=nemotron-3-nano-30b-a3b \
  ATLAS_TARGET_QUANT=nvfp4 CUDARC_CUDA_VERSION=13000 \
  cargo build --release -p spark-server

# 2. Point WEIGHTS and DRAFT at your local NVIDIA checkpoints, then:
bash launch_serve.sh

# 3. Canary
python3 scripts/canary.py
```

See `profiles/dspark-k3.yaml` and `recipe/`.

## What this is not

- Not a vLLM or SGLang restore.
- Not DFlash (z-lab, `markov_rank=0`). This checkpoint is **DSpark**.
- Atlas CLI still says `--dflash` — leftover flag name.
- Weights stay with NVIDIA. No HF weight upload from this package.

## License

Packaging in this repo: MIT. Atlas engine: AGPL-3.0-only (see THIRD_PARTY).
NVIDIA checkpoints: NVIDIA license. DSpark algorithm: DeepSeek (arXiv 2607.05147).

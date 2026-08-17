# Nemotron 3.5 Lightning — Atlas SM121 DSpark

Public **work-in-progress** reproducibility package for serving NVIDIA
Nemotron 3.5 Lightning NVFP4 with the official DSpark draft head on a single
NVIDIA GB10 (SM121) using the Atlas (`spark`) engine. It is published for
source visibility and collaboration, not as a qualified release.

This repository does **not** ship model weights. Authorized collaborators need
this repo, the Atlas engine at the pinned SHA (see Pins), and their own
permitted copy of the NVIDIA checkpoints.

## Status (2026-08-17) — WIP / NOT QUALIFIED

Historical fixed-engine gates closed: correctness (G0/G1/G9/G9b), DSpark
re-gate (G5), and 1M long-context (300K/500K/749,808 NIAH exact). The current
engine WIP adds strict startup admission, row/lifecycle contracts, and stable
generation ownership. Open: C>1 batched-verify determinism, multi-lane propose
accept collapse, final ladder, and r0b0bench. Full claim table:
[CLAIMS.md](CLAIMS.md); repro: [REPRO.md](REPRO.md).

## Headline (fixed-engine, engine `e9fc025`, C1, France-2048 ignore_eos T=0)

| Arm | tok/s | vs no-spec |
|---|---:|---|
| no-spec (serial GEMV, sorted prefill, graphs) | 74.13 | 1.00x |
| DSpark K=3 | **89.31** | **1.20x** |

Quality (DSpark ON): canary exact, GSM8K r0b0-exact 12/12, NIAH 12,440/44,784
exact. Long context: NIAH 300K / 500K / 749,808 (75% window) all exact —
vLLM-parity on the same checkpoint. Lossless argmax verify; live accept
counters; not Gumbel.

Prior `1450eff`-era numbers (77.75 frozen / 94.6 A/B) were measured on the
corrupted-attention model BEFORE the G0 RoPE fix and are invalid bars —
preserved for provenance only in `evidence/historical-1450eff-invalid-bars/`.

## Pins

| Surface | Value |
|---|---|
| Engine SHA | `a4fb38bbc9f3de38fb61bc9c715f60a8f0c8a39e` (public WIP fork `github.com/r0b0tlab/atlas`, branch `main`) |
| Engine upstream | `Avarok-Cybersecurity/atlas` (AGPL-3.0) |
| Runtime image | `avarok/atlas-gb10:latest` (digest-pin at final release) |
| GHCR (private, historical) | `ghcr.io/r0b0tlab/nemotron-3.5-lightning-atlas-sm121@sha256:02a85b48…` (1450eff; see evidence/ghcr.json) |
| Profile | DSpark K=3 (`--dflash-gamma 4`), util 0.75, `max-seq-len 50016`, FP8 KV |
| Target weights | NVIDIA Nemotron 3.5 Lightning 30B-A3B NVFP4 (modelopt 0.44.0rc5, MIXED_PRECISION) |
| Draft weights | official Lightning DSpark head (`Qwen3DSparkModel`, Markov rank 512) |

## Quick start

```bash
# 1. Build spark at the pin (kernel target is nano, not the HF name)
git clone https://github.com/r0b0tlab/atlas.git atlas && cd atlas
git checkout a4fb38bbc9f3de38fb61bc9c715f60a8f0c8a39e
ATLAS_TARGET_HW=gb10 ATLAS_TARGET_MODEL=nemotron-3-nano-30b-a3b \
  ATLAS_TARGET_QUANT=nvfp4 CUDARC_CUDA_VERSION=13000 \
  cargo build --release -p spark-server

# 2. Point WEIGHTS and DRAFT at your local NVIDIA checkpoints, then:
bash launch_serve.sh

# 3. Canary
python3 scripts/canary.py
```

See `profiles/`, `REPRO.md`, and `recipe/`.

## What this is not

- Not a vLLM or SGLang restore.
- Not DFlash (z-lab, `markov_rank=0`). This checkpoint is **DSpark**.
- Not a C>1 speed claim yet — the multi-lane propose path is NOT KEEP
  (accept collapse at n≥2; disclosed in CLAIMS.md #14).

# REPRO — build, serve, and gate Atlas Nemotron Lightning

Target: NVIDIA GB10 / SM121, single node. Engine: Atlas (`spark`), AGPL-3.0.
No weights in this repo.

## 1. Engine

```bash
git clone https://github.com/Avarok-Cybersecurity/atlas.git atlas && cd atlas
git fetch origin  # lightning-sm121 fork anchor (see engine/PIN.md of the project root)
git checkout e9fc025   # pinned committed HEAD at time of this package
ATLAS_TARGET_HW=gb10 ATLAS_TARGET_MODEL=nemotron-3-nano-30b-a3b \
  ATLAS_TARGET_QUANT=nvfp4 CUDARC_CUDA_VERSION=13000 \
  cargo build --release -p spark-server
# binary: target/release/spark  (NOT spark-server)
```

Kernel target note: Lightning (hidden 2688) binds the `nemotron-3-nano-30b-a3b`
kernel set. Check the resolved target in the serve log.

## 2. Serve (DSpark K=3, the gated profile)

```bash
bash launch_serve.sh          # see profiles/dspark-k3.yaml for the env + args
# readiness: curl http://127.0.0.1:8888/v1/models (model load ~90-150 s)
python3 scripts/canary.py     # expect exact "The sum of 7 and 5 is 12."
```

Product env: `ATLAS_DISABLE_WATCHDOGS=1 ATLAS_NO_MTP_DRAFTER_CONTEXT=1
ATLAS_DFLASH_OPTION_B=1 ATLAS_DFLASH_PROPOSE_LANES=1` (lanes=1 until the
multi-lane accept bug is fixed — see PAUSE-STATE).

Long-context profile: `--max-seq-len 1000000 --max-batch-size 1
--max-prefill-tokens 8192 --request-timeout 3000` (bs=1 REQUIRED; the default
300 s deadline truncates >300 s prefills).

## 3. Gate protocols (the ones behind the claims)

- Canary: scripts/canary.py, thinking-off chat, exact string.
- C1 France probe: `scripts/atlas_c1_comp.py` (prompt "The capital of France is",
  2048, ignore_eos, T=0) — NOT the Paris essay.
- Ladder: `scripts/ladder.py` (identical France prompts at C=2/4/8; aggregate =
  Σ completion tokens / wall).
- Lossless probe: `scripts/c4_lossless.py` (4 distinct prompts; C=1 alone then
  C=N concurrent; greedy outputs compared).
- GSM8K r0b0-exact: 12-case fixed subset, exact-match, official scorer untouched.
- NIAH r0b0-exact: fixed needle + filler, depths 12,440 / 24,880 / 44,784 at 50k
  profile; 300K / 500K / 749,808 on the 1M profile. Retrieval must be exact.

## 4. Known limitations (disclosed, not silent)

- C>1 batched verify (DSpark) diverges from C=1 text on 4/4 distinct prompts
  (near-tie class, adjudication in progress). C>1 quality claims require the
  adjudicated bar.
- Multi-lane propose (ATLAS_DFLASH_PROPOSE_LANES=4) collapses acceptance at
  n≥2 — NOT a serving profile until fixed.
- 1M + DSpark is an OOM combination; 1M is AR-only.
- Prefill pace degrades with depth (1031 → 587 tok/s from 300K to 750K).

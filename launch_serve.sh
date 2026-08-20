#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
umask 077
: "${IMAGE:?set the exact immutable Atlas runtime image manifest or local tag}"
: "${WEIGHTS:?set the permitted Lightning NVFP4 checkpoint directory}"
: "${DRAFT:?set the permitted official DSpark checkpoint directory}"
NAME="${NAME:-atlas-lightning}"
PORT="${PORT:-8888}"
MODEL="${MODEL:-nvidia/nemotron-3.5-lightning-30b-a3b}"
MAX_SEQ_LEN="${MAX_SEQ_LEN:-50016}"
MAX_BATCH_SIZE="${MAX_BATCH_SIZE:-8}"
MAX_PREFILL_TOKENS="${MAX_PREFILL_TOKENS:-8192}"
GPU_MEMORY_UTILIZATION="${GPU_MEMORY_UTILIZATION:-0.75}"

docker rm -f "$NAME" >/dev/null 2>&1 || true
docker run -d --name "$NAME" --network host --gpus all --ipc=host \
  --shm-size=64g --ulimit memlock=-1:-1 --cap-add=IPC_LOCK \
  -e ATLAS_NO_MTP_DRAFTER_CONTEXT=1 \
  -e ATLAS_DFLASH_OPTION_B=1 \
  -e ATLAS_LIGHTNING_MAMBA_EXACT_BATCHED=1 \
  -e ATLAS_LIGHTNING_MAMBA_BATCH_IN=1 \
  -e ATLAS_LIGHTNING_MAMBA_BATCH_OUT=1 \
  -e ATLAS_LIGHTNING_MAMBA_EXACT_PERSISTENT=1 \
  -e ATLAS_MOE_EXPERT_GROUPED=1 \
  -v "$WEIGHTS:/model:ro" \
  -v "$DRAFT:/draft:ro" \
  "$IMAGE" serve --model-from-path /model --model-name "$MODEL" --port "$PORT" \
    --max-seq-len "$MAX_SEQ_LEN" --max-batch-size "$MAX_BATCH_SIZE" \
    --max-prefill-tokens "$MAX_PREFILL_TOKENS" --dflash --draft-model /draft \
    --dflash-gamma 4 --dflash-window-size 1024 --kv-cache-dtype fp8 \
    --kv-high-precision-layers max --gpu-memory-utilization "$GPU_MEMORY_UTILIZATION" \
    --scheduling-policy slai --tool-call-parser qwen3_coder \
    --default-chat-template-kwargs '{"enable_thinking":false}'

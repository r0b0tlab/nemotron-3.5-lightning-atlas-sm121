#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail

: "${WEIGHTS:?set WEIGHTS to the Lightning NVFP4 checkpoint dir}"
: "${DRAFT:?set DRAFT to the official DSpark head dir}"
SPARK="${SPARK:-$PWD/spark}"
IMAGE="${IMAGE:-avarok/atlas-gb10@sha256:57fb3ffbc2b4d915b6a124117d478b54a257fcf47fa1f93a4f5641ebb75ccce7}"
NAME="${NAME:-atlas-lightning}"
PORT="${PORT:-8888}"
JINJA="${JINJA:-$PWD/jinja/nemotron_lightning.jinja}"

if [[ ! -x "$SPARK" ]]; then
  echo "spark binary not found or not executable: $SPARK" >&2
  exit 2
fi

docker rm -f "$NAME" >/dev/null 2>&1 || true
docker run -d --name "$NAME" --network host --gpus all --ipc=host \
  --shm-size=64g --ulimit memlock=-1:-1 --cap-add=IPC_LOCK \
  -e ATLAS_DISABLE_WATCHDOGS=1 \
  -e ATLAS_NO_MTP_DRAFTER_CONTEXT=1 \
  -e ATLAS_DFLASH_OPTION_B=1 \
  -v "$SPARK:/usr/local/bin/spark:ro" \
  -v "$WEIGHTS:/model:ro" \
  -v "$DRAFT:/draft:ro" \
  -v "$JINJA:/jinja-templates/nemotron_h.jinja:ro" \
  "$IMAGE" \
  serve --model-from-path /model \
    --model-name nvidia/nemotron-3.5-lightning-30b-a3b \
    --port "$PORT" --max-seq-len 50016 --kv-cache-dtype fp8 \
    --kv-high-precision-layers max --gpu-memory-utilization 0.75 \
    --scheduling-policy slai --tool-call-parser qwen3_coder \
    --default-chat-template-kwargs '{"enable_thinking":true}' \
    --dflash --draft-model /draft --dflash-gamma 4 --dflash-window-size 1024

echo "started $NAME on :$PORT (DSpark K=3)"

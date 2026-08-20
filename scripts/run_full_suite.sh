#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
umask 077
: "${BASE_URL:?set BASE_URL, including the /v1 suffix}"
: "${MODEL:?set the served model name}"
: "${TOKENIZER:?set the permitted local tokenizer/model path}"
: "${R0B0BENCH_GSM8K_DATA:?set the permitted local GSM8K JSONL path}"
: "${R0B0BENCH_BFCL_PYTHON:?set the official BFCL Python executable}"
OUT="${OUT:?set an output directory outside this repository}"
[[ "$BASE_URL" == */v1 ]]
[[ "$OUT" != "$PWD"/* ]] || { echo 'benchmark output must be outside the repository' >&2; exit 2; }
mkdir -p "$OUT"
if [[ -z "${R0B0BENCH_CHAT_TEMPLATE_KWARGS:-}" ]]; then
  export R0B0BENCH_CHAT_TEMPLATE_KWARGS='{"thinking":false,"enable_thinking":false}'
else
  export R0B0BENCH_CHAT_TEMPLATE_KWARGS
fi
python3 -c 'import json, os; value = os.environ["R0B0BENCH_CHAT_TEMPLATE_KWARGS"]; parsed = json.loads(value); assert isinstance(parsed, dict), "chat template kwargs must be a JSON object"'
export R0B0BENCH_SERVED_MODEL="$MODEL"
export BFCL_MAX_TOKENS="${BFCL_MAX_TOKENS:-8192}"
export BFCL_HTTP_TIMEOUT="${BFCL_HTTP_TIMEOUT:-3600}"
export BFCL_NUM_THREADS="${BFCL_NUM_THREADS:-4}"
export BFCL_PROJECT_ROOT="$OUT/bfcl-project"
mkdir -p "$BFCL_PROJECT_ROOT"
r0b0bench doctor --base-url "$BASE_URL" --model "$MODEL"
r0b0bench run \
  --profile core-subset \
  --base-url "$BASE_URL" \
  --model "$MODEL" \
  --tokenizer "$TOKENIZER" \
  --output "$OUT/r0b0bench" \
  --timeout "${R0B0BENCH_TIMEOUT:-3600}"

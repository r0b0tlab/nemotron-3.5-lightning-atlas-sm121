#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
umask 077
: "${ATLAS_SHA:?set the exact reviewed Atlas commit}"
ATLAS_REPO="${ATLAS_REPO:-https://github.com/r0b0tlab/atlas.git}"
OUT="${OUT:-$PWD/out/atlas-$ATLAS_SHA}"
if [[ -e "$OUT" ]]; then
  [[ -d "$OUT/.git" ]] || { echo "refusing non-git output: $OUT" >&2; exit 2; }
else
  mkdir -p "$(dirname "$OUT")"
  git clone "$ATLAS_REPO" "$OUT"
fi
git -C "$OUT" fetch --no-tags origin "$ATLAS_SHA"
git -C "$OUT" checkout --detach "$ATLAS_SHA"
[[ -z "$(git -C "$OUT" status --porcelain)" ]]
ATLAS_TARGET_HW=gb10 \
ATLAS_TARGET_MODEL=nemotron-3.5-lightning-30b-a3b \
ATLAS_TARGET_QUANT=nvfp4 \
CUDARC_CUDA_VERSION=13000 \
  cargo --manifest-path "$OUT/Cargo.toml" build --release -p spark-server
sha256sum "$OUT/target/release/spark" | tee "$OUT/target/release/spark.sha256"
printf 'source_sha=%s\nsource_tree=%s\n' "$ATLAS_SHA" "$(git -C "$OUT" rev-parse "${ATLAS_SHA}^{tree}")"

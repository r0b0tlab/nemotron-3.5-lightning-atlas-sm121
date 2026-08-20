#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
umask 077
: "${SPARK:?set the built spark binary}"
: "${BASE_IMAGE:?set the exact parent image manifest}"
: "${SOURCE_SHA:?set the exact Atlas source SHA}"
: "${SOURCE_TREE:?set the exact Atlas tree SHA}"
: "${BINARY_SHA:?set the exact binary SHA-256}"
TAG="${TAG:-atlas-lightning-repro:${SOURCE_SHA:0:12}}"
ROOT=$(cd "$(dirname "$0")/.." && pwd)
TEMPLATE_SHA=$(sha256sum "$ROOT/jinja/nemotron_lightning.jinja" | cut -d' ' -f1)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp "$ROOT/docker/Dockerfile" "$TMP/Dockerfile"
cp "$SPARK" "$TMP/spark"
cp "$ROOT/jinja/nemotron_lightning.jinja" "$TMP/nemotron_lightning.jinja"
docker build --pull=false \
  --build-arg BASE_IMAGE="$BASE_IMAGE" \
  --build-arg SOURCE_SHA="$SOURCE_SHA" \
  --build-arg SOURCE_TREE="$SOURCE_TREE" \
  --build-arg BINARY_SHA="$BINARY_SHA" \
  --build-arg TEMPLATE_SHA="$TEMPLATE_SHA" \
  -t "$TAG" "$TMP"
IMAGE_INFO=$(docker image inspect "$TAG" --format '{{.Id}} {{json .RepoDigests}}')
printf 'tag=%s\ntemplate_sha=%s\nimage_info=%s\n' "$TAG" "$TEMPLATE_SHA" "$IMAGE_INFO"

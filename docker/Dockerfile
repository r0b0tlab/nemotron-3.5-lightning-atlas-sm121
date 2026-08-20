# syntax=docker/dockerfile:1
ARG BASE_IMAGE
FROM ${BASE_IMAGE}
ARG SOURCE_SHA
ARG SOURCE_TREE
ARG BINARY_SHA
ARG TEMPLATE_SHA
COPY spark /usr/local/bin/spark
COPY nemotron_lightning.jinja /jinja-templates/nemotron_h.jinja
COPY nemotron_lightning.jinja /jinja-templates/nemotron_lightning.jinja
RUN test "$(sha256sum /usr/local/bin/spark | cut -d' ' -f1)" = "$BINARY_SHA" \
 && test "$(sha256sum /jinja-templates/nemotron_h.jinja | cut -d' ' -f1)" = "$TEMPLATE_SHA" \
 && test "$(sha256sum /jinja-templates/nemotron_lightning.jinja | cut -d' ' -f1)" = "$TEMPLATE_SHA" \
 && test -s /jinja-templates/nemotron_h.jinja
LABEL org.opencontainers.image.source="https://github.com/r0b0tlab/nemotron-3.5-lightning-atlas-sm121" \
      org.opencontainers.image.revision="$SOURCE_SHA" \
      org.opencontainers.image.description="Native Atlas Nemotron 3.5 Lightning DSpark runtime; weights excluded" \
      org.opencontainers.image.licenses="AGPL-3.0-only" \
      io.r0b0tlab.atlas.source-tree="$SOURCE_TREE" \
      io.r0b0tlab.atlas.binary-sha256="$BINARY_SHA"

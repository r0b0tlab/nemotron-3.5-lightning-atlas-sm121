# Container reproducibility

The final runtime image is built from `recipe/build_image.sh` with:

- an exact parent image manifest digest;
- an exact Atlas source SHA and tree SHA;
- a locally built `spark` binary whose SHA-256 is asserted inside the image;
- the Lightning chat template baked into the image;
- no model weights in the image.

The claim launcher mounts only the permitted target and DSpark checkpoints
read-only. It does not bind-mount a host binary or host source tree.

A local Docker config ID and a registry manifest digest are separate identities.
Both must be recorded; never rewrite one as the other.

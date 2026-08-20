# Reproducible build contract

The build target is the dedicated Lightning identity:

```bash
ATLAS_TARGET_HW=gb10 \
ATLAS_TARGET_MODEL=nemotron-3.5-lightning-30b-a3b \
ATLAS_TARGET_QUANT=nvfp4 \
CUDARC_CUDA_VERSION=13000 \
cargo build --release -p spark-server
```

The Nano selector is not an acceptable substitute. Lightning may reuse
hidden-2688-compatible kernel implementations internally, but source/build/runtime
identity remains `nemotron-3.5-lightning-30b-a3b`.

The final build receipt must record:

- exact source SHA and tree;
- binary SHA-256 and size;
- compiled kernel count and target;
- parent image manifest;
- model and DSpark manifest hashes;
- complete profile/environment/argv hash.

The historical `1450eff` and `cd2218e` values are retained only under evidence
when they are not the final identity.

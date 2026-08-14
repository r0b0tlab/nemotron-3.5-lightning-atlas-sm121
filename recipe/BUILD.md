# Recipe — build and serve

## Build

Kernel target is `nemotron-3-nano-30b-a3b` even though the served name is Lightning.

```
ATLAS_TARGET_HW=gb10 \
ATLAS_TARGET_MODEL=nemotron-3-nano-30b-a3b \
ATLAS_TARGET_QUANT=nvfp4 \
CUDARC_CUDA_VERSION=13000 \
cargo build --release -p spark-server
```

Binary: `target/release/spark`
Expected sha256 at this pin: `a92553f9481bca89c29af3ca1577ef792806ef58ee7baf64e8b8b479aa391e54`

## Serve

See `../launch_serve.sh` and `../profiles/dspark-k3.yaml`.

Readiness: `GET /v1/models` after ~90–150 s. Canary: `python3 ../scripts/canary.py`.

## Winning kernels at this SHA

- `moe_expert_gemv_wide` — W4A16 routed UP, A in smem, 32 N/CTA
- `moe_expert_relu2_down_wide` — relu2+down, 64 N/CTA
- Mamba n<=4 `w8a16_gemv_batch4` — do not pad FP8 GEMM to M=128

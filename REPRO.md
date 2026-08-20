# Full reproducibility procedure

This package is weights-free. Reproduction requires permitted local copies of:

- NVIDIA Nemotron 3.5 Lightning 30B-A3B ModelOpt NVFP4 target weights;
- NVIDIA's official Lightning DSpark checkpoint.

## 1. Build the exact Atlas source

```bash
export ATLAS_SHA=3f9292938e7ee159bfbe3a1afd16e1de3e340b84
export ATLAS_REPO=https://github.com/r0b0tlab/atlas.git
export OUT=/tmp/atlas-build-$ATLAS_SHA
bash scripts/build_engine.sh
```

The script checks out the exact SHA, requires a clean tree, builds the dedicated
Lightning target, and prints the binary hash. Do not substitute the Nano target.

## 2. Build the immutable runtime image

```bash
export SPARK=$OUT/target/release/spark
export BASE_IMAGE=avarok/atlas-gb10@sha256:57fb3ffbc2b4d915b6a124117d478b54a257fcf47fa1f93a4f5641ebb75ccce7
export SOURCE_SHA=$ATLAS_SHA
export SOURCE_TREE=8b6feef75854c8a88e9b9cb35a1edafe837723ac
export BINARY_SHA=1111f86b201a906b427b8305f337bb654c40099df5e3e40b1dac074e05b78195
export TAG=atlas-lightning-repro:${ATLAS_SHA:0:12}
bash recipe/build_image.sh
```

The Dockerfile embeds the binary and Lightning template. Weights remain outside
the image. Record the local image config ID separately from any registry
manifest digest.

## 3. Serve

```bash
export IMAGE=$TAG
export WEIGHTS=/path/to/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4
export DRAFT=/path/to/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4-DSpark
bash launch_serve.sh
```

The product profile is fixed:

- `--dflash --dflash-gamma 4` (DSpark K=3);
- Option B paged drafter context;
- one proposal lane;
- FP8 target KV, BF16 drafter KV;
- `--max-seq-len 50016`;
- `--max-batch-size 8`;
- `--max-prefill-tokens 8192`;
- `--gpu-memory-utilization 0.75`;
- thinking disabled explicitly;
- production watchdogs enabled.

## 4. Verify endpoint identity

```bash
r0b0bench doctor \
  --base-url http://127.0.0.1:8888/v1 \
  --model nvidia/nemotron-3.5-lightning-30b-a3b
python3 scripts/canary.py http://127.0.0.1:8888/v1/chat/completions
```

Require the expected model name, selected Lightning kernel target, active DSpark
proposer, no unresolved required kernels, and exact arithmetic output.

## 5. Run the full reproducibility suite

The output directory must be outside this repository:

```bash
export BASE_URL=http://127.0.0.1:8888/v1
export MODEL=nvidia/nemotron-3.5-lightning-30b-a3b
export TOKENIZER=$WEIGHTS
export R0B0BENCH_GSM8K_DATA=/path/to/gsm8k/test.jsonl
export R0B0BENCH_BFCL_PYTHON=/path/to/official-bfcl-python
export OUT=/tmp/nemotron-lightning-r0b0bench-$ATLAS_SHA
export R0B0BENCH_CHAT_TEMPLATE_KWARGS='{"thinking":false,"enable_thinking":false}'
bash scripts/run_full_suite.sh
```

This invokes the complete pinned `core-subset` profile without `--only` and
without `--skip-systems`. The run must produce a report with
`invalid_for_publish=false`, complete systems lanes, complete quality lanes,
zero infrastructure failures, and exact source/image/model/profile identity.

## 6. Verify evidence

```bash
sha256sum -c evidence/final-3f92929/MANIFEST.sha256
python3 scripts/public_safety_scan.py .
```

Prompts, responses, credentials, local paths, host identifiers, PIDs, container
IDs, model weights, and raw private telemetry are not published. Quality rows
retain scores, status, timing, usage, and content hashes only.

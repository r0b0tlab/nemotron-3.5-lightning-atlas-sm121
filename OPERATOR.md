# Operator contract

## Production profile

- Native Atlas `spark` image with embedded binary;
- one GB10/SM121;
- dedicated Lightning target;
- DSpark gamma 4 / K=3;
- Option B;
- target FP8 KV and drafter BF16 KV;
- max context 50,016;
- max batch 8;
- prefill cap 8,192;
- util 0.75;
- watchdogs enabled;
- native AR multi-sequence decode enabled by default;
- `ATLAS_LIGHTNING_DECODE_MULTI=0` is diagnostic only and is not the production
  AR profile.

## Required admission

1. No competing GPU process.
2. `/v1/models` returns the expected served model.
3. `/health` is ready.
4. Canary returns the exact expected arithmetic answer.
5. Container binary hash matches the final manifest.
6. Logs show the dedicated Lightning kernel target and active DSpark proposer.
7. No unresolved required kernel lookup or fallback marker.
8. Restart and rerun the canary before benchmark traffic.

## Do not do

- do not use the Nano build selector;
- do not mount a host binary or source tree for claim traffic;
- do not enable `ATLAS_DISABLE_WATCHDOGS` in the production profile;
- do not disable DSpark at higher widths to hide scaling problems;
- do not publish filtered benchmark rows as a full profile;
- do not publish model weights.

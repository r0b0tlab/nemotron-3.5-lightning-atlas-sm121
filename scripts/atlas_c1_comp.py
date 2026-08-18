#!/usr/bin/env python3
"""Official Lightning C=1 completions probe. Prompt is France, not Paris essay."""
import json, time, urllib.request, sys
from datetime import datetime, timezone
from pathlib import Path

out = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/c1.json")
n = int(sys.argv[2]) if len(sys.argv) > 2 else 256
payload = {
    "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
    "prompt": "The capital of France is",
    "max_tokens": n,
    "temperature": 0,
    "ignore_eos": True,
}
req = urllib.request.Request(
    "http://127.0.0.1:8888/v1/completions",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
)
t0 = time.perf_counter()
with urllib.request.urlopen(req, timeout=600) as r:
    body = json.loads(r.read().decode())
elapsed = time.perf_counter() - t0
u = body.get("usage") or {}
comp = u.get("completion_tokens") or 0
text = ((body.get("choices") or [{}])[0].get("text") or "")
# Text gate: "The capital of France is" MUST complete to Paris. A token-count
# alone rubber-stamps a corrupted engine (2026-08-17: an all-attention
# mis-dispatch emitted degenerate tokens at 602 tok/s and this probe still
# said PASS). The knowledge prefix is checked BEFORE any throughput is
# reported, so a broken model can never produce a passing record.
expected_prefix = "Paris"
text_ok = text.lstrip().startswith(expected_prefix)
rec = {
    "ts": datetime.now(timezone.utc).isoformat(),
    "label": "atlas-lightning-c1-completions",
    "completion_tokens": comp,
    "elapsed_s": round(elapsed, 3),
    "decode_tok_s": round(comp / elapsed, 2) if elapsed else 0,
    "finish": (body.get("choices") or [{}])[0].get("finish_reason"),
    "preview": text[:160],
    "text_ok": text_ok,
    "verdict": "PASS" if (text_ok and comp >= int(n * 0.9)) else "FAIL",
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(rec, indent=2) + "\n")
print(json.dumps(rec, indent=2))

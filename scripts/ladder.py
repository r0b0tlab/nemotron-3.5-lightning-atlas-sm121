#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""France-2048 concurrency ladder: C=2/4/8 identical France prompts.

Per-width aggregate tok/s (sum of completions / wall) is the ladder metric.
"""
import json
import sys
import threading
import time
import urllib.request

URL = "http://127.0.0.1:8888/v1/completions"
MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"
MAX_TOKENS = 2048
PROMPT = "The capital of France is"


def run_width(width: int) -> dict:
    results = [None] * width
    t0 = time.perf_counter()

    def worker(i):
        payload = {
            "model": MODEL,
            "prompt": PROMPT,
            "max_tokens": MAX_TOKENS,
            "temperature": 0,
            "ignore_eos": True,
        }
        req = urllib.request.Request(
            URL, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        t_start = time.perf_counter()
        with urllib.request.urlopen(req, timeout=900) as r:
            body = json.loads(r.read().decode())
        elapsed = time.perf_counter() - t_start
        comp = (body.get("usage") or {}).get("completion_tokens") or 0
        text = (body.get("choices") or [{}])[0].get("text") or ""
        # Text gate: France must complete to Paris on EVERY request. A
        # token-count-only ladder cannot tell throughput on a correct
        # engine from throughput on a corrupted one.
        text_ok = text.lstrip().startswith("Paris")
        results[i] = {"elapsed_s": elapsed, "comp": comp,
                      "tok_s": round(comp / elapsed, 2) if elapsed else 0,
                      "preview": text[:80], "text_ok": text_ok}

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(width)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    wall = time.perf_counter() - t0
    tot = sum(r["comp"] for r in results)
    all_text_ok = all(r["text_ok"] for r in results)
    return {
        "width": width,
        "wall_s": round(wall, 3),
        "aggregate_tok_s": round(tot / wall, 2) if wall else 0,
        "text_ok": all_text_ok,
        "per_request": results,
    }


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ladder.json"
    widths = [int(w) for w in (sys.argv[2].split(",") if len(sys.argv) > 2 else ["2", "4", "8"])]
    rows = []
    for w in widths:
        print(f"C={w} ...", flush=True)
        rows.append(run_width(w))
        print(json.dumps(rows[-1], indent=2), flush=True)
    rec = {"prompt": PROMPT, "max_tokens": MAX_TOKENS, "ladder": rows}
    with open(out_path, "w") as f:
        json.dump(rec, f, indent=2)
    print("saved", out_path)


if __name__ == "__main__":
    main()

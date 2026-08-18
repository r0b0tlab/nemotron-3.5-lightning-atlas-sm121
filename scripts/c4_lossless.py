#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DSpark losslessness probe: N distinct prompts, C=1 alone then C=N concurrent.

Speculative decoding is lossless: greedy C=N output must equal C=1 output for
every prompt. Distinct prompts (NOT the Paris loop) per the atlas skill.
"""
import json
import sys
import threading
import time
import urllib.request

URL = "http://127.0.0.1:8888/v1/completions"
MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"
MAX_TOKENS = 128

# (prompt, required text prefix) — the prefix is the CONTENT gate: a
# corrupted engine (e.g. the 2026-08-17 all-attention mis-dispatch) can
# emit matching garbage at C=1 and C=N and pass a pure equality check,
# so every prompt also has a known-good completion prefix.
PROMPTS = [
    ("Write the first twelve prime numbers in order:", "2, 3, 5, 7"),
    ("The chemical formula for table salt is", "NaCl"),
    ("A haiku about winter:\n", ""),
    ("def quicksort(arr):\n    # sort a list in place\n", ""),
]


def complete(prompt: str) -> tuple[str, float, int]:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "max_tokens": MAX_TOKENS,
        "temperature": 0,
        "ignore_eos": True,
    }
    req = urllib.request.Request(
        URL, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=600) as r:
        body = json.loads(r.read().decode())
    elapsed = time.perf_counter() - t0
    text = (body.get("choices") or [{}])[0].get("text") or ""
    comp = (body.get("usage") or {}).get("completion_tokens") or 0
    return text, elapsed, comp


def run_serial(prompts):
    out = []
    for p in prompts:
        text, elapsed, comp = complete(p)
        out.append({"prompt": p, "text": text, "elapsed_s": elapsed,
                    "tok_s": round(comp / elapsed, 2) if elapsed else 0, "comp": comp})
    return out


def run_concurrent(prompts):
    results = [None] * len(prompts)
    t0 = time.perf_counter()

    def worker(i, p):
        text, elapsed, comp = complete(p)
        results[i] = {"prompt": p, "text": text, "elapsed_s": elapsed,
                      "tok_s": round(comp / elapsed, 2) if elapsed else 0, "comp": comp}

    threads = [threading.Thread(target=worker, args=(i, p))
               for i, p in enumerate(prompts)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    wall = time.perf_counter() - t0
    return results, wall


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    out_path = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/{label}.json"

    serial = run_serial([p for p, _ in PROMPTS])
    conc, wall = run_concurrent([p for p, _ in PROMPTS])

    mismatches = 0
    for i, (s, c) in enumerate(zip(serial, conc)):
        if s["text"] != c["text"]:
            mismatches += 1
            print(f"MISMATCH prompt {i}: C1[{s['text'][:60]!r}] != "
                  f"C{len(PROMPTS)}[{c['text'][:60]!r}]")

    # Content gate: checked prompts must carry their known-good prefix in
    # BOTH the C=1 baseline and the C=N run. Equality of two corrupted
    # completions is not a pass.
    content_ok = True
    for i, (_, prefix) in enumerate(PROMPTS):
        if not prefix:
            continue
        for run in (serial[i], conc[i]):
            if not run["text"].lstrip().startswith(prefix):
                content_ok = False
                print(f"CONTENT FAIL prompt {i}: expected prefix {prefix!r}, "
                      f"got {run['text'][:60]!r}")

    tot_tokens = sum(c["comp"] for c in conc)
    rec = {
        "label": label,
        "prompts": len(PROMPTS),
        "max_tokens": MAX_TOKENS,
        "serial": [{"tok_s": s["tok_s"], "text": s["text"]} for s in serial],
        "concurrent": [{"tok_s": c["tok_s"], "text": c["text"],
                        "elapsed_s": round(c["elapsed_s"], 3)} for c in conc],
        "wall_s": round(wall, 3),
        "aggregate_tok_s": round(tot_tokens / wall, 2) if wall else 0,
        "lossless": mismatches == 0 and content_ok,
        "content_ok": content_ok,
        "mismatches": mismatches,
    }
    with open(out_path, "w") as f:
        json.dump(rec, f, indent=2)
    print(json.dumps(rec, indent=2))


if __name__ == "__main__":
    main()

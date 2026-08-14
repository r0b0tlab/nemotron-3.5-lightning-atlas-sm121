#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
import json, sys, urllib.request

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8888/v1/chat/completions"
body = {
    "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
    "messages": [
        {
            "role": "user",
            "content": "What is the sum of 7 and 5? Reply with: The sum of 7 and 5 is N.",
        }
    ],
    "max_tokens": 64,
    "temperature": 0,
    "chat_template_kwargs": {"enable_thinking": False},
}
req = urllib.request.Request(
    URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req, timeout=180) as r:
    text = json.loads(r.read())["choices"][0]["message"].get("content") or ""
print(text)
if text.strip() != "The sum of 7 and 5 is 12.":
    sys.exit(1)

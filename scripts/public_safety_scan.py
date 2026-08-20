#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
private_path = re.compile(r"/(?:home|workspace)/(?:r0b0tdgx|[A-Za-z0-9_.-]{2,})(?:/|$)")
secret = re.compile(r"(?:Bearer\s+[A-Za-z0-9._-]{20,}|(?:ghp_|github_pat_|sk-)[A-Za-z0-9_\-]{12,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:api[_-]?key|password|secret)\s*[:=]\s*[A-Za-z0-9_\-]{12,})", re.I)
weight_suffixes = {".safetensors", ".pt", ".pth", ".bin", ".ckpt", ".onnx"}
errors = []
for path in root.rglob("*"):
    if ".git" in path.parts or "__pycache__" in path.parts:
        continue
    if path.is_symlink():
        errors.append(f"symlink: {path.relative_to(root)}")
        continue
    if path.is_file():
        rel = path.relative_to(root)
        if path.suffix.lower() in weight_suffixes:
            errors.append(f"weight/binary suffix: {rel}")
        data = path.read_bytes()
        if b"\0" in data:
            errors.append(f"NUL byte: {rel}")
        if path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".sh", ".py", ".toml"}:
            text = data.decode("utf-8", "replace")
            if private_path.search(text) or secret.search(text):
                errors.append(f"private/credential pattern: {rel}")
if errors:
    print("PUBLIC_SAFETY_FAIL")
    print("\n".join(errors))
    raise SystemExit(1)
print(f"PUBLIC_SAFETY_PASS files_root={root}")

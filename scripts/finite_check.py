#!/usr/bin/env python3
"""Scan a private PyTorch or safetensors checkpoint without exposing its path."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check checkpoint tensors for NaN/Inf")
    parser.add_argument("checkpoint", type=Path, help="Private checkpoint path")
    args = parser.parse_args()

    path = args.checkpoint
    if not path.exists():
        raise SystemExit("checkpoint does not exist")

    tensors = {}
    if path.suffix == ".safetensors":
        from safetensors.torch import load_file

        tensors = load_file(str(path), device="cpu")
    elif path.suffix in {".pt", ".pth", ".bin"}:
        import torch

        payload = torch.load(path, map_location="cpu", weights_only=False)
        tensors = payload if isinstance(payload, dict) else {"payload": payload}
    else:
        raise SystemExit("expected .safetensors, .pt, .pth, or .bin")

    checked = 0
    non_finite = []
    for name, value in tensors.items():
        try:
            import torch

            if torch.is_tensor(value) and (value.is_floating_point() or value.is_complex()):
                checked += 1
                if not bool(torch.isfinite(value).all()):
                    non_finite.append(name)
        except Exception:
            continue

    result = {"status": "ok" if not non_finite else "non_finite", "tensors_checked": checked, "bad_tensors": non_finite}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not non_finite else 2


if __name__ == "__main__":
    raise SystemExit(main())

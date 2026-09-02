#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
import json
import os
import platform
import sys

result = {
    "python": sys.executable,
    "python_version": platform.python_version(),
    "platform": platform.platform(),
    "cwd": os.getcwd(),
    "torch": None,
    "hip": None,
    "gpu_available": False,
    "gpu_name": None,
}

try:
    import torch
    result["torch"] = torch.__version__
    result["hip"] = getattr(torch.version, "hip", None)
    result["gpu_available"] = bool(torch.cuda.is_available())
    if result["gpu_available"]:
        result["gpu_name"] = torch.cuda.get_device_name(0)
except Exception as exc:
    result["torch_error"] = f"{type(exc).__name__}: {exc}"

print(json.dumps(result, ensure_ascii=False, indent=2))
PY

"""Provenance records written next to every output: what produced it, from which source, on what machine."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

from .config import ROOT

SOURCE_DIRS = ("c4n", "engine", "scripts", "configs")


def source_hash() -> str:
    """sha256 over every source file (path + bytes), independent of git state."""
    h = hashlib.sha256()
    for d in SOURCE_DIRS:
        for p in sorted((ROOT / d).rglob("*")):
            if p.is_file() and p.suffix in {".py", ".c", ".h", ".yaml", ".sh", ".js"} and "__pycache__" not in p.parts:
                h.update(str(p.relative_to(ROOT)).encode()); h.update(p.read_bytes())
    return h.hexdigest()


def file_sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _cmd(args):
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        return None


def environment() -> dict:
    env = {"python": sys.version.split()[0], "platform": platform.platform(), "machine": platform.machine(),
           "cc": (_cmd(["cc", "--version"]) or "").splitlines()[:1]}
    try:
        import numpy, torch
        env["numpy"] = numpy.__version__
        env["torch"] = torch.__version__
        env["cuda"] = torch.version.cuda
        if torch.cuda.is_available():
            env["gpu"] = torch.cuda.get_device_name(0)
        elif torch.backends.mps.is_available():
            env["gpu"] = "Apple MPS"
    except ImportError:
        pass
    env["git_commit"] = _cmd(["git", "-C", str(ROOT), "rev-parse", "HEAD"])
    return env


def write(output: Path, cfg: dict, extra: dict | None = None, hash_output: bool = True) -> Path:
    """Write <output>.meta.json describing how `output` was produced."""
    output = Path(output)
    meta = {"output": str(output.relative_to(ROOT)) if output.is_relative_to(ROOT) else str(output),
            "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "command": " ".join(sys.argv), "source_sha256": source_hash(), "config": cfg, "environment": environment()}
    if hash_output and output.is_file():
        meta["output_sha256"] = file_sha256(output)
    meta.update(extra or {})
    path = output.with_name(output.name + ".meta.json")
    path.write_text(json.dumps(meta, indent=1, default=str))
    return path

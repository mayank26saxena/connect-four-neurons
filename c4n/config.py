from pathlib import Path

import os

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(name: str | None = None) -> dict:
    """Load configs/<name>.yaml; the default comes from $C4N_CONFIG (falls back to "base")."""
    name = name or os.environ.get("C4N_CONFIG", "base")
    with open(ROOT / "configs" / f"{name}.yaml") as f:
        return yaml.safe_load(f)


def results_dir(cfg: dict) -> Path:
    """Where a run writes its result files: configs may set `results_dir` (default results/)."""
    d = ROOT / cfg.get("results_dir", "results")
    d.mkdir(parents=True, exist_ok=True)
    return d

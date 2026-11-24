"""Test B, step 2 (PLAN.md addendum (s), S7): build the physically blinded bundle for the describing agents.
The bundle holds only what the (r) protocol's tools need: the model export, the dev split, the Board/tool code, the protocol doc,
and the ns3/ workspace (units, stats, the neuron-vs-random key, the dev cache, the prompt). It does NOT hold docs/PLAN.md,
docs/LOG.md, results/ (the circuit and the membership file), ns/, ns2/, the validation split, or any circuit / tactic code, so an
agent cannot learn which units belong to the circuit or that a blocking study exists. Writes build/ns3_bundle.tgz and
ns3/BUNDLE_FILES.txt (path + sha256 of every file shipped)."""
import hashlib
import re
import shutil
import tarfile
from pathlib import Path

from c4n import config

ROOT = config.ROOT
NAME = "connect4-neurons-s"
FILES = ["pyproject.toml", "uv.lock", ".python-version", "c4n/config.py", "c4n/engine.py", "c4n/model.py", "c4n/ns.py",
         "engine/c4.c", "engine/c4.h", "scripts/31_ns_tool.py", "configs/ns3.yaml", "docs/NEURON_SCIENTIST.md",
         "data/analysis.npz", "web/model.json", "web/model.bin",
         "ns3/units.json", "ns3/stats.json", "ns3/private/key.json", "ns3/cache/dev_acts.npy",
         "ns3/prompts/unit_prompt_s.txt", "ns3/ORCHESTRATOR.md"]
FORBIDDEN = ["docs/PLAN.md", "docs/LOG.md", "results", "ns/", "ns2/", "data/val.npz", "c4n/circuit.py", "c4n/tactics.py"]


def prompt_s():
    """The (r) unit prompt with the workspace renamed ns2 -> ns3 and the repository path left as {REPO}; nothing else changed."""
    p = (ROOT / "ns2" / "prompts" / "unit_prompt_r.txt").read_text()
    p = re.sub(r"/Users/[^/\s]+/c4n-run/connect4-neurons-main", "{REPO}", p)  # (r) ran in a checkout elsewhere; its path was redacted to {REPO} before release
    p = p.replace("Never open `ns/` (an earlier study), `ns2/superseded/` or `ns2/descriptions/` (other than through the `submit` command).",
                  "Never open `ns3/descriptions/` (other than through the `submit` command).")
    p = p.replace("Never open anything in `ns/` or `ns2/private/`, `ns2/cache/`", "Never open anything in `ns3/private/`, `ns3/cache/`")
    p = p.replace("ns2", "ns3")
    return p


LEAK_WORDS = ("circuit", "decoy", "membership", "block_circuit")


def clean_config():
    """configs/ns3.yaml without the lines that only the preparation step reads (they name the study's design)."""
    keep = []
    for line in (ROOT / "configs" / "ns3.yaml").read_text().splitlines():
        low = line.lower()
        if low.lstrip().startswith(("n_circuit", "n_decoys", "stat_games")):
            continue
        if line.startswith("neuron_scientist:"):
            line = "neuron_scientist:"
        keep.append(line.split("#")[0].rstrip() if any(w in low for w in LEAK_WORDS) else line)
    return "\n".join(keep) + "\n"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    (ROOT / "ns3" / "prompts").mkdir(parents=True, exist_ok=True)
    (ROOT / "ns3" / "prompts" / "unit_prompt_s.txt").write_text(prompt_s())
    files = [f for f in FILES if (ROOT / f).exists()]
    missing = sorted(set(FILES) - set(files) - {".python-version", "engine/c4.h"})
    assert not missing, f"missing: {missing}"
    for f in files:
        assert not any(f == x or f.startswith(x) for x in FORBIDDEN), f
    out = ROOT / "build" / "ns3_bundle"
    shutil.rmtree(out, ignore_errors=True)
    for f in files:
        (out / NAME / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / f, out / NAME / f)
    (out / NAME / "configs" / "ns3.yaml").write_text(clean_config())
    for f in files:  # nothing shipped may name the design
        if not f.endswith((".bin", ".npz", ".npy", ".lock")):
            low = (out / NAME / f).read_text().lower()
            assert not any(w in low for w in LEAK_WORDS), (f, [w for w in LEAK_WORDS if w in low])
    text = "".join(f"{sha(out / NAME / f)}  {f}\n" for f in files)
    (ROOT / "ns3" / "BUNDLE_FILES.txt").write_text(text)
    shutil.copy2(ROOT / "ns3" / "BUNDLE_FILES.txt", out / NAME / "ns3" / "BUNDLE_FILES.txt")
    tgz = ROOT / "build" / "ns3_bundle.tgz"
    with tarfile.open(tgz, "w:gz") as t:
        t.add(out / NAME, arcname=NAME)
    print(f"{len(files)} files -> {tgz} ({tgz.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()

"""Write MANIFEST.sha256: hashes of every data file, checkpoint, result and web export (tracked or not)."""
from c4n import config
from c4n.provenance import file_sha256

DIRS = ("data", "checkpoints", "results", "web")


def main():
    lines = []
    for d in DIRS:
        root = config.ROOT / d
        if root.exists():
            for p in sorted(root.rglob("*")):
                if p.is_file() and not p.name.endswith(".meta.json"):
                    lines.append(f"{file_sha256(p)}  {p.relative_to(config.ROOT)}")
    (config.ROOT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
    print(f"{len(lines)} files")


if __name__ == "__main__":
    main()

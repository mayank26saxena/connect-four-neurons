"""Assemble the blog post, its interactive demo and the neuron atlas into one self-contained folder for the site publisher.

The research pages live side by side under docs/blog/ (post/, post/demo/, neuron-atlas/, vertical/, demo/, atlas/data/) and refer
to each other with ../ paths. The site publisher (mayank26saxena.github.io/bin/publish_post.py) needs one folder whose pages only
refer to files inside it. This script copies what the three pages load into build/publish_post/ and rewrites their paths:

  index.html            the post                         (docs/blog/post/index.html)
  demo/index.html       the interactive demo             (docs/blog/post/demo/index.html)
  atlas/index.html      the neuron atlas                 (docs/blog/neuron-atlas/index.html)
  atlas/data/           the atlas's per-layer data       (docs/blog/atlas/data, gitignored: built by scripts/12 and 43/44)
  vertical/, lib/       shared demo code, the browser model (float16 weights) and the concept names

Files the pages fetch at run time (model weights, atlas data) are listed in publish-files.txt so the publisher copies them too.
Shared style (../assets/tokens.css) stays shared. Light file work only; run after scripts/42_build_post.py."""
import re
import shutil

from c4n import config

ROOT = config.ROOT
B = ROOT / "docs" / "blog"
OUT = ROOT / "build" / "publish_post"


def put(rel, text=None, src=None):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if text is not None:
        p.write_text(text, encoding="utf-8")
    else:
        shutil.copyfile(src, p)


def sub(text, pairs, where):
    for a, b in pairs:
        assert a in text, f"{where}: expected to find {a!r}"
        text = text.replace(a, b)
    return text


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    # the post: only its two outward links change
    post = (B / "post" / "index.html").read_text(encoding="utf-8")
    post = sub(post, [('href="demo/"', 'href="demo/index.html"'), ('href="../neuron-atlas/#library"', 'href="atlas/index.html#library"'),
                      ('href="../neuron-atlas/"', 'href="atlas/index.html"')], "post")
    assert "../neuron-atlas" not in post and "../ns-atlas" not in post and "../demo/" not in post, "post still points outside the bundle"
    put("index.html", post)
    for f in ("post.css", "post.js", "story.js", "data/figures.js", "data/atlas.js", "img/demo.png"):
        put(f, src=B / "post" / f)
    # the demo page, one level down
    demo = (B / "post" / "demo" / "index.html").read_text(encoding="utf-8")
    demo = sub(demo, [('href="../../vertical/vertical.css"', 'href="../vertical/vertical.css"'), ('src="../../demo/concepts.js"', 'src="../lib/concepts.js"'),
                      ('src="../../vertical/', 'src="../vertical/'), ('window.VDEMO_MODEL = "../../demo/model.json"', 'window.VDEMO_MODEL = "../lib/model.json"'),
                      ('window.ATLAS_URL = "../../neuron-atlas/"', 'window.ATLAS_URL = "../atlas/index.html"'),
                      ('href="../../neuron-atlas/"', 'href="../atlas/index.html"'), ('href="../"', 'href="../index.html"'), ('href="../#agent"', 'href="../index.html#agent"')], "demo")
    put("demo/index.html", demo)
    for f in ("vertical.css", "vertical.js", "switches.js", "c4model.js", "data/vertical.js"):
        put(f"vertical/{f}", src=B / "vertical" / f)
    for f in ("concepts.js", "model.json", "model.bin"):
        put(f"lib/{f}", src=B / "demo" / f)
    # the neuron atlas, one level down; its script fetches the per-layer data and the model
    at = (B / "neuron-atlas" / "index.html").read_text(encoding="utf-8")
    at = sub(at, [('href="../assets/tokens.css"', 'href="../../assets/tokens.css"'), ('src="../demo/concepts.js"', 'src="../lib/concepts.js"'),
                  ('src="../vertical/c4model.js"', 'src="../vertical/c4model.js"'), ('src="../post/data/atlas.js"', 'src="../data/atlas.js"'),
                  ('href="../post/"', 'href="../index.html"')], "atlas page")
    put("atlas/index.html", at)
    put("atlas/atlas.css", src=B / "neuron-atlas" / "atlas.css")
    put("atlas/data/map.js", src=B / "neuron-atlas" / "data" / "map.js")
    js = (B / "neuron-atlas" / "atlas.js").read_text(encoding="utf-8")
    js = sub(js, [('const D = "../atlas/data/"', 'const D = "data/"'), ('C4Model.load("../demo/model.json")', 'C4Model.load("../lib/model.json")'),
                  ('href="../post/"', 'href="../index.html"')], "atlas.js")
    put("atlas/atlas.js", js)
    fetched = ["meta.json", "overview.json", "games.json"] + [f"L{l}.json" for l in range(6)]
    for f in fetched:
        put(f"atlas/data/{f}", src=B / "atlas" / "data" / f)
    extra = ["lib/model.json", "lib/model.bin"] + [f"atlas/data/{f}" for f in fetched]
    put("publish-files.txt", "# files the pages fetch at run time (not visible as src/href); copied by the site publisher\n" + "\n".join(extra) + "\n")
    # every relative src/href in the three pages must resolve inside the bundle (shared style files excepted)
    bad = []
    for page in ("index.html", "demo/index.html", "atlas/index.html"):
        base = (OUT / page).parent
        for path in re.findall(r'\b(?:src|href)="(?!https?:|//|/|#|mailto:|data:)([^"#?]+)', (OUT / page).read_text()):
            if path.endswith(("assets/tokens.css", "assets/charts.js")):
                continue
            f = (base / path).resolve()
            if not f.is_file() or OUT.resolve() not in f.parents:
                bad.append(f"{page}: {path}")
    assert not bad, f"references outside the bundle: {bad}"
    size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"bundle {OUT} ready: {sum(1 for f in OUT.rglob('*') if f.is_file())} files, {size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()

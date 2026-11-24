"""Map view of the neuron atlas: a 2-D layout of all 12,288 neuron poles by what the board looks like when they fire.
Each pole's "occ" vector (126 numbers: change in how often each cell holds the mover's stone, the opponent's stone, or is empty, when
the pole fires, from docs/blog/atlas/data/L*.json) is embedded with t-SNE (PCA init, fixed seed). Regions are k-means clusters of the
layout, named by their most common concept family and concept among poles with F1 >= 0.3. Writes docs/blog/neuron-atlas/data/map.js,
aligned with docs/blog/atlas/data/overview.json. Run on a GPU host (CPU work, a minute or two)."""
import collections
import json

import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

from c4n import config
from c4n.concepts import NAMES

ROOT = config.ROOT
ATL = ROOT / "docs" / "blog" / "atlas" / "data"
OUT = ROOT / "docs" / "blog" / "neuron-atlas" / "data" / "map.js"
SEED, K = 20261123, 18


def main():
    ov = json.loads((ATL / "overview.json").read_text())
    meta = json.loads((ATL / "meta.json").read_text())
    layers = {l: json.loads((ATL / f"L{l}.json").read_text()) for l in range(meta["config"]["n_layer"])}
    n = len(ov["layer"])
    X = np.zeros((n, 126), dtype=np.float32)
    for i in range(n):
        r = layers[ov["layer"][i]][ov["neuron"][i]]
        X[i] = np.asarray(r["poles"][ov["sign"][i]]["occ"], dtype=np.float32) / 45.0
    Y = TSNE(n_components=2, perplexity=40, init="pca", random_state=SEED, learning_rate="auto").fit_transform(X)
    Y = (Y - Y.min(0)) / (Y.max(0) - Y.min(0))
    km = KMeans(n_clusters=K, n_init=10, random_state=SEED).fit(Y)
    regions = []
    for k in range(K):
        idx = np.flatnonzero(km.labels_ == k)
        good = [i for i in idx if ov["f1"][i] >= 0.3]
        fam = collections.Counter(meta["families"][ov["fam"][i]] for i in good).most_common(1)
        con = collections.Counter(NAMES[ov["c"][i]] for i in good).most_common(1)  # overview "c" indexes the full NAMES list, not meta["concepts"]
        regions.append({"x": float(km.cluster_centers_[k][0]), "y": float(km.cluster_centers_[k][1]), "n": int(len(idx)), "n_labelled": len(good),
                        "family": fam[0][0] if fam else None, "concept": con[0][0] if con else None})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("window.ATLASMAP = " + json.dumps({"x": np.round(Y[:, 0], 4).tolist(), "y": np.round(Y[:, 1], 4).tolist(),
                                                       "region": km.labels_.tolist(), "regions": regions, "seed": SEED, "names": list(NAMES)}, separators=(",", ":")) + ";\n")
    print(f"{n} poles laid out; {K} regions; wrote {OUT}")


if __name__ == "__main__":
    main()

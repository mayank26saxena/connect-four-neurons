# Connect Four neurons: interpretability with an exact answer key

A small transformer (6 layers, d_model 256, 1,024 bias-free SwiGLU neurons per layer, 6.3M parameters) learns to play Connect Four
from the raw list of moves. A C rules engine labels every position with exact concepts (cells, landing spots, immediate wins,
forced blocks, threats, lines, game phase), so claims about what a neuron or a circuit does can be checked against the truth
rather than against an LLM judge.

The project takes Goodfire's "Neurons as an Interpretable Basis" (Tigges et al., 2026) as its starting point and asks, in a
setting with ground truth: are single neurons a good unit of analysis, what does the model compute, and would an AI agent that
describes neurons one at a time (a "Neuron Scientist") find the parts that actually drive a behaviour?

Every test was written into [docs/PLAN.md](docs/PLAN.md) (dated addenda a-u) before it was run; [docs/LOG.md](docs/LOG.md) is the
dated lab notebook with every number, including the predictions that failed.

## Main findings

- **The model keeps a board in its head**, in the player's own frame (mine / theirs, not red / yellow): 98.6% readable after
  layer 3's attention, and editing a stone in that internal board changes the move when the stone matters far more than when it
  does not (addenda h-k).
- **Vertical blocking has a compact circuit; horizontal and diagonal blocking do not.** By a rule fixed in advance, 53 neurons carry
  80% of the push towards blocking a vertical three (addendum s). Read from input to output: attention head 2 of layer 0 gathers
  the opponent's recent moves; 15 directions (3,000 neurons would be needed for the same share) carry the threat through layers
  1-4; 36 single-neuron "column alarms" in layer 5 push the move. Switching each step off drops vertical blocks from 100% to 73%,
  64% and 70% (addenda t, u). Horizontal and diagonal threats need 40 and 60 directions, or 290 and 770 neurons, and no neuron
  circuit within the cap.
- **A blind describing agent found the circuit where single neurons do the work.** Given the 20 most important circuit neurons
  shuffled among 20 matched decoys and 10 random directions, and told nothing about blocking, a fresh agent per unit wrote a rule
  that picks out "block in this column" for 14 of the 20 circuit neurons and 2 of the 20 decoys (pre-registered bar: at least 10
  and at most 2). Its rules also predicted the circuit neurons' own firing better (median F1 0.53 vs 0.29). A text-only reading of
  the descriptions did not separate the groups (18 of 20 vs 6 of 20; registered bar at most 2), so the test that works runs the
  agent's rule (addendum s, Test B).
- **Neurons suit local concepts, not global ones.** Single neurons capture 31% of 659 concepts against 56% for trained linear
  readouts; they beat random directions on local concepts (one cell, one column, the last move) and lose on global ones. Wider MLPs
  made single neurons less, not more, interpretable: all three registered predictions failed in the opposite direction
  (addenda c-g, o).

## Write-up

Post: [An AI Agent Found Most of the Neurons That Block a Connect Four Threat](https://mayank26saxena.github.io/blog/connect-four-blocking-neurons/), with an [interactive demo](https://mayank26saxena.github.io/blog/connect-four-blocking-neurons/demo/index.html) and a [neuron atlas](https://mayank26saxena.github.io/blog/connect-four-blocking-neurons/atlas/index.html).

- Blog post: [docs/blog/post/](docs/blog/post/) (built by `scripts/42_build_post.py`, which fills every number from `results/` and
  fails on any mismatch), with an interactive demo ([docs/blog/post/demo/](docs/blog/post/demo/)) and a browsable neuron atlas
  ([docs/blog/neuron-atlas/](docs/blog/neuron-atlas/)).
- Serve locally: `python3 -m http.server 8812 --directory docs/blog`, then open `/post/`.

## Layout

```
engine/c4.c          bitboard engine, deterministic depth-limited negamax teacher, seeded game generator
c4n/                 engine bindings, concept labels, model, analysis, tactics, world-model probes, circuit patching (circuit.py),
                     Neuron Scientist tools and verification (ns.py), provenance
scripts/01-24        model, data, training and the neuron / concept / width / validity / world-model studies (see REPRODUCE.md)
scripts/30-46        Neuron Scientist studies (q), (r) and the blind test on the blocking circuit, the circuit itself, the vertical map
scripts/42-47        blog post, atlas data and the publishing bundle
configs/             every hyperparameter (base.yaml = main run; others = sweeps, ladder, studies)
results/             every result file, each with a .meta.json (source hash, config, environment, output hash)
ns/, ns2/, ns3/      the three agent studies: prompts, frozen descriptions, the agents' work folders, orchestrator logs, reports
web/, docs/blog/     dependency-free JavaScript port of the model, the post, demo and atlas
tests/               engine vs brute force, determinism, concept labels, decomposition exactness, JS port vs PyTorch
```

## Running

Requires `uv`, a C compiler and, for training and the patching studies, a CUDA GPU (one RTX 4090 is ample). See
[REPRODUCE.md](REPRODUCE.md).

```bash
uv sync
make test
make all          # data, training, play strength, the first analyses, web export, manifest
```

`C4N_CONFIG=smoke make all` runs every stage at toy scale in a few minutes.

**Weights.** Training checkpoints are not stored in git. The exact weights every later analysis, the agents and the demo use are
the float16 export in `docs/blog/demo/model.{json,bin}` (loaded by `ns.load_web_model`); `MANIFEST.sha256` lists the hashes of the
full-precision checkpoints and data.

## Agent studies and blinding

The describing agents ran in a separate account from sealed bundles (`scripts/38_ns3_bundle.py` lists what each bundle holds):
no plan, log, results or answer key. Test B's keys (`ns3/private/key.json`, which units are neurons or random directions, and
`results/ns3_membership.json`, which neurons are circuit or decoy) were committed only after the descriptions were frozen and
scored. The keys of the two earlier studies (`ns/private/`, `ns2/private/`) stayed on the machine that ran them and are not included. Absolute paths in the agents' work files were
replaced with `{REPO}` before release.

## Limits

One small model and one tactic studied end to end; the neuron-first method works for vertical threats, where single neurons do the
work, and not for horizontal or diagonal ones. Switches use mean ablation, and they also cost ordinary play. See the post's Limits
section and docs/LOG.md for every failed prediction.

## Reference

C. Tigges, M. Kowal, T. McGrath, O. Lewis, N. Cammarata. *Neurons as an Interpretable Basis.* Goodfire Research, 2026.
https://www.goodfire.com/research/neurons-as-an-interpretable-basis

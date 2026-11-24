# Reproducing every result

## Environment

- Python 3.12, dependencies pinned in `uv.lock` (`uv sync` installs exactly these; torch 2.9.0, CUDA 12.8 wheels on Linux).
- C compiler (`cc`); the engine is compiled on first use with `-O2 -ffp-contract=off` into `build/`.
- Main run hardware: one NVIDIA RTX 4090 (driver 595.112.07), image `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404`.
  Each output's `.meta.json` records the exact environment it was produced in.

## Determinism

- **Data** is a pure function of the config. The teacher returns exact depth-limited minimax scores (the transposition
  table only accepts exact-depth hits), move sampling uses a seeded SplitMix64 generator, and the softmax uses a
  libm-free `exp` so results do not depend on the C library. Check with
  `uv run python scripts/check_determinism.py 2000`: expected hash
  `e9d05db59ce73388cb477020be0efbf48ab02015f2893c8cdf1854150a4452e8` (first 2,000 training games).
- **Training** uses fixed seeds for initialisation and data order. GPU kernels are not bitwise deterministic across
  hardware, so retrained weights can differ in low-order bits; the released checkpoints and their hashes
  (`MANIFEST.sha256`) are the reference for every reported number.
- **Analysis** is deterministic given a checkpoint (seeded sampling of poles, firings, rotations and Leiden).

## Steps

| Stage | Command | Output |
|---|---|---|
| tests | `make test` | — |
| data | `make data` | `data/{train,val,analysis}.npz` (+ `.meta.json` with content hash) |
| training | `make train` | `checkpoints/main/step_*.pt`, `results/train_curve_main.json` |
| play strength | `make play` | `results/play_main_step_008000.json` |
| analyses | `make analysis` | `results/sparsity.json`, `concepts_summary.json`, `pole_table.json`, `modes.json`, `action.json` |
| demo export | `make web` | `web/model.{json,bin}`, `web/poles.json`, `web/reference.json` |
| manifest | `make manifest` | `MANIFEST.sha256` |

`make all` runs them in order. `C4N_CONFIG=smoke make all` is a toy-scale end-to-end check.

## Later studies

Each script reads its config (`C4N_CONFIG`, default `base`), writes one result file in `results/` with a `.meta.json`, and is
described in the PLAN.md addendum it names. GPU stages ran on one RTX 4090 or RTX A4500 pod.

| Study (PLAN addendum) | Scripts | Main outputs |
|---|---|---|
| width sweep (c) | `scripts/make_sweep.py`, `run_sweep.sh`, `10_sweep_summary.py` | `results/sweep/`, `sweep_summary.json` |
| sparse autoencoder (Q7) | `11_sae.py` | `sae.json` |
| validity tests T1-T7 (e) | `13_basis_controls.py`, `14_crossfit.py`, `15_validity_summary.py` | `basis_controls.json`, `crossfit.json`, `validity_summary.json` |
| tactic atlas (f, g) | `16_tactic_atlas.py`, `17_tactic_emergence.py`, `18_atlas_export.py`, `19_build_atlas.py` | `tactic_atlas.json`, `tactic_emergence.json`, `docs/blog/atlas/data/` |
| world model and board edits (h-k) | `21_world_model.py`, `21b_edit_followup.py`, `21c_edit_history.py`, `22_board_causal.py` | `world_model*.json`, `board_causal.json` |
| size ladder (l) | `scripts/run_ladder.sh`, `23_ladder_summary.py` | `results/ladder/`, `ladder_summary.json` |
| concept coverage (o) | `24_concept_coverage.py` | `concept_coverage.json` |
| Neuron Scientist (q), (r) | `30_ns_prepare.py`, `31_ns_tool.py` (agent tools), `32_ns_verify.py` | `ns/report.json`, `ns2/report.json` |
| blocking circuit, Test A (s) | `35_block_circuit.py`, `36_ns_block_testA.py` | `block_circuit.json` (frozen; hash in LOG), `ns_block_testA.json` |
| Test B, the blind run (s) | `37_ns3_prepare.py`, `38_ns3_bundle.py`, agents, `45_ns3_textcheck.py`, `32_ns_verify.py`, `46_ns3_score.py` | `ns3/report.json`, `ns3_testB.json` |
| orientations (t) | `39_orientation_followup.py` | `orientation_followup.json` |
| vertical blocker end to end (u) | `40_vertical_map.py`, `40b_vertical_posthoc.py`, `41_vertical_demo_export.py` | `vertical_map.json`, `vertical_posthoc.json` |
| write-up | `42_build_post.py`, `43_atlas_map_export.py`, `44_atlas_map_layout.py`, `47_publish_bundle.py` | `docs/blog/post/`, `build/publish_post/` |

The agent studies need a separate Claude Code session per unit (`ns3/ORCHESTRATOR.md` is the orchestrator's brief and
`ns3/prompts/unit_prompt_s.txt` the unit prompt); everything else is a script. Scoring a study needs its answer key
(`ns*/private/key.json`, written by `30_ns_prepare.py` / `37_ns3_prepare.py`). Test B's key is included (`ns3/private/key.json`);
the keys of studies (q) and (r) are not, so their reports (`ns/report.json`, `ns2/report.json`) are the record for those two.

## Remote execution

`scripts/pod.sh push | run "<cmd>" | pull` syncs this checkout to a GPU host given `POD_SSH="user@host -p port"`,
runs a command there, and copies `results/`, `runs/`, `checkpoints/` and `data/` back.

# Full pipeline. Every stage reads configs/$(C4N_CONFIG).yaml (default: base) and writes provenance next to its output.
# Run on a CUDA host; `scripts/pod.sh` syncs a checkout to a remote host if you develop elsewhere.
export C4N_CONFIG ?= base
PY = uv run python -W ignore

.PHONY: all test data train play analysis web manifest
all: test data train play analysis web manifest

test:
	uv run pytest -q tests

data:            ## teacher games for train / val / analysis (CPU, deterministic)
	$(PY) scripts/01_generate_data.py

train:           ## transformer on teacher soft targets; checkpoints on a log-spaced schedule
	$(PY) scripts/02_train.py

play:            ## play strength of the final checkpoint
	$(PY) scripts/03_eval_play.py

analysis:        ## Q1 sparsity, Q2-Q3 concepts, Q4 modes, Q5 action
	$(PY) scripts/04_sparsity.py
	$(PY) scripts/05_concepts.py
	$(PY) scripts/06_modes.py
	$(PY) scripts/07_action.py
	$(PY) scripts/07b_group_action.py
	$(PY) scripts/08_dynamics.py
	$(PY) scripts/11_sae.py

web:             ## weights + pole catalog for the in-browser demo, then check the JS port against PyTorch
	$(PY) scripts/09_export_web.py
	node tests/check_web_port.js

manifest:
	$(PY) scripts/manifest.py

blog:            ## rebuild docs/blog/index.html from results (stdlib + pyyaml, no model run)
	$(PY) scripts/12_build_blog.py

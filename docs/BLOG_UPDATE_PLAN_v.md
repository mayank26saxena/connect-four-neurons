# Plan: adding study (v) to the Connect Four post and atlas

Status 2026-11-25: V1-V13 run and scored (8 hold, 5 fail; docs/LOG.md). v-14 (the blind auditing game) was not run; the
post says so in Appendix J. The update below was published to the post and atlas on 2026-11-25 (V1-V13 only).

## What the post gains (one story, not a second paper)

The current post says *where* blocking lives and whether an agent finds it. Study (v) adds *what each neuron writes*. That
gives three short claims, each backed by a figure or table:

1. **Reading a neuron by its output works, but only through the later layers.** The J-lens readout names the column a neuron
   actually pushes for 71% of measurable neurons in layers 0-4, against 29% for the logit lens and 14% chance (v-1). Layer 5
   is 94% (v-2).
2. **Vertical blocking behaves like a fact: distributed but readable.** Removing the 205 answer-writer neurons leaves half the
   blocks in place. A median of 10 more readable neurons flips almost all of them, and random ones flip none (v-7, v-8).
3. **The neurons are usable without labels.** Six rule-written example boards per column pick neurons whose probe scores AUROC
   0.95-0.99, matching probes trained on 40 labels for 5 of 7 columns (v-9). Their output vectors steer the model to that column
   61% of the time, against 68% for a labelled direction (v-10).

Failures go in Limits and the appendix, in plain words:
- Early layers barely write moves (v-3).
- "Two unrelated concepts at once" is common here, 59% (36% in the follow-up), because board concepts are compositional (v-5).
- Indirect output vectors keep their meaning only 74% of the time when moved (v-6).
- Neuron voting did not find opening triggers (v-12).
- Gradient-ascent unlearning was not a few neurons (v-13).

Credit: cite Shone & Dunlap (2026, parts 1 and 2) once, where the method is introduced, and Gurnee et al. (2026) for the J-lens.
No comparison section, in line with the earlier decision.

## Changes, file by file

| Where | Change | Source numbers |
|---|---|---|
| Post, section 02 (after Figure 4) | New sub-section "What the neurons write": two paragraphs plus **Figure 5**, agreement with the causal column by layer for the J-lens, the logit lens and chance | outputs_v15.json V1 |
| Post, section 02 | One paragraph plus **Figure 6**, a removal curve: share of vertical blocks still played vs readable neurons removed, with a random-neuron line and the answer-writers-only point marked | outputs_v15.json V5 (needs per-k curve, see below) |
| Post, section 03 | One paragraph and a 3-row table: zero-label probe vs 40/400-label probes vs heuristic, and the steering rates | outputs_v67.json |
| Post, section 03 or 05 | The organisms and audit, two sentences: the backdoors reuse pretrained column neurons (v-11); the audit result once v-14 returns | outputs_v8.json |
| Post, Limits | Add v-3, v-5, v-6, v-12 and v-13 in one paragraph | LOG |
| Post, Appendix J (new) | "Reading neurons by what they write, in full": the 13-prediction table, the type-3 follow-up, the fixed-basis rows, organism behaviour, why voting and restoration failed | all three JSONs |
| Post, references | Shone & Dunlap 2026 (two posts), Gurnee et al. 2026 (arXiv 2607.15495). Check each title against its page before publishing | - |
| Atlas, neuron page | New "What it writes" row: column readout (7 bars, J-lens) and top-5 concept readout, with the causal check where it was measured | outputs_readouts.npz |
| Atlas, Library | New set "Answer writers" (the 205 layer-5 writers, marked where they overlap R) | outputs_v15.json V5 |
| Figure numbers | Current Figures 5-7 become 7-9; update in-text references and the build assertions | - |

Word budget: the main text stays under about 2,000 words. The new text in sections 02/03 is about 350 words; the detail goes in
Appendix J.

## Build steps

1. **Small export addition.** `48_readouts.py` stores only the flip count per position. Figure 6 needs the curve (share still
   blocking at k = 0, 10, ..., 500, readable vs random). Add a CPU-light export, or a short pod re-run of V5 only (about 2 min of
   GPU, about $0.05).
2. **`scripts/42_build_post.py`:** new placeholders `ov_*`, each read from the result files with assertions, so the build fails
   if a prose number drifts.
3. **`post.js`:** two chart components (grouped bars by layer; a removal curve with a random line) in the house style. Add an
   Appendix J table renderer.
4. **`scripts/43_atlas_map_export.py` / `atlas.js`:** export readJ and the top-5 concept readouts per pole, and draw them on the
   neuron page and in the new Library set.
5. **QA, per the research-blog checklist:**
   - desktop and 390 px screenshots of every new figure;
   - no overflow;
   - tooltips;
   - every citation resolves;
   - the build's number checks pass.
6. **Publish:**
   - `scripts/47_publish_bundle.py`, then the site's `bin/publish_post.py` (same slug), after the author's go-ahead;
   - refresh the public repo with a new snapshot commit (`make_public_snapshot.sh` flow);
   - keep `v_audit/private/` untracked until v-14 returns.

## Open decisions (author)

- **Placement:** a new sub-section in section 02 (recommended; keeps one story), or a new section 04.
- **Timing:** publish V1-V13 now and add the audit result when it returns (recommended), or wait for v-14.
- **Atlas:** add the "What it writes" row now, or keep the atlas unchanged for this update.

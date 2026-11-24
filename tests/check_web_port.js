// Node check that web/c4model.js reproduces PyTorch (web/reference.json). Run: node tests/check_web_port.js
const fs = require("fs");
const path = require("path");
const { C4Model } = require("../web/c4model.js");

const web = path.join(__dirname, "..", "web");
const man = JSON.parse(fs.readFileSync(path.join(web, "model.json")));
const bin = fs.readFileSync(path.join(web, "model.bin"));
const m = C4Model.fromBuffer(man, bin.buffer.slice(bin.byteOffset, bin.byteOffset + bin.byteLength));
const ref = JSON.parse(fs.readFileSync(path.join(web, "reference.json")));
let maxLogit = 0, maxAct = 0, argmaxAgree = 0, n = 0;
const t0 = Date.now();
for (const r of ref) {
  const out = m.forward(r.tokens);
  r.logits.forEach((row, p) => {
    const js = out.logits[p];
    let a = 0, b = 0;
    row.forEach((v, c) => { maxLogit = Math.max(maxLogit, Math.abs(v - js[c])); if (v > row[a]) a = c; if (js[c] > js[b]) b = c; });
    argmaxAgree += a === b; n++;
  });
  const last = out.acts[3][r.tokens.length - 1];
  r.acts_layer3_last.forEach((v, j) => { maxAct = Math.max(maxAct, Math.abs(v - last[j])); });
}
const ms = (Date.now() - t0) / ref.length;
console.log(JSON.stringify({ max_abs_logit_diff: maxLogit, max_abs_act_diff: maxAct, argmax_agreement: argmaxAgree / n, ms_per_game_forward: ms }));
// mean-ablated parts (web/parts.json, web/reference_parts.json), if exported
if (fs.existsSync(path.join(web, "parts.json"))) {
  const P = JSON.parse(fs.readFileSync(path.join(web, "parts.json"))), RP = JSON.parse(fs.readFileSync(path.join(web, "reference_parts.json")));
  let worst = 0;
  for (const part of P.parts) {
    const opts = { ablate: new Set(part.neurons.map(([l, n]) => `${l}:${n}`)), headMean: new Set(part.heads.map(([l, h]) => `${l}:${h}`)), mlpMean: new Set(part.mlp), means: P };
    for (const r of RP[part.id]) {
      const out = m.forward(r.tokens, opts);
      r.logits.forEach((row, p) => row.forEach((v, c) => { worst = Math.max(worst, Math.abs(v - out.logits[p][c])); }));
    }
  }
  console.log(JSON.stringify({ parts_checked: P.parts.length, max_abs_logit_diff_parts: worst }));
  if (worst > 5e-3) process.exit(1);
}
if (maxLogit > 1e-3 || argmaxAgree / n < 1) process.exit(1);
// board probes and edits (web/worldmodel.json, exported by scripts/21_world_model.py): replay each puzzle's edit in JS
if (fs.existsSync(path.join(web, "worldmodel.json"))) {
  const { WorldModel } = require("../web/worldmodel.js");
  const meta = JSON.parse(fs.readFileSync(path.join(web, "worldmodel.json")));
  const wb = fs.readFileSync(path.join(web, "worldmodel.bin"));
  const wm = WorldModel.fromBuffer(meta, wb.buffer.slice(wb.byteOffset, wb.byteOffset + wb.byteLength));
  const sm = (lg, legal) => { const e = lg.map((v, c) => legal[c] ? Math.exp(v) : 0), z = e.reduce((a, b) => a + b); return e.map((v) => v / z); };
  let worstP = 0;
  for (const pz of meta.puzzles) {
    const tokens = [7, ...pz.moves], at = pz.moves.length;
    const legal = pz.scores_edit.map((s) => s !== -32768);
    const clean = sm(Array.from(m.forward(tokens).logits[at]), legal);
    const ed = sm(Array.from(m.forward(tokens, { residHook: wm.editHook({ cell: pz.cell, src: pz.src, tgt: pz.tgt, at }) }).logits[at]), legal);
    clean.forEach((v, c) => { worstP = Math.max(worstP, Math.abs(v - pz.p_clean[c]), Math.abs(ed[c] - pz.p_edit[c])); });
  }
  console.log(JSON.stringify({ puzzles_checked: meta.puzzles.length, max_abs_prob_diff_edits: worstP }));
  if (worstP > 2e-2) process.exit(1);
}

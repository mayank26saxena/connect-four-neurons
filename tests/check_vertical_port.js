// Node check (PLAN addendum u): web/c4model.js reproduces PyTorch under the vertical-blocker demo switches and returns the
// same L0 H2 attention. Inputs: web/vertical.json, web/reference_vertical.json (scripts/40_vertical_map.py). Run: node tests/check_vertical_port.js
const fs = require("fs");
const path = require("path");
const { C4Model } = require("../web/c4model.js");
const { switchOpts } = require("../docs/blog/vertical/switches.js");

const web = path.join(__dirname, "..", "web");
const man = JSON.parse(fs.readFileSync(path.join(web, "model.json")));
const bin = fs.readFileSync(path.join(web, "model.bin"));
const m = C4Model.fromBuffer(man, bin.buffer.slice(bin.byteOffset, bin.byteOffset + bin.byteLength));
const V = JSON.parse(fs.readFileSync(path.join(web, "vertical.json")));
const refs = JSON.parse(fs.readFileSync(path.join(web, "reference_vertical.json")));
let worst = {}, worstAtt = 0;
for (const r of refs) {
  for (const [name, rows] of Object.entries(r.logits)) {
    const out = m.forward(r.tokens, switchOpts(V, name));
    let w = 0;
    rows.forEach((row, p) => row.forEach((v, c) => { w = Math.max(w, Math.abs(v - out.logits[p][c])); }));
    worst[name] = Math.max(worst[name] || 0, w);
    if (name === "none") {
      const att = out.attn[V.head[0]][r.tokens.length - 1][V.head[1]];
      r.head_attention_last.forEach((v, s) => { worstAtt = Math.max(worstAtt, Math.abs(v - att[s])); });
    }
  }
}
console.log(JSON.stringify({ games: refs.length, max_abs_logit_diff: worst, max_abs_attention_diff: worstAtt }));
if (Object.values(worst).some((w) => w > 5e-3) || worstAtt > 1e-3) process.exit(1);

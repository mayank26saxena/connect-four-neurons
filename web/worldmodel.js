// The board in the model's head: linear probes on the residual stream (exported by scripts/21_world_model.py) and edits
// to what they read. Mirrors c4n/worldmodel.py (Probe.logits, edit_alpha, edit_hook).
//   const wm = WorldModel.fromBuffer(meta, buffer);
//   wm.read(x, i) -> Float32Array(42 * 3) softmax probabilities [empty, mine, theirs] per cell at read point i
//   wm.editHook({cell, src, tgt, start, at}) -> residHook for C4Model.forward: edits position `at` from block `start` on
(function (global) {
  "use strict";
  function f16(h) {
    const s = h & 0x8000 ? -1 : 1, e = (h >> 10) & 31, f = h & 1023;
    if (e === 0) return s * Math.pow(2, -14) * (f / 1024);
    if (e === 31) return f ? NaN : s * Infinity;
    return s * Math.pow(2, e - 15) * (1 + f / 1024);
  }

  class WorldModel {
    static fromBuffer(meta, buf) {
      const u16 = new Uint16Array(buf), [P, D, K, C] = meta.W_shape, nW = P * D * K * C, [, , KT] = meta.Wt_shape;
      const W = new Float32Array(nW), Wt = new Float32Array(P * D * KT);
      for (let i = 0; i < nW; i++) W[i] = f16(u16[i]);
      for (let i = 0; i < Wt.length; i++) Wt[i] = f16(u16[nW + i]);
      return new WorldModel(meta, W, Wt);
    }
    constructor(meta, W, Wt) { this.meta = meta; this.W = W; this.Wt = Wt; [this.P, this.D, this.K, this.C] = meta.W_shape; }
    w(i, d, k, c) { return this.W[((i * this.D + d) * this.K + k) * this.C + c]; }

    logits(x, i) {
      const { D, K, C } = this, out = new Float32Array(K * C), b = this.meta.b[i];
      for (let k = 0; k < K; k++) for (let c = 0; c < C; c++) {
        let s = b[k][c]; const base = (i * D * K + k) * C + c;
        for (let d = 0; d < D; d++) s += x[d] * this.W[base + d * K * C];
        out[k * C + c] = s;
      }
      return out;
    }
    read(x, i) {
      const lg = this.logits(x, i), { K, C } = this;
      for (let k = 0; k < K; k++) {
        let mx = -Infinity, z = 0;
        for (let c = 0; c < C; c++) mx = Math.max(mx, lg[k * C + c]);
        for (let c = 0; c < C; c++) { lg[k * C + c] = Math.exp(lg[k * C + c] - mx); z += lg[k * C + c]; }
        for (let c = 0; c < C; c++) lg[k * C + c] /= z;
      }
      return lg;
    }
    // threat-cell probabilities at read point i: [mine(42), theirs(42)]
    threats(x, i) {
      const { D } = this, KT = this.meta.Wt_shape[2], out = new Float32Array(KT), bt = this.meta.bt[i];
      for (let k = 0; k < KT; k++) {
        let s = bt[k];
        for (let d = 0; d < D; d++) s += x[d] * this.Wt[(i * D + d) * KT + k];
        out[k] = 1 / (1 + Math.exp(-s));
      }
      return out;
    }

    // Move x along w_tgt - w_src of cell `cell` until tgt beats every other class by the cell's target margin.
    edit(x, i, cell, src, tgt) {
      const { D, C } = this, m = this.meta.margin[i - 1][cell];
      const u = new Float32Array(D), col = (c) => { const v = new Float32Array(D); for (let d = 0; d < D; d++) v[d] = this.w(i, d, cell, c); return v; };
      const Wc = [0, 1, 2].map(col);
      for (let d = 0; d < D; d++) u[d] = Wc[tgt][d] - Wc[src][d];
      const lg = this.logits(x, i), b = cell * C;
      let alpha = 0;
      for (let j = 0; j < C; j++) {
        if (j === tgt) continue;
        let slope = 0; for (let d = 0; d < D; d++) slope += u[d] * (Wc[tgt][d] - Wc[j][d]);
        if (slope <= 1e-12) continue;
        alpha = Math.max(alpha, (m - (lg[b + tgt] - lg[b + j])) / slope);
      }
      for (let d = 0; d < D; d++) x[d] += alpha * u[d];
      return alpha;
    }
    editHook({ cell, src, tgt, start = this.meta.start, at }) {
      return (i, p, x) => { if (i >= start + 1 && p === at) this.edit(x, i, cell, src, tgt); };
    }
  }
  global.WorldModel = WorldModel;
  if (typeof module !== "undefined") module.exports = { WorldModel };
})(typeof window !== "undefined" ? window : globalThis);

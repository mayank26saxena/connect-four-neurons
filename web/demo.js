// Live neuron demo: play the model, watch labelled neurons fire, switch neurons off or force them on, and see what
// the model does. Mount: C4Demo.mount(element, { base: "./" }). Needs c4model.js and concepts.js loaded first, and in
// `base`: model.json, model.bin, poles.json (labelled poles with threshold and force-on value), groups.json (top
// neurons per action concept, from scripts/07b_group_action.py).
(function (global) {
  "use strict";
  const W = 7, H = 6, BOS = 7;
  const TRIVIAL = /^(ply_|me_first_player|last_col_)/;  // readable straight off position / token embeddings
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const poleId = (l, n, s) => `L${l}·N${n}${s === "+" ? "+" : "−"}`;
  const softmax = (lg, legal) => {
    let mx = -Infinity; for (let c = 0; c < W; c++) if (legal[c] && lg[c] > mx) mx = lg[c];
    const p = new Float32Array(W); let z = 0;
    for (let c = 0; c < W; c++) { p[c] = legal[c] ? Math.exp(lg[c] - mx) : 0; z += p[c]; }
    for (let c = 0; c < W; c++) p[c] /= z; return p;
  };

  function boardOf(moves) {
    const g = Array.from({ length: H }, () => Array(W).fill(0)), h = Array(W).fill(0);
    moves.forEach((c, i) => { g[h[c]][c] = 1 + (i % 2); h[c]++; });
    return { g, h };
  }
  function winner(g) {
    for (let r = 0; r < H; r++) for (let c = 0; c < W; c++) {
      const p = g[r][c]; if (!p) continue;
      for (const [dr, dc] of [[0, 1], [1, 0], [1, 1], [1, -1]]) {
        const cells = [0, 1, 2, 3].map((k) => [r + k * dr, c + k * dc]);
        if (cells.every(([rr, cc]) => rr >= 0 && rr < H && cc >= 0 && cc < W && g[rr][cc] === p)) return { p, cells };
      }
    }
    return null;
  }

  async function mount(root, opts = {}) {
    const base = opts.base || "./";
    root.classList.add("c4demo");
    root.innerHTML = `<div class="c4-status">Loading the model (12 MB)…</div>`;
    const [model, poles, groups, parts] = await Promise.all([
      C4Model.load(base + "model.json"),
      fetch(base + "poles.json").then((r) => r.json()),
      fetch(base + "groups.json").then((r) => (r.ok ? r.json() : {})).catch(() => ({})),
      fetch(base + "parts.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
    ]);
    const examples = parts && parts.examples ? parts.examples : [];
    const TN = { win: "take the win", block: "block", fork: "make a fork", poison: "avoid the poisoned column" };
    const partById = parts ? Object.fromEntries(parts.parts.map((p) => [p.id, p])) : {};
    function exText(x) { return `Right move: column ${x.good.map((c) => c + 1).join(" or ")}. The intact model puts ${Math.round(100 * x.p_intact)}% on it; with the part off, ${(100 * x.p_ablated).toFixed(x.p_ablated < 0.1 ? 1 : 0)}%.`; }
    const L = model.cfg.n_layer;
    const byKey = new Map(poles.map((p) => [`${p.layer}:${p.neuron}${p.pole}`, p]));
    const cellPoles = poles.filter((p) => /^cell_r\dc\d_(mine|theirs)$/.test(p.concept_sweep) && p.f1_sweep >= 0.8);

    // st.iv: pole key "l:n±" -> { kind: "off" } | { kind: "on", from }; st.groupOff: Set of concept names
    const st = { moves: [], humanFirst: true, iv: new Map(), groupOff: new Set(), parts: new Set(), focus: null, hold: false };
    const groupOpts = Object.keys(groups).map((c) => `<option value="${c}">${esc(C4Concepts.describe(c).text)}</option>`).join("");
    root.innerHTML = `
      <div class="c4-bar">
        <div class="c4-btns">
          <button data-act="new1">New game: you start</button>
          <button data-act="new2">New game: model starts</button>
          <button data-act="undo">Undo</button>
          <button data-act="clear">Restore all neurons</button>
          <button data-act="go" class="c4-go" style="display:none">Let the model move</button>
        </div>
        <div class="c4-status" aria-live="polite"></div>
      </div>
      <div class="c4-grid">
        <div class="c4-left">
          <svg class="c4-board" viewBox="0 0 350 330" role="img" aria-label="Connect Four board"></svg>
          <div class="c4-legend"><span><i class="c4-pI"></i>intact model</span><span><i class="c4-pA"></i>with your changes (this one plays)</span></div>
          <div class="c4-mini-wrap"><div class="c4-mini-title">The board as the model's cell neurons see it</div><svg class="c4-mini" viewBox="0 0 140 120"></svg>
          <div class="c4-mini-note">Each cell shows the strongest firing neuron whose ground-truth concept is "this cell holds my / their stone".</div></div>
        </div>
        <div class="c4-right">
          <div class="c4-h">Neurons firing now <small>labelled poles above their p97 / p3 threshold, strongest first</small></div>
          <ol class="c4-list"></ol>
          ${parts ? `<div class="c4-h">Switch off a part of the model <small>its output is replaced by its average, so the rest of the model keeps working</small></div>
          <div class="c4-group"><select class="c4-selp">${parts.parts.map((p) => `<option value="${p.id}">${esc(p.label)}</option>`).join("")}</select><button data-act="part">Switch off</button></div>
          <p class="c4-note c4-pnote">${esc(parts.parts[0].why)}</p>
          ${examples.length ? `<div class="c4-h">Try a position where it matters <small>loads a real position and switches that part off</small></div>
          <div class="c4-group"><select class="c4-sele">${examples.map((x, i) => `<option value="${i}">${esc(partById[x.part].label)}: ${TN[x.tactic]}</option>`).join("")}</select><button data-act="example">Load</button></div>
          <p class="c4-note c4-enote">${esc(exText(examples[0]))}</p>` : ""}` : ""}
          ${groupOpts ? `<div class="c4-h">Switch off a whole concept <small>its 50 best-matching neurons at once</small></div>
          <div class="c4-group"><select class="c4-sel">${groupOpts}</select><button data-act="group">Switch off</button></div>` : ""}
          <div class="c4-off"></div>
        </div>
      </div>`;
    const $ = (s) => root.querySelector(s);
    const board = $(".c4-board"), mini = $(".c4-mini"), list = $(".c4-list"), status = $(".c4-status"), offBox = $(".c4-off");

    const changed = () => st.iv.size > 0 || st.groupOff.size > 0 || st.parts.size > 0;
    function interventions() {
      const ablate = new Set(), clamp = new Map();
      for (const c of st.groupOff) for (const [l, n] of groups[c]) ablate.add(`${l}:${n}`);
      for (const [k, v] of st.iv) {
        const p = byKey.get(k), nk = `${p.layer}:${p.neuron}`;
        if (v.kind === "off") ablate.add(nk); else clamp.set(nk, [p.clamp, v.from]);
      }
      const headMean = new Set(), mlpMean = new Set();
      for (const id of st.parts) { const p = partById[id]; p.neurons.forEach(([l, n]) => ablate.add(`${l}:${n}`)); p.heads.forEach(([l, h]) => headMean.add(`${l}:${h}`)); p.mlp.forEach((l) => mlpMean.add(l)); }
      return { ablate, clamp, headMean, mlpMean, means: parts };
    }
    function sessionFor(o) { const s = model.session(o); s.push(BOS); st.moves.forEach((c) => s.push(c)); return s; }

    let intact = null, edited = null;
    function recompute() { intact = sessionFor({}); edited = changed() ? sessionFor(interventions()) : null; }
    function legalCols() { const { h } = boardOf(st.moves); return h.map((x) => x < H); }
    function policy(sess) { return softmax(sess.logits[st.moves.length], legalCols()); }
    function modelMove() {
      const p = policy(edited || intact), legal = legalCols(); let best = -1;
      for (let c = 0; c < W; c++) if (legal[c] && (best < 0 || p[c] > p[best])) best = c;
      return best;
    }

    function firing() {
      const t = st.moves.length, out = [];
      for (let l = 0; l < L; l++) {
        const a = intact.acts[l][t];
        for (let n = 0; n < a.length; n++) for (const sign of ["+", "-"]) {
          const p = byKey.get(`${l}:${n}${sign}`); if (!p || TRIVIAL.test(p.concept_sweep)) continue;
          const r = a[n] / p.threshold;
          if (r > 1 && ((sign === "+" && a[n] > 0) || (sign === "-" && a[n] < 0))) out.push({ p, r });
        }
      }
      return out.sort((x, y) => y.r - x.r);
    }

    function draw() {
      const { g, h } = boardOf(st.moves), win = winner(g), t = st.moves.length;
      const pI = policy(intact), pA = edited ? policy(edited) : null;
      const focus = st.focus ? C4Concepts.describe(st.focus.concept_sweep) : null;
      const cs = 44, ox = 21, oy = 70;
      let s = "";
      for (let c = 0; c < W; c++) {  // move-probability bars: wide = intact, thin dark = edited model
        const x = ox + c * cs + 6, bw = cs - 12, hI = 46 * pI[c];
        s += `<rect x="${x}" y="${58 - hI}" width="${bw}" height="${hI}" class="c4-pI"/>`;
        if (pA) { const hA = 46 * pA[c]; s += `<rect x="${x + bw / 2 - 3}" y="${58 - hA}" width="6" height="${hA}" class="c4-pA"/>`; }
        s += `<text x="${x + bw / 2}" y="10" class="c4-pn" text-anchor="middle">${Math.round(100 * (pA || pI)[c])}%</text>`;
      }
      s += `<rect x="${ox - 6}" y="${oy - 6}" width="${W * cs + 12}" height="${H * cs + 12}" rx="6" class="c4-frame"/>`;
      for (let r = 0; r < H; r++) for (let c = 0; c < W; c++) {
        const cx = ox + c * cs + cs / 2, cy = oy + (H - 1 - r) * cs + cs / 2, v = g[r][c];
        const hl = focus && (focus.cells.some(([rr, cc]) => rr === r && cc === c) || (focus.cols.includes(c) && r === Math.min(h[c], H - 1)));
        const wn = win && win.cells.some(([rr, cc]) => rr === r && cc === c);
        s += `<circle cx="${cx}" cy="${cy}" r="17" class="c4-cell ${v === 1 ? "p1" : v === 2 ? "p2" : ""} ${hl ? "hl" : ""} ${wn ? "wn" : ""}"/>`;
      }
      for (let c = 0; c < W; c++) s += `<rect x="${ox + c * cs}" y="0" width="${cs}" height="${oy + H * cs}" class="c4-hit" data-col="${c}"><title>Play column ${c + 1}</title></rect>`;
      board.innerHTML = s;

      const best = Array.from({ length: H }, () => Array(W).fill(null));
      for (const p of cellPoles) {
        const r = intact.acts[p.layer][t][p.neuron] / p.threshold;
        if (r <= 1) continue;
        const [, rr, cc, who] = p.concept_sweep.match(/cell_r(\d)c(\d)_(mine|theirs)/);
        if (!best[rr][cc] || best[rr][cc].r < r) best[rr][cc] = { r, who };
      }
      const toMove = 1 + (t % 2); let m = "";
      for (let r = 0; r < H; r++) for (let c = 0; c < W; c++) {
        const b = best[r][c], owner = b ? (b.who === "mine" ? toMove : 3 - toMove) : 0;
        m += `<circle cx="${10 + c * 20}" cy="${10 + (H - 1 - r) * 20}" r="7.5" class="c4-cell ${owner === 1 ? "p1" : owner === 2 ? "p2" : ""}" opacity="${b ? Math.min(1, 0.35 + b.r / 3) : 1}"/>`;
      }
      mini.innerHTML = m;

      const f = firing().slice(0, 10);
      list.innerHTML = f.length ? f.map(({ p, r }) => {
        const k = `${p.layer}:${p.neuron}${p.pole}`, d = C4Concepts.describe(p.concept_sweep), v = st.iv.get(k);
        return `<li data-k="${k}" class="${v ? "is-" + v.kind : ""}">
          <span class="c4-id">${poleId(p.layer, p.neuron, p.pole)}</span>
          <span class="c4-txt">${esc(d.text)}<small>${esc(d.family)} · F1 ${p.f1_sweep.toFixed(2)}</small></span>
          <span class="c4-str"><i style="width:${Math.min(100, 25 * r)}%"></i></span>
          <span class="c4-acts"><button class="c4-tog" data-k="${k}" data-kind="off">${v && v.kind === "off" ? "on again" : "off"}</button><button class="c4-tog" data-k="${k}" data-kind="on">${v && v.kind === "on" ? "release" : "force on"}</button></span></li>`;
      }).join("") : `<li class="c4-empty">No labelled neuron is above threshold here.</li>`;

      const chips = [...st.groupOff].map((c) => `<span class="c4-chip">${esc(C4Concepts.describe(c).text)}: 50 neurons off <button data-grp="${c}" aria-label="restore">×</button></span>`)
        .concat([...st.iv].map(([k, v]) => { const p = byKey.get(k); return `<span class="c4-chip">${poleId(p.layer, p.neuron, p.pole)} ${v.kind === "off" ? "off" : "forced on from move " + (v.from + 1)} <button data-k="${k}" data-kind="${v.kind}" class="c4-tog" aria-label="undo">×</button></span>`; }));
      for (const id of st.parts) chips.push(`<span class="c4-chip">${esc(partById[id].label)} off <button data-part="${id}" aria-label="restore">×</button></span>`);
      offBox.innerHTML = chips.length ? `<div class="c4-h">Your changes <small>applied to the model you are playing</small></div>${chips.join(" ")}` : "";

      const turnHuman = (t % 2 === 0) === st.humanFirst;
      const go = $(".c4-go"); if (go) go.style.display = st.hold ? "" : "none";
      status.textContent = st.hold ? "The model is about to move. Compare the grey and dark bars, then let it move." : win ? (((win.p === 1) === st.humanFirst) ? "You win." : "The model wins.")
        : t === W * H ? "Draw." : turnHuman ? "Your move: click a column." : "Model is thinking…";
    }

    function maybeModelMove() {
      if (st.hold) return;
      const { g } = boardOf(st.moves), t = st.moves.length;
      if (!winner(g) && t < W * H && ((t % 2 === 0) !== st.humanFirst)) setTimeout(() => { st.moves.push(modelMove()); recompute(); draw(); }, 250);
    }
    function play(c) {
      const { g, h } = boardOf(st.moves);
      if (winner(g) || h[c] >= H) return;
      st.moves.push(c); recompute(); draw(); maybeModelMove();
    }

    root.addEventListener("click", (e) => {
      const col = e.target.closest("[data-col]"), tog = e.target.closest(".c4-tog"), act = e.target.closest("[data-act]"), grp = e.target.closest("[data-grp]"), prt = e.target.closest("[data-part]");
      if (prt) { st.parts.delete(prt.dataset.part); recompute(); draw(); return; }
      if (tog) {
        const k = tog.dataset.k, kind = tog.dataset.kind, cur = st.iv.get(k);
        if (cur && cur.kind === kind) st.iv.delete(k); else st.iv.set(k, { kind, from: st.moves.length });
        recompute(); draw(); return;
      }
      if (grp) { st.groupOff.delete(grp.dataset.grp); recompute(); draw(); return; }
      if (act) {
        const a = act.dataset.act;
        if (a === "group") { st.groupOff.add($(".c4-sel").value); recompute(); draw(); return; }
        if (a === "go") { st.hold = false; draw(); maybeModelMove(); return; }
        if (a === "example") {
          const x = examples[+$(".c4-sele").value];
          st.moves = Array.from(x.moves, Number); st.humanFirst = x.t % 2 === 1; st.iv.clear(); st.groupOff.clear(); st.parts.clear(); st.parts.add(x.part);
          st.hold = true; recompute(); draw(); return;
        }
        if (a === "part") { st.parts.add($(".c4-selp").value); recompute(); draw(); return; }
        if (a === "clear") { st.iv.clear(); st.groupOff.clear(); st.parts.clear(); recompute(); draw(); return; }
        st.hold = false;
        if (a === "undo") st.moves.splice(Math.max(0, st.moves.length - 2));
        else { st.moves = []; st.humanFirst = a === "new1"; }
        recompute(); draw(); if (a !== "undo") maybeModelMove();
        return;
      }
      if (col) { const t = st.moves.length; if ((t % 2 === 0) === st.humanFirst) play(+col.dataset.col); }
    });
    root.addEventListener("change", (e) => {
      if (e.target.classList.contains("c4-selp")) $(".c4-pnote").textContent = partById[e.target.value].why;
      if (e.target.classList.contains("c4-sele")) $(".c4-enote").textContent = exText(examples[+e.target.value]);
    });
    root.addEventListener("mouseover", (e) => {
      const li = e.target.closest("li[data-k]"); const p = li ? byKey.get(li.dataset.k) : null;
      if (p !== st.focus) { st.focus = p; draw(); }
    });
    recompute(); draw();
    return { state: st, play };
  }

  global.C4Demo = { mount };
})(window);

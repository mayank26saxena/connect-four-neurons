// "The board in its head": play the model, read the board it believes in at every layer (linear probes on the residual
// stream), and edit that belief to see whether its move follows. Mount: C4MindsEye.mount(el, { base: "./" }).
// Needs c4model.js and worldmodel.js loaded first, and in `base`: model.json/.bin, worldmodel.json/.bin.
// Colours are relative to the player about to move: blue = their stones ("mine"), ochre = the opponent's ("theirs").
(function (global) {
  "use strict";
  const W = 7, H = 6, BOS = 7, EMPTY = 0, MINE = 1, THEIRS = 2;
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  const softmax = (lg, legal) => {
    let mx = -Infinity; for (let c = 0; c < W; c++) if (legal[c] && lg[c] > mx) mx = lg[c];
    const p = new Float32Array(W); let z = 0;
    for (let c = 0; c < W; c++) { p[c] = legal[c] ? Math.exp(lg[c] - mx) : 0; z += p[c]; }
    for (let c = 0; c < W; c++) p[c] /= z; return p;
  };
  const cellName = (k) => `column ${(k % W) + 1}, row ${Math.floor(k / W) + 1}`;
  const STATE = ["empty", "mine", "theirs"];

  // truth board relative to the player to move after `moves`: Int8Array(42), cell k = row * 7 + col, row 0 = bottom
  function relBoard(moves) {
    const b = new Int8Array(42), h = Array(W).fill(0), n = moves.length;
    moves.forEach((c, i) => { b[h[c] * W + c] = (i % 2) === (n % 2) ? MINE : THEIRS; h[c]++; });
    return { b, h };
  }
  function winner(b) {
    for (let r = 0; r < H; r++) for (let c = 0; c < W; c++) {
      const p = b[r * W + c]; if (!p) continue;
      for (const [dr, dc] of [[0, 1], [1, 0], [1, 1], [1, -1]]) {
        const cells = [0, 1, 2, 3].map((k) => [r + k * dr, c + k * dc]);
        if (cells.every(([rr, cc]) => rr >= 0 && rr < H && cc >= 0 && cc < W && b[rr * W + cc] === p)) return cells.map(([rr, cc]) => rr * W + cc);
      }
    }
    return null;
  }

  // Draw a board. cells[k] = { p: [pEmpty, pMine, pTheirs] } for beliefs, or { s: state } for the real board.
  function drawBoard(svg, cells, o = {}) {
    svg.innerHTML = "";
    const S = o.size || 50, R = S * 0.4, pad = o.pad == null ? 6 : o.pad;
    svg.setAttribute("viewBox", `0 0 ${W * S + 2 * pad} ${H * S + 2 * pad}`);
    el("rect", { x: 0, y: 0, width: W * S + 2 * pad, height: H * S + 2 * pad, rx: S * 0.14, class: "me-frame" }, svg);
    for (let k = 0; k < 42; k++) {
      const r = Math.floor(k / W), c = k % W, cx = pad + c * S + S / 2, cy = pad + (H - 1 - r) * S + S / 2;
      el("circle", { cx, cy, r: R, class: "me-hole" }, svg);
      const x = cells[k];
      if (x.p) {
        if (x.p[MINE] > 0.02) el("circle", { cx, cy, r: R, class: "me-mine", "fill-opacity": x.p[MINE].toFixed(3) }, svg);
        if (x.p[THEIRS] > 0.02) el("circle", { cx, cy, r: R, class: "me-theirs", "fill-opacity": x.p[THEIRS].toFixed(3) }, svg);
        if (o.truth && argmax(x.p) !== o.truth[k]) el("circle", { cx, cy, r: R + S * 0.04, class: "me-wrong" }, svg);
      } else if (x.s) el("circle", { cx, cy, r: R, class: x.s === MINE ? "me-mine" : "me-theirs" }, svg);
      if (o.threats) {
        const tm = o.threats[k], tt = o.threats[42 + k];
        if (tm > 0.5) el("circle", { cx, cy, r: R * 0.42, class: "me-thr-m", "fill-opacity": Math.min(1, tm).toFixed(2) }, svg);
        if (tt > 0.5) el("circle", { cx, cy, r: R * 0.42, class: "me-thr-t", "fill-opacity": Math.min(1, tt).toFixed(2) }, svg);
      }
      if (o.win && o.win.includes(k)) el("circle", { cx, cy, r: R * 0.25, class: "me-winmark" }, svg);
      if (o.edit && o.edit.cell === k) el("circle", { cx, cy, r: R + S * 0.06, class: "me-editring" }, svg);
      if (o.onCell) {
        const hit = el("rect", { x: pad + c * S, y: pad + (H - 1 - r) * S, width: S, height: S, class: "me-hit" }, svg);
        hit.addEventListener("click", () => o.onCell(k));
        el("title", {}, hit).textContent = o.title ? o.title(k) : cellName(k);
      }
    }
  }
  const argmax = (p) => (p[0] >= p[1] && p[0] >= p[2] ? 0 : p[1] >= p[2] ? 1 : 2);

  async function mount(root, opts = {}) {
    const base = opts.base || "./";
    root.classList.add("mindseye");
    root.innerHTML = `<div class="me-status">Loading the model (13 MB)…</div>`;
    const [model, meta, wbuf] = await Promise.all([
      C4Model.load(base + "model.json"),
      fetch(base + "worldmodel.json").then((r) => r.json()),
      fetch(base + "worldmodel.bin").then((r) => r.arrayBuffer()),
    ]);
    const wm = WorldModel.fromBuffer(meta, wbuf), NP = meta.points.length;
    const PT = { creates_win: "the edit gives the mover a win", creates_threat: "the edit gives the opponent a threat to block",
      removes_threat: "the edit removes the opponent's threat", other: "the edit changes the best move" };
    const st = { moves: [], humanFirst: true, layer: Math.min(3, NP - 1), edit: null, puzzle: null, threats: false, hold: false };

    root.innerHTML = `
      <div class="me-bar">
        <div class="me-btns">
          <button data-act="new1">New game: you start</button><button data-act="new2">Model starts</button>
          <button data-act="undo">Undo</button>
          <select class="me-puz"><option value="">Load an edit to try…</option>${meta.puzzles.map((p, i) => `<option value="${i}">${i + 1}. ${esc(PT[p.type])} (${p.followed ? "followed" : "ignored"})</option>`).join("")}</select>
        </div>
        <div class="me-status" aria-live="polite"></div>
      </div>
      <div class="me-grid">
        <figure class="me-panel"><figcaption>The real board<small>click a column to play</small></figcaption><svg class="me-real"></svg></figure>
        <figure class="me-panel"><figcaption>The board the model believes<small class="me-acc"></small></figcaption><svg class="me-belief"></svg>
          <label class="me-slider">Read at <input type="range" min="0" max="${NP - 1}" step="1" value="${Math.min(3, NP - 1)}"><b class="me-lname"></b></label>
          <label class="me-chk"><input type="checkbox" class="me-thr"> show the cells it reads as threats</label>
        </figure>
      </div>
      <div class="me-strip" aria-label="belief at every layer"></div>
      <div class="me-edit">
        <div class="me-h">Edit its belief <small>click a cell on the believed board: a stone switches colour, an empty landing cell gets a stone. Only the model's internal state changes, never the real board.</small></div>
        <div class="me-bars"></div>
        <p class="me-verdict"></p>
        <p class="me-fine">The examples are hand-picked to show both outcomes (three followed, one ignored, per kind). Across all ${meta.n_scored ? meta.n_scored.toLocaleString() : "scored"} edits like these, the model followed only a minority; see the write-up.</p>
        <div class="me-btns"><button data-act="clearedit">Clear the edit</button><button data-act="go" class="me-go" style="display:none">Let the model move</button></div>
      </div>
      <p class="me-legend"><span><i class="me-k-m"></i>stones of the player about to move</span><span><i class="me-k-t"></i>the opponent's stones</span><span><i class="me-k-w"></i>model's belief is wrong</span><span><i class="me-k-e"></i>edited cell</span></p>`;
    const $ = (s) => root.querySelector(s);
    const status = $(".me-status"), slider = $(".me-slider input");

    function forward(edit) {
      const tokens = [BOS, ...st.moves], at = st.moves.length;
      const o = edit ? { residHook: wm.editHook({ cell: edit.cell, src: edit.src, tgt: edit.tgt, at }) } : {};
      const out = model.forward(tokens, o);
      return { out, at, resid: out.resid.map((r) => r[at]) };
    }

    function render() {
      const { b, h } = relBoard(st.moves), win = winner(b), legal = h.map((x) => x < H);
      const humanTurn = (st.moves.length % 2 === 0) === st.humanFirst;
      const clean = forward(null), edited = st.edit ? forward(st.edit) : null;
      const cur = edited || clean;
      const pc = softmax(clean.out.logits[clean.at], legal), pe = edited ? softmax(edited.out.logits[edited.at], legal) : null;
      const beliefs = cur.resid.map((x, i) => wm.read(x, i));
      const cellsAt = (i) => Array.from({ length: 42 }, (_, k) => ({ p: [beliefs[i][k * 3], beliefs[i][k * 3 + 1], beliefs[i][k * 3 + 2]] }));
      const truth = Int8Array.from(b);
      if (st.edit) truth[st.edit.cell] = st.edit.tgt;
      // real board
      drawBoard($(".me-real"), Array.from(b, (s) => ({ s })), { win: win || [], onCell: (k) => play(k % W), title: (k) => `play column ${(k % W) + 1}` });
      // belief board at the chosen layer
      const i = st.layer;
      const wrong = Array.from({ length: 42 }, (_, k) => argmax(cellsAt(i)[k].p) !== truth[k]).filter(Boolean).length;
      drawBoard($(".me-belief"), cellsAt(i), { truth, edit: st.edit, threats: st.threats ? wm.threats(cur.resid[i], i) : null, onCell: clickBelief,
        title: (k) => `${cellName(k)}: believed ${STATE[argmax(cellsAt(i)[k].p)]} (${Math.round(100 * Math.max(...cellsAt(i)[k].p))}%)` });
      $(".me-lname").textContent = meta.points[i] === "embed" ? "the embeddings (before any layer)" : `after layer ${meta.points[i].slice(1)}`;
      $(".me-acc").textContent = `${42 - wrong} of 42 cells read correctly${st.edit ? " (against the edited board)" : ""}`;
      // strip: every layer
      const strip = $(".me-strip"); strip.innerHTML = "";
      for (let j = 0; j < NP; j++) {
        const f = document.createElement("button"); f.className = "me-mini" + (j === i ? " on" : "");
        const sv = document.createElementNS(NS, "svg"); f.appendChild(sv);
        const cj = cellsAt(j), wj = cj.filter((x, k) => argmax(x.p) !== truth[k]).length;
        drawBoard(sv, cj, { size: 16, pad: 2, truth, edit: st.edit });
        const cap = document.createElement("span"); cap.innerHTML = `${j === 0 ? "embed" : "L" + (j - 1)}<b>${42 - wj}/42</b>`; f.appendChild(cap);
        f.addEventListener("click", () => { st.layer = j; slider.value = j; render(); });
        strip.appendChild(f);
      }
      // move probabilities
      const bars = $(".me-bars"); bars.innerHTML = "";
      const pz = st.puzzle;
      for (let c = 0; c < W; c++) {
        const row = document.createElement("div"); row.className = "me-row" + (legal[c] ? "" : " illegal");
        const good = pz && st.edit && pz.cell === st.edit.cell && pz.tgt === st.edit.tgt;
        const tag = good ? (pz.best_edit.includes(c) ? `<em class="me-best e">best if edited</em>` : pz.best_real.includes(c) ? `<em class="me-best">best for real</em>` : "") : "";
        row.innerHTML = `<span>col ${c + 1}</span><div class="me-tr"><i class="c" style="width:${(100 * pc[c]).toFixed(1)}%"></i>${pe ? `<i class="e" style="width:${(100 * pe[c]).toFixed(1)}%"></i>` : ""}</div><span class="me-pv">${Math.round(100 * pc[c])}%${pe ? ` → ${Math.round(100 * pe[c])}%` : ""}</span>${tag}`;
        bars.appendChild(row);
      }
      const verdict = $(".me-verdict");
      if (!st.edit) verdict.innerHTML = `Grey: the model's move probabilities. Click a cell on the believed board to edit it; the edit is written into the residual stream from layer ${meta.start} on, at the current position only.`;
      else {
        const top = (p) => p.indexOf(Math.max(...p));
        const msg = `You edited ${cellName(st.edit.cell)} from <b>${STATE[st.edit.src]}</b> to <b>${STATE[st.edit.tgt]}</b>. Its move: column ${top(pc) + 1} → column ${top(pe) + 1}.`;
        let extra = "";
        if (pz && pz.cell === st.edit.cell && pz.tgt === st.edit.tgt) {
          const ok = pz.best_edit.includes(top(pe));
          extra = ` On the edited board the teacher's best move is column ${pz.best_edit.map((c) => c + 1).join(" or ")}${ok ? " — the model <b>followed its edited belief</b>." : " — the model <b>did not follow</b> this edit (it is one of the misses we keep in on purpose)."}`;
        }
        verdict.innerHTML = msg + extra;
      }
      // turn handling
      const over = !!win || st.moves.length === 42;
      if (over) status.textContent = win ? (humanTurn ? "The model won." : "You won.") : "Draw.";
      else if (humanTurn) status.textContent = "Your move.";
      else if (st.hold) status.textContent = "Position loaded. Edit a cell, or let the model move.";
      else status.textContent = "Model is thinking…";
      $(".me-go").style.display = !over && !humanTurn && st.hold ? "" : "none";
      if (!over && !humanTurn && !st.hold) setTimeout(() => modelMove(pe || pc), 350);
    }

    function clickBelief(k) {
      const { b, h } = relBoard(st.moves), r = Math.floor(k / W), c = k % W;
      if (b[k] !== EMPTY) st.edit = { cell: k, src: b[k], tgt: b[k] === MINE ? THEIRS : MINE };
      else if (r === h[c]) {
        const prev = st.edit && st.edit.cell === k ? st.edit.tgt : EMPTY;
        st.edit = prev === EMPTY ? { cell: k, src: EMPTY, tgt: MINE } : prev === MINE ? { cell: k, src: EMPTY, tgt: THEIRS } : null;
      } else { status.textContent = "That cell is floating: only stones and landing cells can be edited."; return; }
      st.hold = true; render();
    }
    function play(c) {
      const { h } = relBoard(st.moves), humanTurn = (st.moves.length % 2 === 0) === st.humanFirst;
      if (!humanTurn || h[c] >= H || winner(relBoard(st.moves).b)) return;
      st.moves.push(c); st.edit = null; st.puzzle = null; st.hold = false; render();
    }
    function modelMove(p) {
      const c = p.indexOf(Math.max(...p));
      st.moves.push(c); st.edit = null; st.puzzle = null; render();
    }
    function load(i) {
      const pz = meta.puzzles[i];
      st.moves = pz.moves.slice(); st.humanFirst = pz.moves.length % 2 === 1; st.puzzle = pz; st.hold = true;
      st.edit = null; render();
      status.textContent = `Loaded. Now click ${cellName(pz.cell)} on the believed board (it is ${STATE[pz.src]}; the edit makes it ${STATE[pz.tgt]}).`;
      setTimeout(() => { st.edit = { cell: pz.cell, src: pz.src, tgt: pz.tgt }; render(); }, 900);
    }
    root.addEventListener("click", (e) => {
      const a = e.target.closest("button[data-act]"); if (!a) return;
      const act = a.dataset.act;
      if (act === "new1" || act === "new2") { st.moves = []; st.humanFirst = act === "new1"; st.edit = null; st.puzzle = null; st.hold = false; render(); }
      if (act === "undo") { st.moves.splice(Math.max(0, st.moves.length - 2)); st.edit = null; st.puzzle = null; st.hold = false; render(); }
      if (act === "clearedit") { st.edit = null; render(); }
      if (act === "go") { st.hold = false; render(); }
    });
    slider.addEventListener("input", () => { st.layer = +slider.value; render(); });
    $(".me-thr").addEventListener("change", (e) => { st.threats = e.target.checked; render(); });
    $(".me-puz").addEventListener("change", (e) => { if (e.target.value !== "") load(+e.target.value); });
    render();
    return { load, state: st };
  }
  global.C4MindsEye = { mount, relBoard, drawBoard };
})(typeof window !== "undefined" ? window : globalThis);

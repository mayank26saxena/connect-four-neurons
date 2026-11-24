/* Connect Four neuron atlas. Loads data/overview.json (every pole, compact), per-layer files on demand, games.json (move strings),
   tactics.json (component effects, validation, emergence). No dependencies. Needs ../demo/concepts.js for concept text. */
(function () {
  "use strict";
  const D = "data/";
  const J = (f) => fetch(D + f).then((r) => r.json());
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const MINUS = "−";
  const sg = (v, d = 2) => (v < 0 ? MINUS : "") + Math.abs(v).toFixed(d);
  const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
  const TDEF = {
    win: ["Take the win", "A winning move exists; the right answer is a winning column."],
    block: ["Block", "No win available and the opponent threatens exactly one; the right answer is the blocking column."],
    poison: ["Avoid a poisoned column", "Some column would hand the opponent a win on top; the right answer is any other legal column."],
    fork: ["Make a fork", "A move creates two winning cells the opponent cannot both block; the right answer is a fork column."],
  };
  const FAMLAB = { cell: "board cell", land: "landing cell", line: "open line", opp_threat_r: "opponent's threat cell", my_threat_r: "own threat cell", last_col: "last-move column",
    full: "column full", ply: "game phase", block_now: "must block", win_now: "win now", poison: "poisoned column", teacher_best: "teacher's best move" };
  const FAMCOL = { cell: "#2563b0", land: "#2f8f83", line: "#7a4fb5", opp_threat_r: "#c9503a", my_threat_r: "#e08a6a", last_col: "#c4577f", full: "#5a8a2f", ply: "#8a9194",
    block_now: "#9b2f22", win_now: "#d09017", poison: "#6b4a2b", teacher_best: "#3a4a8a" };
  const OTHER = "#cfd4d2";
  let META, OV, TAC, GAMES, NAMES, NEU = [], DESC = [], LAYERS = {}, ROWS = [], TACS;

  const conceptText = (k) => C4Concepts.describe(NAMES[k]).text;  // concept indices refer to the full list (names.json), not meta.concepts
  const famName = (f) => FAMLAB[f] || f.replace(/_/g, " ");
  const poleId = (l, n, s) => `L${l}·N${n}${s ? MINUS : "+"}`;

  // ---------- boards ----------
  function replay(str, t) {
    const g = Array.from({ length: 6 }, () => Array(7).fill(0)), h = Array(7).fill(0); let last = null;
    for (let i = 0; i < t; i++) { const c = +str[i]; g[h[c]][c] = 1 + (i % 2); last = [h[c], c]; h[c]++; }
    return { g, last };
  }
  function boardSVG(g, last, t) {
    const mover = 1 + (t % 2); let s = `<svg viewBox="0 0 70 60"><rect x="0" y="0" width="70" height="60" rx="4" fill="#e4e8e7"/>`;
    for (let r = 0; r < 6; r++) for (let c = 0; c < 7; c++) {
      const v = g[r][c], col = v === 0 ? "#fafbfb" : v === mover ? "#2563b0" : "#d09017", ring = last && last[0] === r && last[1] === c;
      s += `<circle cx="${5 + c * 10}" cy="${5 + (5 - r) * 10}" r="4.2" fill="${col}"${ring ? ' stroke="#1b1f1d" stroke-width="1.4"' : ""}/>`;
    }
    return s + "</svg>";
  }
  function liftSVG(vals, label) {
    let s = `<svg viewBox="0 0 70 60"><rect x="0" y="0" width="70" height="60" rx="4" fill="#e4e8e7"/>`;
    for (let r = 0; r < 6; r++) for (let c = 0; c < 7; c++) {
      const v = vals[r * 7 + c], a = Math.min(1, Math.abs(v) / 45), col = v >= 0 ? "#2563b0" : "#c9503a";
      s += `<circle cx="${5 + c * 10}" cy="${5 + (5 - r) * 10}" r="4.2" fill="#fafbfb"/><circle cx="${5 + c * 10}" cy="${5 + (5 - r) * 10}" r="4.2" fill="${col}" opacity="${(0.08 + 0.92 * a).toFixed(2)}"><title>${label}: ${v > 0 ? "+" : v < 0 ? MINUS : ""}${Math.abs(v)} points</title></circle>`;
    }
    return s + "</svg>";
  }

  // ---------- data ----------
  function prepare() {
    const n = OV.layer.length, L = META.config.n_layer, F = META.config.d_ff;
    for (let l = 0; l < L; l++) NEU.push(Array.from({ length: F }, () => ({ f1: -1, fam: -1, c: -1, sign: 0, tac: null })));
    for (let i = 0; i < n; i++) {
      const o = NEU[OV.layer[i]][OV.neuron[i]];
      if (OV.f1[i] > o.f1) { o.f1 = OV.f1[i]; o.fam = OV.fam[i]; o.c = OV.c[i]; o.sign = OV.sign[i]; }
      o.tac = OV.tac[i];
    }
    DESC = new Array(n);
    const cache = NAMES.map((_, k) => conceptText(k).toLowerCase());
    for (let i = 0; i < n; i++) DESC[i] = `${cache[OV.c[i]]} ${META.families[OV.fam[i]]} l${OV.layer[i]} n${OV.neuron[i]}`;
    TACS = META.tactics;
  }
  const layerData = (l) => (LAYERS[l] ? Promise.resolve(LAYERS[l]) : J(`L${l}.json`).then((d) => (LAYERS[l] = d)));

  // ---------- tactics section ----------
  function tacticsSection() {
    const cols = TAC.columns, comps = TAC.components, drop = TAC.component_drop, ci = cols.length - 1;
    const spec = (j) => comps.map((c, i) => ({ c, v: drop[i][j] - drop[i][ci], d: drop[i][j] })).sort((a, b) => b.v - a.v);
    let h = '<div class="tcards">';
    TAC.tactics.forEach((t, j) => {
      const top = spec(j).slice(0, 3).filter((x) => x.v >= 0.01), val = TAC.neuron_validation[t].find((x) => x.k === 50) || TAC.neuron_validation[t][1];
      h += `<div class="tcard"><h3>${TDEF[t][0]}</h3><p class="def">${TDEF[t][1]}</p>
        <div class="acc">${Math.round(100 * TAC.intact[t])}%<small>chance ${Math.round(100 * TAC.chance[t])}% · ${TAC.n_positions[t][1].toLocaleString("en-US")} positions</small></div>
        <div class="lbl">Parts it depends on beyond the control</div><ul>${top.length ? top.map((x) => `<li><b>${x.c.name}</b>: ${sg(100 * x.d, 0)} points lost (control ${sg(100 * (x.d - x.v), 0)})</li>`).join("") : "<li>No single part stands out; every ablation of one part leaves it intact.</li>"}</ul>
        <div class="lbl">Most supportive neurons</div><div>${TAC.top_neurons[t].slice(0, 8).map((x) => `<button class="chip" data-l="${x.layer}" data-n="${x.neuron}">L${x.layer}·N${x.neuron}</button>`).join("")}</div>
        <p class="note">Switching off its top 50: ${Math.round(100 * val.top_rate)}% (50 random neurons: ${Math.round(100 * val.random_rate_mean)}%; control: ${Math.round(100 * val.control_rate_top)}%).</p></div>`;
    });
    h += "</div>";
    const shown = comps.map((c, i) => i).filter((i) => comps[i].kind === "mlp" || Math.max(...drop[i].slice(0, ci)) >= 0.08);
    h += `<div class="tscroll"><table class="heat"><thead><tr><th>Part ablated</th>${TAC.tactics.map((t) => `<th>${t}</th>`).join("")}<th class="ctrl">control</th></tr></thead><tbody>`;
    shown.forEach((i) => {
      h += `<tr><td>${comps[i].name}</td>${drop[i].map((v, j) => `<td class="${j === ci ? "ctrl" : ""}" style="background:rgba(37,99,176,${Math.min(0.75, Math.max(0, v) * 1.3).toFixed(2)})">${sg(100 * v, 0)}</td>`).join("")}</tr>`;
    });
    h += `</tbody></table></div><p class="hnote">Points of accuracy lost when one part's output is replaced by its average (mean ablation). ${shown.length} of ${comps.length} parts shown: every MLP, and every attention head that costs a tactic at least 8 points.</p>`;
    h += `<h3 style="margin-top:22px">When each tactic is learned</h3><div id="emerge"></div><p class="hnote">Accuracy of the greedy move on each tactic's positions, at 13 points in training. Poison avoidance is learned within 100 steps; the fork never gets above about 75%.</p>`;
    $("#tactics").innerHTML = h;
    $("#tactics").addEventListener("click", (e) => { const b = e.target.closest(".chip"); if (b) openNeuron(+b.dataset.l, +b.dataset.n); });
    emergence();
  }
  function emergence() {
    const E = TAC.emergence, W = 640, Hh = 210, L = 38, R = 96, T = 10, B = 30, ink = css("--ink-2");
    const x = (st) => L + (Math.log10(Math.max(st, 10)) - 1) / (Math.log10(8000) - 1) * (W - L - R), y = (v) => Hh - B - v * (Hh - B - T);
    const cl = { win: "#d09017", block: "#2563b0", poison: "#2f8f83", fork: "#c9503a", control: "#8a9194" };
    let s = `<svg viewBox="0 0 ${W} ${Hh}" style="width:100%;height:auto;overflow:visible">`;
    [0, 0.25, 0.5, 0.75, 1].forEach((v) => (s += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="${css("--rule")}"/><text x="${L - 6}" y="${y(v) + 3.5}" text-anchor="end" class="num" font-size="10.5">${Math.round(v * 100)}%</text>`));
    [10, 100, 1000, 8000].forEach((st) => (s += `<text x="${x(st)}" y="${Hh - 12}" text-anchor="middle" class="num" font-size="10.5">${st === 10 ? "0" : st.toLocaleString("en-US")}</text>`));
    s += `<text x="${(L + W - R) / 2}" y="${Hh - 0}" text-anchor="middle" font-size="10.5" fill="${ink}">training step (log scale)</text>`;
    const last = E.intact.length - 1; let ly = {};
    TAC.columns.forEach((c, j) => {
      s += `<polyline fill="none" stroke="${cl[c]}" stroke-width="${c === "control" ? 1.6 : 2.4}" ${c === "control" ? 'stroke-dasharray="4 3"' : ""} points="${E.steps.map((st, i) => `${x(st)},${y(E.intact[i][j])}`).join(" ")}"/>`;
      ly[c] = y(E.intact[last][j]);
    });
    const order = Object.keys(ly).sort((a, b) => ly[a] - ly[b]); order.forEach((c, i) => { if (i && ly[c] < ly[order[i - 1]] + 13) ly[c] = ly[order[i - 1]] + 13; });
    TAC.columns.forEach((c, j) => (s += `<text x="${W - R + 8}" y="${ly[c] + 4}" font-size="11.5" fill="${cl[c]}" font-weight="600">${c === "control" ? "control" : c} ${Math.round(100 * E.intact[last][j])}%</text>`));
    $("#emerge").innerHTML = s + "</svg>";
  }

  // ---------- landscape ----------
  function landscape() {
    const L = META.config.n_layer, F = META.config.d_ff, PW = 128, PH = F / PW, S = 8;
    $("#landscape").innerHTML = Array.from({ length: L }, (_, l) => `<div class="lrow"><span>L${l}</span><canvas id="cv${l}" width="${PW * S}" height="${PH * S}"></canvas></div>`).join("");
    const sel = $("#colorBy");
    sel.innerHTML = `<option value="fam">best-matching concept family</option>` + TACS.map((t, j) => `<option value="t${j}">support for: ${TDEF[t][0].toLowerCase()}</option>`).join("");
    const maxAbs = TACS.map((_, j) => Math.max(...NEU.flat().map((o) => Math.abs(o.tac ? o.tac[j] : 0))) || 1);
    const draw = () => {
      const mode = sel.value;
      for (let l = 0; l < L; l++) {
        const ctx = $(`#cv${l}`).getContext("2d"); ctx.clearRect(0, 0, PW * S, PH * S);
        for (let j = 0; j < F; j++) {
          const o = NEU[l][j], gx = (j % PW) * S, gy = Math.floor(j / PW) * S;
          if (mode === "fam") { ctx.globalAlpha = 0.25 + 0.75 * Math.min(1, Math.max(0, o.f1) / 0.8); ctx.fillStyle = FAMCOL[META.families[o.fam]] || OTHER; }
          else { const v = o.tac[+mode.slice(1)] / maxAbs[+mode.slice(1)]; ctx.globalAlpha = Math.min(1, 0.06 + Math.abs(v) * 3.2); ctx.fillStyle = v >= 0 ? "#2563b0" : "#c9503a"; }
          ctx.fillRect(gx + 0.5, gy + 0.5, S - 1, S - 1);
        }
      }
      ctxLegend(mode);
    };
    const ctxLegend = (mode) => {
      $("#legend").innerHTML = mode === "fam" ? Object.entries(FAMCOL).map(([f, c]) => `<span><i style="background:${c}"></i>${famName(f)}</span>`).join("") + `<span><i style="background:${OTHER}"></i>other</span>`
        : `<span><i style="background:#2563b0"></i>supports the tactic</span><span><i style="background:#c9503a"></i>works against it</span><span>brighter = stronger first-order effect</span>`;
    };
    sel.onchange = draw; draw();
    for (let l = 0; l < L; l++) {
      const cv = $(`#cv${l}`), at = (e) => { const r = cv.getBoundingClientRect(), j = Math.floor(((e.clientY - r.top) / r.height) * PH) * PW + Math.floor(((e.clientX - r.left) / r.width) * PW); return Math.max(0, Math.min(F - 1, j)); };
      cv.onclick = (e) => openNeuron(l, at(e));
      cv.onmousemove = (e) => { const j = at(e), o = NEU[l][j]; tipShow(e, `<b>${poleId(l, j, o.sign)}</b><br>${esc(conceptText(o.c))}<br>F1 ${o.f1.toFixed(2)}`); };
      cv.onmouseleave = () => tipHide();
    }
  }
  let tip;
  function tipShow(e, html) {
    if (!tip) { tip = document.createElement("div"); tip.className = "tip"; document.body.appendChild(tip); }
    tip.innerHTML = html; tip.style.opacity = 1; tip.style.left = Math.min(e.clientX + 14, innerWidth - tip.offsetWidth - 8) + "px"; tip.style.top = e.clientY + 14 + "px";
  }
  const tipHide = () => { if (tip) tip.style.opacity = 0; };

  // ---------- browse ----------
  function browse() {
    const L = META.config.n_layer;
    $("#layer").insertAdjacentHTML("beforeend", Array.from({ length: L }, (_, l) => `<option value="${l}">layer ${l}</option>`).join(""));
    $("#sort").innerHTML = `<option value="f1">best concept match (F1)</option><option value="rate">how often it fires</option>` + TACS.map((t, j) => `<option value="t${j}">supports: ${TDEF[t][0].toLowerCase()}</option>`).join("");
    const run = () => {
      const q = $("#q").value.trim().toLowerCase().split(/\s+/).filter(Boolean), layer = $("#layer").value, pole = $("#pole").value, sort = $("#sort").value, out = [];
      for (let i = 0; i < OV.layer.length; i++) {
        if (layer !== "" && OV.layer[i] !== +layer) continue;
        if (pole !== "" && OV.sign[i] !== +pole) continue;
        if (q.length && !q.every((w) => DESC[i].includes(w))) continue;
        out.push(i);
      }
      const key = sort === "f1" ? (i) => OV.f1[i] : sort === "rate" ? (i) => OV.rate[i] : (i) => OV.tac[i][+sort.slice(1)];
      out.sort((a, b) => key(b) - key(a));
      ROWS = out;
      $("#count").textContent = `${out.length.toLocaleString("en-US")} poles match; showing the first ${Math.min(80, out.length)}.`;
      $("#rows").innerHTML = out.slice(0, 80).map((i) => `<li data-i="${i}"><span class="id">${poleId(OV.layer[i], OV.neuron[i], OV.sign[i])}</span><span class="t">${esc(conceptText(OV.c[i]))}<small>${esc(famName(META.families[OV.fam[i]]))} · fires on ${(100 * OV.rate[i]).toFixed(1)}% of positions</small></span><span class="f">${OV.f1[i].toFixed(2)}</span></li>`).join("");
    };
    ["q", "layer", "pole", "sort"].forEach((id) => ($("#" + id).oninput = run));
    $("#rows").onclick = (e) => { const li = e.target.closest("li"); if (li) openPole(OV.layer[+li.dataset.i], OV.neuron[+li.dataset.i], OV.sign[+li.dataset.i]); };
    run();
  }

  // ---------- detail ----------
  const openNeuron = (l, n) => openPole(l, n, NEU[l][n].sign);
  function openPole(l, n, s) {
    layerData(l).then((recs) => {
      const r = recs[n], P = r.poles[s], other = r.poles[1 - s];
      const cands = P.C.map((k, i) => `<li>${esc(conceptText(k))} <b>F1 ${P.F1[i].toFixed(2)}</b></li>`).join("");
      const bar = (label, v, scale, title) => { const w = Math.min(50, (Math.abs(v) / scale) * 50); return `<div class="bar" title="${title || ""}"><span>${label}</span><span class="tr"><em></em><i style="${v >= 0 ? `left:50%;width:${w}%;background:#2563b0` : `right:50%;width:${w}%;background:#c9503a`}"></i></span><span>${sg(v, 2)}</span></div>`; };
      const dsg = s === 0 ? 1 : -1, dle = r.dle.map((v) => v * dsg);  // a negative pole fires at negative activation, so its effect flips sign
      const dmax = Math.max(...dle.map(Math.abs), 1e-6);
      let h = `<div class="poletabs">${[0, 1].map((k) => `<button data-s="${k}" class="${k === s ? "on" : ""}"><b>${poleId(l, n, k)}</b>${esc(conceptText(r.poles[k].C[0]))}</button>`).join("")}</div>`;
      h += `<p class="big">Fires when ${esc(conceptText(P.C[0]).replace(/^./, (c) => c.toLowerCase()))}.</p><ul class="note" style="padding-left:18px">${cands}</ul>`;
      h += `<div class="kv"><span>fires on <b>${(100 * P.rate).toFixed(1)}%</b> of positions</span><span>average move number <b>${P.ply.toFixed(0)}</b></span><span>threshold <b>${sg(P.thr, 2)}</b></span><span>range p0.5 to p99.5 <b>${sg(r.q[0], 1)} to ${sg(r.q[4], 1)}</b></span></div>`;
      h += `<h4>What the board looks like when it fires</h4><div class="boards"><div class="bd">${liftSVG(P.occ.slice(0, 42), "mover's stone")}mover's stone</div><div class="bd">${liftSVG(P.occ.slice(42, 84), "opponent's stone")}opponent's stone</div><div class="bd">${liftSVG(P.occ.slice(84, 126), "empty")}empty</div></div><p class="note">Blue: more likely than usual when this pole fires; red: less likely. Colour strength is the change in points, saturating at 45.</p>`;
      h += `<h4>Direct effect on the next move</h4>${dle.map((v, c) => bar(`column ${c + 1}`, v, dmax, "Through the output layer, before later layers act on it")).join("")}<p class="note">What this pole does to each column's score when it fires, centred across columns. Only the direct path through the output layer: later layers can change it.</p>`;
      const tmax = TACS.map((_, j) => Math.max(...OV.tac.map((a) => Math.abs(a[j]))) || 1);
      h += `<h4>Support for each tactic</h4>${TACS.map((t, j) => bar(t, r.tac[j], tmax[j], "first-order effect of zeroing this neuron on the tactic's log-odds")).join("")}<p class="note">Positive: zeroing this neuron makes the tactic less likely. Scale is the largest value among all neurons.</p>`;
      h += `<h4>Where it fires most</h4><div class="exg">${P.ex.map(([g, t, a]) => { const b = replay(GAMES[g], t); const nx = GAMES[g][t]; return `<div class="ex">${boardSVG(b.g, b.last, t)}move ${t + 1} · activation ${sg(a, 1)}${nx !== undefined ? `<br>played column ${+nx + 1}` : ""}</div>`; }).join("")}</div><p class="note">Stones: blue is the player about to move, ochre the opponent; the ring marks the last move.</p>`;
      const o2 = other.F1[0];
      h += `<p class="note">The other pole of this neuron matches “${esc(conceptText(other.C[0]))}” (F1 ${o2.toFixed(2)}).</p>`;
      $("#dtitle").textContent = poleId(l, n, s); $("#dbody").innerHTML = h; $("#dbody").scrollTop = 0;
      document.body.classList.add("open"); $("#drawer").setAttribute("aria-hidden", "false");
      history.replaceState(null, "", `#L${l}.N${n}.${s}`);
      $("#dbody").querySelectorAll(".poletabs button").forEach((b) => (b.onclick = () => openPole(l, n, +b.dataset.s)));
    });
  }
  function close() { document.body.classList.remove("open"); $("#drawer").setAttribute("aria-hidden", "true"); history.replaceState(null, "", location.pathname); }
  $("#dclose").onclick = close; $("#scrim").onclick = close; addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });

  Promise.all([J("meta.json"), J("overview.json"), J("tactics.json"), J("games.json"), J("names.json")]).then(([m, o, t, g, nm]) => {
    META = m; OV = o; TAC = t; GAMES = g; NAMES = nm;
    prepare();
    const c = META.config;
    $("#card").innerHTML = `<span><b>${c.n_layer}</b> layers</span><span><b>${c.d_model}</b> wide</span><span><b>${c.n_head}</b> heads</span><span><b>${c.d_ff.toLocaleString("en-US")}</b> SwiGLU neurons per layer</span><span><b>${(META.n_params / 1e6).toFixed(2)}M</b> parameters</span><span>${META.n_games.toLocaleString("en-US")} held-out games · ${META.n_positions.toLocaleString("en-US")} positions</span>`;
    tacticsSection(); landscape(); browse();
    const m2 = location.hash.match(/^#L(\d+)\.N(\d+)(?:\.(\d))?$/); if (m2) openPole(+m2[1], +m2[2], m2[3] ? +m2[3] : NEU[+m2[1]][+m2[2]].sign);
  }).catch((e) => { $("#card").innerHTML = `<span>Could not load the atlas data: ${esc(e.message)}</span>`; });
})();

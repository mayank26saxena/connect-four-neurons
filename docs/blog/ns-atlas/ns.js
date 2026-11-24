// Neuron Scientist atlas page. Data: window.NS from data/ns.js (scripts/33_ns_atlas_export.py). Every number comes from there.
(function () {
  "use strict";
  const D = window.NS, U = D.units, T = D.totals, S = D.studies;
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const f2 = (x) => (x == null ? "–" : x.toFixed(2));
  const g3 = (x) => (x == null ? "–" : Number(x.toPrecision(3)).toString());
  const pc = (x) => (x == null ? "–" : Math.round(100 * x) + "%");
  const concept = (name) => (window.C4Concepts ? C4Concepts.describe(name).text : name);
  const real = U.filter((u) => u.kind === "neuron");

  // ---------- header
  $("#meta-counts").textContent = `${T.real} real neurons, ${T.controls} random-direction controls`;
  const ctrlGood = U.filter((u) => u.kind !== "neuron" && u.f1 >= D.bar);
  const r = S.r, q = S.q;

  // ---------- boards
  function boardSVG(moves, size = 14) {
    const h = Array(7).fill(0), cells = [], n = moves.length;
    moves.forEach((c, i) => { cells.push([h[c], c, (i % 2) === (n % 2)]); h[c]++; });
    const W = 7 * size + 4, H = 6 * size + 4;
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="board after ${n} moves"><rect x="0" y="0" width="${W}" height="${H}" rx="3" fill="#e4e8e7"/>`;
    for (let r = 0; r < 6; r++) for (let c = 0; c < 7; c++) s += `<circle cx="${2 + c * size + size / 2}" cy="${2 + (5 - r) * size + size / 2}" r="${size * 0.4}" fill="#fafbfb"/>`;
    cells.forEach(([r, c, mine], i) => {
      const cx = 2 + c * size + size / 2, cy = 2 + (5 - r) * size + size / 2;
      s += `<circle cx="${cx}" cy="${cy}" r="${size * 0.4}" fill="${mine ? "var(--me)" : "var(--op)"}"/>`;
      if (i === n - 1) s += `<circle cx="${cx}" cy="${cy}" r="${size * 0.16}" fill="#fff"/>`;
    });
    return s + "</svg>";
  }

  // ---------- cards
  const CAT = { verified: "Well described", below: "Below the bar", control: "Random-direction control" };
  function metric(label, value, sub, frac, half) {
    const bar = frac == null ? "" : `<div class="bar"><i style="width:${Math.max(0, Math.min(1, frac)) * 100}%"></i>${half ? "<em></em>" : ""}</div>`;
    return `<div class="metric"><b>${value}</b>${bar}<span>${label}${sub ? "<br>" + sub : ""}</span></div>`;
  }
  function card(u) {
    const who = u.kind === "neuron" ? `Layer ${u.layer} · neuron ${u.neuron} · ${u.pole === "+" ? "positive" : "negative"} pole` : `Layer ${u.layer} · random direction`;
    const badges = `<span class="badge ${u.cat}">${CAT[u.cat]}</span>` + (u.opening ? `<span class="badge open" title="${pc(u.early_share)} of the positions where its rule fires have fewer than 4 stones (post-hoc label)">Opening unit</span>` : "") +
      `<span class="badge conf">confidence: ${esc(u.confidence)}</span>`;
    const judge = u.judge == null ? "–" : pc(u.judge);
    const metrics = metric("held-out F1", f2(u.f1), `AUROC ${f2(u.auroc)}`, u.f1) +
      metric("dictionary", f2(u.dict_f1), esc(concept(u.dict_concept)), u.dict_f1) +
      metric("judge", judge, `${u.judge_pairs} pairs, chance 50%`, u.judge, true) +
      metric("simulation", u.sim_share == null ? "–" : pc(u.sim_share), "of a perfect reader", u.sim_share) +
      metric("synthesis", u.synth_beats ? "beats max" : "below max", `best ${g3(u.synth_best)} vs ${g3(u.dev_max)}`, null);
    let boards = "";
    if (u.examples.length) {
      boards = `<div class="boards"><div class="lbl">Strongest firings in recorded games</div>` +
        u.examples.map((e) => `<figure>${boardSVG(e.moves)}<figcaption>${e.moves.length} stone${e.moves.length === 1 ? "" : "s"} · ${g3(u.pole === "-" ? -e.act : e.act)}</figcaption></figure>`).join("") + "</div>";
    } else if (u.synthesis.length) {
      boards = `<div class="boards"><div class="lbl">Positions the agent built to make it fire</div>` +
        u.synthesis.map((m) => `<figure>${boardSVG(m)}<figcaption>${m.length} stone${m.length === 1 ? "" : "s"}</figcaption></figure>`).join("") + "</div>";
    }
    const top = u.steer.map((v, c) => [v, c]).sort((a, b) => Math.abs(b[0]) - Math.abs(a[0]))[0];
    const measured = Math.abs(top[0]) >= 0.01 ? `measured: forcing it high moves column ${top[1]} by ${top[0] > 0 ? "+" : ""}${Math.round(top[0] * 100)} points on average` : "measured: no average effect above 1 point";
    return `<article class="card" id="${u.id}"><header><span class="uid">${who}</span><span class="src">study ${u.study} · ${u.unit}</span>${badges}</header>
      <p class="desc">${esc(u.description)}</p><div class="metrics">${metrics}</div>${boards}
      <p class="effect"><b>Effect.</b> ${esc(u.effect || "not stated")} <span class="src">(${measured})</span></p>
      <details><summary>Rule and lab notes</summary><pre>${esc(u.program)}</pre><p class="notes">${esc(u.notes)}</p></details></article>`;
  }

  // ---------- filters
  const layerSel = $("#f-layer");
  for (let l = 0; l < 6; l++) layerSel.insertAdjacentHTML("beforeend", `<option value="${l}">${l}</option>`);
  let shown = 30;
  function list() {
    const cat = $("#f-cat").value, l = $("#f-layer").value, st = $("#f-study").value, qy = $("#f-q").value.trim().toLowerCase(), so = $("#f-sort").value;
    let xs = U.filter((u) => (cat === "all" || u.cat === cat) && (l === "" || u.layer === +l) && (st === "" || u.study === st) &&
      (!qy || (u.description + " " + u.effect + " " + concept(u.dict_concept)).toLowerCase().includes(qy)));
    // opening units (post-hoc label) sort after the others so an artefact is never the first card
    const key = { f1: (u) => -(u.f1 || 0), layer: (u) => u.layer * 10 - (u.f1 || 0), judge: (u) => -(u.judge || 0) }[so];
    const k2 = (u) => (u.opening ? 100 : 0) + key(u);
    xs.sort((a, b) => k2(a) - k2(b));
    $("#count").textContent = `${xs.length} unit${xs.length === 1 ? "" : "s"}` + (cat === "verified" ? ` (${xs.filter((u) => u.opening).length} opening units)` : "");
    $("#cards").innerHTML = xs.slice(0, shown).map(card).join("") + (xs.length > shown ? `<button class="more" id="more">Show ${Math.min(30, xs.length - shown)} more</button>` : "");
    const m = $("#more"); if (m) m.addEventListener("click", () => { shown += 30; list(); });
  }
  ["#f-cat", "#f-layer", "#f-study", "#f-sort"].forEach((s) => $(s).addEventListener("change", () => { shown = 30; list(); }));
  $("#f-q").addEventListener("input", () => { shown = 30; list(); });
  list();

  // ---------- predictions table
  const P = [
    ["a", "Unexplained neurons: agent beats the concept list by ≥ 0.15 F1", (p) => `+${f2(p.q_a.median_agent_minus_dict)}`, "q_a"],
    ["b", "Explained neurons: agent within 0.05 of the concept list or better", (p) => `${f2(p.q_b.agent)} vs ${f2(p.q_b.dict)}`, "q_b"],
    ["c", "Real neurons ≥ 0.20 F1 above random directions, and half of the random ones rated low", (p) => `${p.q_c.real_minus_random_f1 >= 0 ? "+" : ""}${f2(p.q_c.real_minus_random_f1)}; ${pc(p.q_c.random_low_confidence_rate)} low`, "q_c"],
    ["d", "Simulation recovers ≥ 50% of a perfect reader (median)", (p) => (p.q_d.real_sim_share_median == null ? "undefined" : pc(p.q_d.real_sim_share_median)), "q_d"],
    ["e", "Text-only judge ≥ 80% on real neurons", (p) => `${pc(p.q_e.real_mean)} (random ${pc(p.q_e.random_mean)})`, "q_e"],
    ["f", "(r) only: half of real neurons above the random directions' 90th percentile", (p) => (p.r_f ? `${pc(p.r_f.real_frac_above_random_p90)}` : "–"), "r_f"],
  ];
  const cell = (p, k, fn) => (p[k] ? `${fn(p)} <span class="${p[k].holds ? "held" : "failed"}">${p[k].holds ? "held" : "failed"}</span>` : "–");
  $("#preds").innerHTML = `<thead><tr><th></th><th>Prediction</th><th>Study (q)</th><th>Study (r)</th></tr></thead><tbody>` +
    P.map(([id, txt, fn, k]) => `<tr><td>${id}</td><td>${txt}</td><td>${cell(q.predictions, k, fn)}</td><td>${cell(r.predictions, k, fn)}</td></tr>`).join("") + "</tbody>";
  $("#opening-note").textContent = `Opening units (post-hoc, not pre-registered): ${D.opening_rule}. ${T.verified_opening} of the ${T.verified} well-described real neurons and ${T.controls_ge_bar_opening} of the ${ctrlGood.length} well-described random directions are opening units, all from study (q).`;
})();

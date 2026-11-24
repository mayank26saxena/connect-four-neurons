/* Dependency-free SVG charts for the Connect Four neurons post. Styling comes from tokens.css.
   Each chart takes a container, a data object from window.FIGURES, and an optional <tbody> for an accessible data table. */
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
  const MINUS = "−";
  const num = (x, d = 0) => (x < 0 ? MINUS : "") + Math.abs(x).toFixed(d);
  const el = (tag, attrs = {}, parent) => { const e = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); if (parent) parent.appendChild(e); return e; };
  const text = (p, x, y, s, a = {}) => { const t = el("text", Object.assign({ x, y }, a), p); t.textContent = s; return t; };
  const lin = (d0, d1, r0, r1) => (v) => r0 + ((v - d0) / (d1 - d0)) * (r1 - r0);

  let tip;
  function tooltip(target, html) {
    if (!tip) { tip = document.createElement("div"); tip.className = "tip"; document.body.appendChild(tip); }
    target.addEventListener("mousemove", (e) => {
      tip.innerHTML = html; tip.style.opacity = 1;
      tip.style.left = Math.min(e.clientX + 14, innerWidth - tip.offsetWidth - 8) + "px"; tip.style.top = e.clientY + 14 + "px";
    });
    target.addEventListener("mouseleave", () => { tip.style.opacity = 0; });
  }

  // draw(width) is re-run whenever the container's width changes
  function mount(container, draw) {
    let last = -1;
    const run = () => { const w = Math.max(280, Math.floor(container.clientWidth)); if (w === last) return; last = w; container.innerHTML = ""; draw(w); };
    run();
    if ("ResizeObserver" in window) new ResizeObserver(run).observe(container);
  }
  const fillTable = (tbody, rows) => { if (tbody) tbody.innerHTML = rows.map((r) => "<tr>" + r.map((c, i) => `<td${i ? ' class="n"' : ""}>${c}</td>`).join("") + "</tr>").join(""); };
  const svgIn = (c, w, h) => el("svg", { viewBox: `0 0 ${w} ${h}`, role: "img" }, c);
  const axisY = (g, y, x0, x1, ticks, fmt) => ticks.forEach((t) => {
    el("line", { x1: x0, x2: x1, y1: y(t), y2: y(t), class: "grid-l", stroke: css("--rule"), "stroke-width": 1 }, g);
    text(g, x0 - 6, y(t) + 3.5, fmt(t), { "text-anchor": "end", class: "num" });
  });

  // ---- Figure 1: diverging bars, neurons minus random directions, by concept family ----
  function families(container, rows, tbody) {
    fillTable(tbody, rows.map((r) => [r.label + (r.readable_from_embeddings ? " *" : ""), r.neurons, r.rotation]));
    mount(container, (w) => {
      const narrow = w < 480, labW = narrow ? 128 : 220, valW = narrow ? 74 : 96, rowH = narrow ? 40 : 34, top = 22;
      const h = top + rows.length * rowH + 22, x0 = labW, x1 = w - valW - 8;
      const diffs = rows.map((r) => r.neurons - r.rotation);
      const lo = Math.floor(Math.min(0, ...diffs) / 200) * 200, hi = Math.ceil(Math.max(0, ...diffs) / 100) * 100 + 100;
      const x = lin(lo, hi, x0, x1);
      const s = svgIn(container, w, h);
      for (let t = lo; t <= hi; t += 200) { el("line", { x1: x(t), x2: x(t), y1: top - 6, y2: h - 18, stroke: css("--rule") }, s); text(s, x(t), h - 4, (t > 0 ? "+" : t < 0 ? MINUS : "") + Math.abs(t), { "text-anchor": "middle", class: "num" }); }
      el("line", { x1: x(0), x2: x(0), y1: top - 6, y2: h - 18, stroke: css("--axis"), "stroke-width": 1.5 }, s);
      text(s, x1 + 8, 12, "neurons / random", { class: "num", "text-anchor": "start" });
      rows.forEach((r, i) => {
        const y = top + i * rowH + rowH / 2, d = r.neurons - r.rotation, win = d > 0;
        const lab = r.label + (r.readable_from_embeddings ? " *" : "");
        const t = text(s, 0, y + 4, lab, { "font-size": narrow ? 11.5 : 13 });
        if (narrow && lab.length > 18) { t.textContent = ""; const parts = lab.split(" "); const mid = Math.ceil(parts.length / 2); [parts.slice(0, mid).join(" "), parts.slice(mid).join(" ")].forEach((p, k) => { const ts = el("tspan", { x: 0, dy: k ? 13 : -3 }, t); ts.textContent = p; }); }
        el("rect", { x: Math.min(x(0), x(d)), y: y - 8, width: Math.max(1.5, Math.abs(x(d) - x(0))), height: 16, rx: 1.5, fill: win ? css("--accent") : css("--ink-2") }, s);
        text(s, x1 + 8, y + 4, `${r.neurons} / ${r.rotation}`, { class: "num", "text-anchor": "start", "font-size": 12 });
        const hit = el("rect", { x: 0, y: y - rowH / 2, width: w, height: rowH, class: "hit" }, s);
        tooltip(hit, `<b>${r.label}</b><br>neurons: ${r.neurons} poles<br>random directions: ${r.rotation} poles${r.readable_from_embeddings ? "<br><i>readable from embeddings</i>" : ""}`);
      });
    });
  }

  // ---- Figure 2: three small multiples over width ----
  function sweep(container, data, tbody) {
    const W = data.widths, P = data.panels;
    fillTable(tbody, W.map((w, i) => [w.toLocaleString("en-US"), ...P.map((p) => p.values[i].map((v) => num(v * p.scale, 1)).join(" / "))]));
    mount(container, (w) => {
      const cols = w >= 640 ? 3 : 1, pw = Math.floor((w - (cols - 1) * 18) / cols), ph = 190, gh = cols === 1 ? 3 * (ph + 14) : ph + 14;
      const s = svgIn(container, w, gh);
      P.forEach((p, pi) => {
        const ox = cols === 1 ? 0 : pi * (pw + 18), oy = cols === 1 ? pi * (ph + 14) : 0;
        const g = el("g", { transform: `translate(${ox},${oy})` }, s);
        const vals = p.values.flat().map((v) => v * p.scale), mn = Math.min(0, ...vals), mx = Math.max(...vals);
        const pad = (mx - mn) * 0.15 || 1, d0 = mn < 0 ? mn - pad : Math.max(0, mn - pad), d1 = mx + pad;
        const step = [1, 2, 5, 10, 20, 25, 50].find((t) => (d1 - d0) / t <= 4) || 50;
        const ticks = []; for (let t = Math.ceil(d0 / step) * step; t <= d1; t += step) ticks.push(t);
        const L = 40, R = 14, T = 38, B = 34, x = lin(0, W.length - 1, L, pw - R), y = lin(d0, d1, ph - B, T);
        const t1 = text(g, 0, 12, p.title, { "font-weight": 600, "font-size": 12.5 }); if (pw < 260) t1.setAttribute("font-size", 11.5);
        text(g, 0, 27, p.unit, { class: "num", "text-anchor": "start" });
        axisY(g, y, L, pw - R, ticks, (t) => num(t, step < 1 ? 1 : 0));
        if (d0 < 0 && d1 > 0) el("line", { x1: L, x2: pw - R, y1: y(0), y2: y(0), stroke: css("--axis"), "stroke-width": 1.5 }, g);
        W.forEach((wd, i) => text(g, x(i), ph - 14, wd.toLocaleString("en-US"), { "text-anchor": "middle", class: "num" }));
        text(g, (L + pw - R) / 2, ph - 1, "neurons per layer", { "text-anchor": "middle", class: "num" });
        const means = p.values.map((v) => (v[0] + v[1]) / 2 * p.scale);
        el("polyline", { points: means.map((m, i) => `${x(i)},${y(m)}`).join(" "), fill: "none", stroke: css("--accent"), "stroke-width": 2.2 }, g);
        p.values.forEach((v, i) => {
          v.forEach((val) => el("circle", { cx: x(i), cy: y(val * p.scale), r: 4, fill: css("--card"), stroke: css("--accent"), "stroke-width": 1.5 }, g));
          el("circle", { cx: x(i), cy: y(means[i]), r: 3.6, fill: css("--accent") }, g);
          const hit = el("rect", { x: x(i) - 14, y: T - 6, width: 28, height: ph - B - T + 10, class: "hit" }, g);
          tooltip(hit, `<b>${W[i].toLocaleString("en-US")} neurons per layer</b><br>seed 1: ${num(v[0] * p.scale, 1)}<br>seed 2: ${num(v[1] * p.scale, 1)}<br>mean: ${num(means[i], 1)}`);
        });
        [0, W.length - 1].forEach((i) => {  // end-point values, placed clear of the seed circles
          const ys = p.values[i].map((v) => y(v * p.scale)), neg = means[i] < 0;
          text(g, x(i) + (i === 0 ? 4 : 2), neg ? Math.max(...ys) + 17 : Math.min(...ys) - 9, (means[i] > 0 && p.key === "gap" ? "+" : "") + num(means[i], 1), { class: "num", "text-anchor": i === 0 ? "start" : "end", "font-weight": 600 });
        });
      });
    });
  }

  // ---- Figure 3: group ablation, 2 x 2 grid ----
  function group(container, data, tbody) {
    const ks = data.ks;
    fillTable(tbody, ks.map((k, i) => [k, num(data.concepts.block.off[i] * 100, 0) + "%", num(data.concepts.block.random[i] * 100, 0) + "%", num(data.concepts.block.on[i] * 100, 0) + "%"]));
    const panels = [
      { c: "block", mode: "off", title: "Must block: top-k neurons switched off", base: "intact", dots: "off_cols", main: "off", note: "blocking rate" },
      { c: "block", mode: "on", title: "Must block: top-k neurons forced on", base: "false_intact", dots: "on_cols", main: "on", note: "plays the column anyway" },
      { c: "win", mode: "off", title: "Win now: top-k neurons switched off", base: "intact", dots: "off_cols", main: "off", note: "win-taking rate" },
      { c: "win", mode: "on", title: "Win now: top-k neurons forced on", base: "false_intact", dots: "on_cols", main: "on", note: "plays the column anyway" }];
    mount(container, (w) => {
      const cols = w >= 600 ? 2 : 1, pw = Math.floor((w - (cols - 1) * 22) / cols), ph = 200, rows = Math.ceil(panels.length / cols);
      const s = svgIn(container, w, rows * (ph + 14));
      panels.forEach((p, pi) => {
        const d = data.concepts[p.c], ox = (pi % cols) * (pw + 22), oy = Math.floor(pi / cols) * (ph + 14);
        const g = el("g", { transform: `translate(${ox},${oy})` }, s);
        const L = 38, R = 10, T = 34, B = 34, x = lin(0, ks.length - 1, L, pw - R), y = lin(0, 1, ph - B, T);
        text(g, 0, 12, p.title, { "font-weight": 600, "font-size": pw < 280 ? 11 : 12.5 });
        text(g, 0, 26, p.note, { class: "num", "text-anchor": "start" });
        axisY(g, y, L, pw - R, [0, 0.5, 1], (t) => Math.round(t * 100) + "%");
        ks.forEach((k, i) => { if (i % 2 === 0 || pw > 330) text(g, x(i), ph - 14, k, { "text-anchor": "middle", class: "num" }); });
        text(g, (L + pw - R) / 2, ph - 1, "k neurons", { "text-anchor": "middle", class: "num" });
        el("line", { x1: L, x2: pw - R, y1: y(d[p.base]), y2: y(d[p.base]), stroke: css("--muted"), "stroke-dasharray": "4 3" }, g);
        text(g, pw - R, y(d[p.base]) + (p.mode === "off" ? -5 : 12), (p.mode === "off" ? "intact " : "baseline ") + Math.round(d[p.base] * 100) + "%", { "text-anchor": "end", class: "num" });
        if (p.mode === "off") {
          el("polyline", { points: d.random.map((v, i) => `${x(i)},${y(v)}`).join(" "), fill: "none", stroke: "#8a9194", "stroke-width": 2 }, g);
          d.random.forEach((v, i) => el("circle", { cx: x(i), cy: y(v), r: 3, fill: "#8a9194" }, g));
        }
        d[p.dots].forEach((cols7, i) => cols7.forEach((v) => el("circle", { cx: x(i), cy: y(v), r: 2, fill: css("--accent"), opacity: 0.28 }, g)));
        el("polyline", { points: d[p.main].map((v, i) => `${x(i)},${y(v)}`).join(" "), fill: "none", stroke: css("--accent"), "stroke-width": 2.4 }, g);
        d[p.main].forEach((v, i) => {
          el("circle", { cx: x(i), cy: y(v), r: 3.6, fill: css("--accent") }, g);
          const hit = el("rect", { x: x(i) - 12, y: T - 4, width: 24, height: ph - B - T + 8, class: "hit" }, g);
          tooltip(hit, `<b>k = ${ks[i]}</b><br>top-k: ${Math.round(v * 100)}%` + (p.mode === "off" ? `<br>random: ${Math.round(d.random[i] * 100)}%` : "") + `<br>baseline: ${Math.round(d[p.base] * 100)}%`);
        });
      });
    });
  }

  // ---- Figure 4: behaviour against neuron alignment over training ----
  function dynamics(container, rows, tbody) {
    fillTable(tbody, rows.map((r) => [r.step.toLocaleString("en-US"), Math.round(r.block * 100) + "%", Math.round(r.win * 100) + "%"]));
    mount(container, (w) => {
      const h = w < 480 ? 330 : 280, L = 40, R = w < 480 ? 12 : 120, T = 14, B = 40, narrow = w < 480;
      const s = svgIn(container, w, h);
      const sx = (st) => Math.log10(Math.max(st, 10)), x = lin(1, Math.log10(8000), L, w - R), y = lin(0, 1, h - B, T);
      axisY(s, y, L, w - R, [0, 0.25, 0.5, 0.75, 1], (t) => Math.round(t * 100) + "%");
      [10, 100, 1000, 8000].forEach((t) => text(s, x(Math.log10(t)), h - 22, t === 10 ? "0" : t.toLocaleString("en-US"), { "text-anchor": "middle", class: "num" }));
      text(s, (L + w - R) / 2, h - (narrow ? 38 : 6), "training step (log scale)", { "text-anchor": "middle", class: "num" });
      const series = [
        { k: "block", c: css("--accent"), dash: "", name: "blocks threats", lab: "blocks" },
        { k: "f1_block", c: css("--accent"), dash: "5 4", name: "best 'must block' neuron, F1", lab: "neuron F1" },
        { k: "win", c: css("--c-soft"), dash: "", name: "takes available wins", lab: "takes wins" },
        { k: "f1_win", c: css("--c-soft"), dash: "5 4", name: "best 'win now' neuron, F1", lab: "neuron F1" }];
      const last = rows[rows.length - 1], ly = {};
      series.map((sr) => [sr.k, y(last[sr.k])]).sort((a, b) => a[1] - b[1]).forEach((e, i, arr) => { ly[e[0]] = i && e[1] < ly[arr[i - 1][0]] + 14 ? ly[arr[i - 1][0]] + 14 : e[1]; });
      series.forEach((sr) => {
        el("polyline", { points: rows.map((r) => `${x(sx(r.step))},${y(r[sr.k])}`).join(" "), fill: "none", stroke: sr.c, "stroke-width": 2.4, "stroke-dasharray": sr.dash }, s);
        if (!narrow) text(s, w - R + 8, ly[sr.k] + 4, `${sr.lab} ${last[sr.k].toFixed(2)}`, { "text-anchor": "start", "font-size": 11.5, fill: sr.k.includes("win") ? css("--t-soft") : css("--t-explicit") });
      });
      rows.forEach((r) => {
        const hit = el("rect", { x: x(sx(r.step)) - 8, y: T, width: 16, height: h - B - T, class: "hit" }, s);
        tooltip(hit, `<b>step ${r.step.toLocaleString("en-US")}</b><br>blocks ${Math.round(r.block * 100)}% · best neuron F1 ${r.f1_block.toFixed(2)}<br>takes wins ${Math.round(r.win * 100)}% · best neuron F1 ${r.f1_win.toFixed(2)}`);
      });
      if (narrow) { [["solid: behaviour, dashed: best neuron F1", 0], ["blue: must block · ochre: win now", 14]].forEach(([t, dy]) => text(s, L, h - 6 + dy - 14, t, { class: "num", "text-anchor": "start" })); }
    });
  }

  window.C4Charts = { families, sweep, group, dynamics };
})();

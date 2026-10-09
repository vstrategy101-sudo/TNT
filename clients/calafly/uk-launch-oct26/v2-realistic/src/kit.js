// CalaFly realistic kit: procedural scene painters + HTML builders for phone UI and props.
(function () {
  const K = {};

  K.COUNTRIES = {
    usa:    { key: "usa", name: "the USA", short: "USA", tag: "USA", code: "JFK", city: "NEW YORK", board: "NEW YORK", plan: "USA eSIM", sky: "usa", wall: ["#1d2b64", "#f8a170", "#6a3093"] },
    turkey: { key: "turkey", name: "Turkey", short: "Turkey", tag: "Turkey", code: "AYT", city: "ANTALYA", board: "ANTALYA", plan: "Turkey eSIM", sky: "turkey", wall: ["#0b6e8a", "#5fd4c4", "#f6e7b0"] },
    dubai:  { key: "dubai", name: "Dubai", short: "Dubai", tag: "Dubai", code: "DXB", city: "DUBAI", board: "DUBAI", plan: "Dubai eSIM", sky: "dubai", wall: ["#3a1c71", "#d76d77", "#ffaf7b"] },
  };

  // ---------- noise ----------
  function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
  function makeNoise(seed) {
    const r = rng(seed), N = 256, p = new Float32Array(N * N);
    for (let i = 0; i < N * N; i++) p[i] = r();
    const sm = t => t * t * (3 - 2 * t);
    return (x, y) => {
      const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
      const a = p[((yi & 255) * N) + (xi & 255)], b = p[((yi & 255) * N) + ((xi + 1) & 255)];
      const c = p[(((yi + 1) & 255) * N) + (xi & 255)], d = p[(((yi + 1) & 255) * N) + ((xi + 1) & 255)];
      const u = sm(xf), v = sm(yf);
      return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
    };
  }
  function fbm(n, x, y, oct = 5) { let s = 0, a = 0.5, f = 1, t = 0; for (let i = 0; i < oct; i++) { s += a * n(x * f, y * f); t += a; a *= 0.5; f *= 2.03; } return s / t; }
  const hex = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  const mix = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
  function grad(stops, t) { // stops: [[pos, "#hex"], ...]
    for (let i = 0; i < stops.length - 1; i++) {
      const [p0, c0] = stops[i], [p1, c1] = stops[i + 1];
      if (t <= p1) return mix(hex(c0), hex(c1), (t - p0) / (p1 - p0 || 1));
    }
    return hex(stops[stops.length - 1][1]);
  }

  // ---------- sky / landscape painter ----------
  const SKIES = {
    dubai:  { stops: [[0, "#1f2f5a"], [0.38, "#6b5b8e"], [0.62, "#e8875a"], [0.8, "#ffc98f"], [1, "#ffe2b8"]], sun: [0.62, 0.78, "#fff1d0"], cloud: "#ffd8b8", cloudAmt: 0.42, ground: "dunes" },
    turkey: { stops: [[0, "#1d6fd1"], [0.45, "#4fa3ea"], [0.66, "#a9dcff"], [0.7, "#d9f2ff"], [1, "#d9f2ff"]], sun: [0.25, 0.18, "#ffffff"], cloud: "#ffffff", cloudAmt: 0.5, ground: "sea" },
    usa:    { stops: [[0, "#0d1636"], [0.45, "#30366e"], [0.68, "#8a5c8e"], [0.82, "#f09a6a"], [1, "#ffcf9a"]], sun: [0.7, 0.86, "#ffd9a8"], cloud: "#b9a6d8", cloudAmt: 0.38, ground: "lights" },
  };
  K.paintSky = function (cv, kind, seed = 7) {
    const w = cv.width, h = cv.height, ctx = cv.getContext("2d"), S = SKIES[kind];
    const img = ctx.createImageData(w, h), d = img.data, n = makeNoise(seed), n2 = makeNoise(seed + 11);
    const horizon = S.ground === "sea" ? 0.68 : S.ground === "dunes" ? 0.8 : 0.84;
    for (let y = 0; y < h; y++) {
      const ty = y / h;
      for (let x = 0; x < w; x++) {
        const tx = x / w;
        let c = grad(S.stops, Math.min(ty / horizon, 1) * 0.999);
        // sun glow
        const dx = tx - S.sun[0], dy = (ty - S.sun[1]) * 1.4, r = Math.sqrt(dx * dx + dy * dy);
        c = mix(c, hex(S.sun[2]), Math.max(0, 0.9 - r * 2.2) ** 2);
        // clouds (stretched fbm, thicker towards the horizon)
        if (ty < horizon) {
          const f = fbm(n, tx * 5.5, ty * 14 + 3, 6);
          const band = 0.35 + 0.65 * Math.min(1, ty / horizon + 0.15);
          const a = Math.max(0, (f - (1 - S.cloudAmt)) * 3.2) * band;
          const lit = mix(hex(S.cloud), [255, 255, 255], Math.max(0, 0.6 - r));
          c = mix(c, lit, Math.min(0.92, a));
        }
        // ground
        if (S.ground === "sea" && ty >= horizon) {
          const t = (ty - horizon) / (1 - horizon);
          c = mix(hex("#2a8fb5"), hex("#0a4f72"), Math.pow(t, 0.7));
          const glint = fbm(n2, tx * 60, t * 220, 3);
          c = mix(c, [255, 255, 255], Math.max(0, glint - 0.66) * 2.6 * (1 - t) * (1 - Math.abs(tx - S.sun[0]) * 1.4));
        } else if (S.ground === "dunes") {
          const dune = horizon - 0.06 * fbm(n2, tx * 3, 1, 3) - 0.02 * Math.sin(tx * 9);
          if (ty >= dune) { const t = (ty - dune) / (1 - dune); c = mix(hex("#c97a4a"), hex("#5a2e22"), Math.pow(t, 0.55)); c = mix(c, hex("#ffc98f"), 0.25 * (1 - t)); }
        } else if (S.ground === "lights" && ty >= horizon) {
          const t = (ty - horizon) / (1 - horizon);
          c = mix(hex("#2a2140"), hex("#0c0a16"), t);
        }
        // haze at horizon
        c = mix(c, hex(S.stops[S.stops.length - 2][1]), Math.max(0, 0.35 - Math.abs(ty - horizon) * 4) * 0.6);
        const g = (n2(x * 0.9, y * 0.9) - 0.5) * 6; // film grain
        const i = (y * w + x) * 4; d[i] = c[0] + g; d[i + 1] = c[1] + g; d[i + 2] = c[2] + g; d[i + 3] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);
    if (S.ground === "lights") { // distant city lights bokeh (no skyline)
      const r = rng(seed + 3);
      for (let i = 0; i < 260; i++) {
        const x = r() * w, y = h * (0.86 + r() * 0.12), s = 1 + r() * r() * w * 0.012;
        const col = r() < 0.7 ? "255,206,140" : "255,255,235";
        const gr = ctx.createRadialGradient(x, y, 0, x, y, s * 2.2);
        gr.addColorStop(0, `rgba(${col},${0.55 + r() * 0.4})`); gr.addColorStop(1, `rgba(${col},0)`);
        ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(x, y, s * 2.2, 0, 7); ctx.fill();
      }
    }
  };

  K.paintFabric = function (cv, base = "#c9c3b8", seed = 5) {
    const w = cv.width, h = cv.height, ctx = cv.getContext("2d"), img = ctx.createImageData(w, h), d = img.data, n = makeNoise(seed), b = hex(base);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const weave = (Math.sin(x * 2.6) * 0.5 + Math.sin(y * 2.9) * 0.5) * 2.5;
      const slub = (fbm(n, x * 0.015, y * 0.25, 3) - 0.5) * 12 + (fbm(n, x * 0.25, y * 0.015, 3) - 0.5) * 10 + (fbm(n, x * 0.006, y * 0.006, 3) - 0.5) * 30;
      const light = 1.12 - 0.42 * Math.hypot(x / w - 0.25, y / h - 0.2);
      const v = weave + slub + (Math.random() - 0.5) * 10;
      const i = (y * w + x) * 4; d[i] = (b[0] + v) * light; d[i + 1] = (b[1] + v) * light; d[i + 2] = (b[2] + v) * light; d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
  };

  K.paintWood = function (cv, seed = 9) {
    const w = cv.width, h = cv.height, ctx = cv.getContext("2d"), img = ctx.createImageData(w, h), d = img.data, n = makeNoise(seed);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const t = fbm(n, x * 0.004, y * 0.06, 4);
      const ring = Math.sin(t * 40 + y * 0.02) * 0.5 + 0.5;
      let c = mix(hex("#b9875a"), hex("#8a5a35"), ring * 0.7 + (t - 0.5));
      const light = 1.1 - 0.45 * Math.hypot(x / w - 0.3, y / h - 0.25);
      const g = (Math.random() - 0.5) * 8;
      const i = (y * w + x) * 4; d[i] = c[0] * light + g; d[i + 1] = c[1] * light + g; d[i + 2] = c[2] * light + g; d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
  };

  K.paintWall = function (cv, cols, seed = 2) { // iOS-like wallpaper: soft colour blobs
    const w = cv.width, h = cv.height, ctx = cv.getContext("2d"), r = rng(seed);
    ctx.fillStyle = cols[0]; ctx.fillRect(0, 0, w, h);
    for (let i = 0; i < 7; i++) {
      const x = r() * w, y = r() * h, s = (0.4 + r() * 0.6) * w;
      const g = ctx.createRadialGradient(x, y, 0, x, y, s);
      g.addColorStop(0, cols[1 + (i % (cols.length - 1))] + "cc"); g.addColorStop(1, cols[1 + (i % (cols.length - 1))] + "00");
      ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    }
    const sh = ctx.createLinearGradient(0, 0, 0, h); sh.addColorStop(0, "rgba(0,0,0,.18)"); sh.addColorStop(0.5, "rgba(0,0,0,0)"); sh.addColorStop(1, "rgba(0,0,0,.25)");
    ctx.fillStyle = sh; ctx.fillRect(0, 0, w, h);
  };

  K.paintCamera = function (cv) { // out-of-focus living room with a laptop showing the QR
    const w = cv.width, h = cv.height, ctx = cv.getContext("2d");
    const g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, "#5b5550"); g.addColorStop(0.55, "#8d8379"); g.addColorStop(1, "#4a4440");
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    ctx.filter = "blur(18px)";
    ctx.fillStyle = "#f2d9a6"; ctx.beginPath(); ctx.arc(w * 0.85, h * 0.12, w * 0.12, 0, 7); ctx.fill(); // lamp
    ctx.fillStyle = "#3a3632"; ctx.fillRect(-20, h * 0.72, w + 40, h * 0.4); // sofa arm
    ctx.filter = "blur(2px)";
    // laptop screen (bright) holding the QR
    const sx = w * 0.12, sy = h * 0.22, sw = w * 0.76, sh = sw * 0.66;
    ctx.fillStyle = "#1c1d20"; ctx.fillRect(sx - 10, sy - 10, sw + 20, sh + 20);
    ctx.fillStyle = "#f7f8fa"; ctx.fillRect(sx, sy, sw, sh);
    const Q = window.QR, m = Q.length, qs = sh * 0.62, cell = qs / m, qx = sx + (sw - qs) / 2, qy = sy + (sh - qs) / 2 + sh * 0.04;
    ctx.fillStyle = "#0b0d10";
    for (let r = 0; r < m; r++) for (let c = 0; c < m; c++) if (Q[r][c]) ctx.fillRect(qx + c * cell, qy + r * cell, cell + 0.5, cell + 0.5);
    ctx.fillStyle = "#18c8a8"; ctx.fillRect(sx, sy, sw, sh * 0.07);
    ctx.filter = "none";
    const v = ctx.createRadialGradient(w / 2, h / 2, w * 0.3, w / 2, h / 2, w * 0.9); v.addColorStop(0, "rgba(0,0,0,0)"); v.addColorStop(1, "rgba(0,0,0,.45)");
    ctx.fillStyle = v; ctx.fillRect(0, 0, w, h);
  };

  // ---------- HTML builders ----------
  const tickSvg = (c = "#0b0d10") => `<svg viewBox="0 0 24 24" fill="none" stroke="${c}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg>`;
  K.tickSvg = tickSvg;
  K.logo = (cls = "") => `<div class="logo ${cls}"><span class="dot"></span><span>CA<span class="la">LA</span></span></div>`;
  K.minilogo = `<span class="minilogo"><span class="dot"></span><span>CA<span class="la">LA</span></span></span>`;

  K.sbar = ({ light = false, time = "9:41", carrier = "", weak = false } = {}) => `
    <div class="sbar ${light ? "light" : ""}"><span>${carrier ? `<span class="carrier">${carrier}</span>` : time}</span>
      <span class="r"><span class="sig ${weak ? "weak" : ""}"><i></i><i></i><i></i><i></i></span><span class="bat"><i></i></span></span></div>`;

  K.iphone = (screen, { flat = false, id = "" } = {}) => `
    <div class="iphone ${flat ? "flat" : ""}" ${id ? `id="${id}"` : ""}>
      <span class="btn l1"></span><span class="btn l2"></span><span class="btn l3"></span><span class="btn r1"></span>
      <div class="bezel"><div class="screen">${screen}<div class="island"></div><div class="glare"></div></div></div>
    </div>`;

  K.notif = ({ icon = "chat", title, body, time = "now", style = "" }) => {
    const ic = icon === "app" ? `<span class="ic appicon"></span>`
      : `<span class="ic" style="background:linear-gradient(160deg,#6be37a,#2fbf4a);display:grid;place-items:center"><svg width="26" height="26" viewBox="0 0 24 24"><path fill="#fff" d="M12 3C6.5 3 2 6.6 2 11c0 2.4 1.3 4.6 3.5 6.1L5 21l4.1-2.3c.9.2 1.9.3 2.9.3 5.5 0 10-3.6 10-8s-4.5-8-10-8z"/></svg></span>`;
    return `<div class="notif" style="${style}">${ic}<div class="tx"><b>${title}<span>${time}</span></b>${body}</div></div>`;
  };

  K.lockScreen = (C, notifs = "", { date = "Friday 17 October", time = "14:05" } = {}) => `
    <div class="lock"><canvas class="wall" width="300" height="640" data-wall="${C.key}" style="width:100%;height:100%"></canvas>
      ${K.sbar({ light: true, carrier: "CalaFly" })}
      <div class="date">${date}</div><div class="clock">${time}</div>
      <div class="nstack" style="position:absolute;left:0;right:0;top:300px">${notifs}</div>
      <div class="bottom"><i></i><i></i></div><div class="home"></div></div>`;

  K.web = (inner, { dark = false } = {}) => `
    <div class="app ${dark ? "dark" : ""}">${K.sbar({ light: dark })}
      <div class="nav">${K.minilogo}<span class="burger"></span></div>
      <div class="body">${inner}</div>
      <div class="urlbar"><span class="lk"></span>calafly.net</div><div class="homebar"></div></div>`;

  K.showOffer = false;
  K.offer = (C) => (K.showOffer && window.OFFERS) ? window.OFFERS.get(C.key) : null;

  K.screenOrder = (C) => { const o = K.offer(C), O = window.OFFERS; return K.web(`
    <span class="chip">${C.tag}</span>
    <h3>Order<br><span class="hl">confirmed.</span></h3>
    <div class="card2">
      <div class="row2"><span>Plan</span><b>${C.plan}${o ? " · " + o.data : ""}</b></div>
      <div class="row2"><span>Covers</span><b>${o ? o.days + " days" : "Your whole trip"}</b></div>
      ${o ? `<div class="row2"><span>Paid once</span><b style="font:800 30px CFD;letter-spacing:-.03em">${O.price(C.key)}</b></div>` : `<div class="row2"><span>Payment</span><b class="ok">One-off ✓</b></div>`}
      <div class="row2"><span>Daily charges</span><b class="ok">None ✓</b></div>
      ${o && o.code ? `<div class="row2"><span>New customer code</span><b style="background:var(--yellow);border-radius:6px;padding:0 6px">${o.code} −${o.pct}%</b></div>` : `<div class="row2"><span>Install</span><b>Scan QR code</b></div>`}
    </div>
    <div class="bigbtn" style="margin-top:4px">Install eSIM</div>`); };

  K.screenRefund = (C) => K.web(`
    <span class="chip">My eSIMs</span>
    <div class="card2" style="display:flex;gap:14px;align-items:center">
      <span class="appicon" style="width:52px;height:52px;border-radius:14px;flex:0 0 auto"></span>
      <div style="flex:1"><b style="font:800 22px CFD;letter-spacing:-.02em">${C.plan}</b><div style="font:500 14.5px UI;color:#59616b;margin-top:2px">Bought for your trip</div></div>
    </div>
    <div class="card2">
      <div class="row2"><span>Status</span><b style="color:#c2410c">Unused</b></div>
      <div class="row2"><span>Refund</span><b class="ok">100% guaranteed ✓</b></div>
    </div>
    <div class="bigbtn" id="refundbtn" style="background:var(--pink);color:var(--ink)">Request refund</div>
    <div style="font:500 13px/1.35 UI;color:#59616b;text-align:center">100% refund if your eSIM is unused. T&amp;Cs apply.</div>`);

  K.screenPick = (C) => K.web(`
    <span class="chip">Where to?</span>
    <h3>Pick your<br><span class="hl">destination.</span></h3>
    ${[["usa", "USA", "JFK · MCO · LAX"], ["turkey", "Turkey", "IST · AYT · DLM"], ["dubai", "Dubai", "DXB"]].map(([k, n, codes]) => `
      <div class="card2 pick" data-k="${k}" style="display:flex;align-items:center;gap:14px;padding:12px 14px;transition:none">
        <span style="font:800 26px CFD;letter-spacing:-.03em;flex:1">${n}<span style="display:block;font:500 13px UI;color:#59616b;letter-spacing:0;margin-top:2px">${codes} · one price, whole trip</span></span>
        <span class="tick pk" style="opacity:0">${tickSvg()}</span>
      </div>`).join("")}
    <div class="bigbtn" id="pickbtn">Continue</div>`);

  K.screenPlan = (C) => { const o = K.offer(C), O = window.OFFERS; return K.web(`
    <span class="chip">${C.tag}</span>
    <h3>${C.short} data,<br><span class="hl">sorted.</span></h3>
    <div class="card2" style="display:grid;gap:10px">
      ${o ? `<div style="display:flex;align-items:baseline;justify-content:space-between;border-bottom:1.5px dashed #c9d1d8;padding-bottom:8px"><span style="font:600 15px UI;color:#59616b">${o.data} · ${o.days} days</span><b style="font:800 40px CFD;letter-spacing:-.04em">${O.price(C.key)}</b></div>` : ""}
      ${["Set up in minutes", "Pay once, not per day", "100% refund if unused"].map(t => `<div style="display:flex;gap:10px;align-items:center;font:600 16.5px UI"><span class="tick">${tickSvg()}</span>${t}</div>`).join("")}
    </div>
    <div class="bigbtn">Get Calafly</div>
    <div style="font:500 12.5px/1.35 UI;color:#59616b;text-align:center">Data-only eSIM. Unlocked, eSIM-compatible phone needed.</div>`); };

  K.screenCamera = (C, { progress = 0.65, sheet = true, pill = "eSIM QR code" } = {}) => `
    <div class="camera"><canvas width="300" height="640" data-cam="1"></canvas>
      <div class="reticle"><i></i><i></i><i></i><i></i></div>
      <div class="campill" style="top:${sheet ? 470 : 560}px">${pill}</div>
      ${K.sbar({ light: true })}
      ${sheet ? `<div class="sheet" id="esimsheet"><div class="grab"></div><div class="simic"></div>
        <h4>Activating eSIM</h4><p>CalaFly · ${C.plan}</p>
        <div class="bar"><i id="esimbar" style="width:${progress * 100}%"></i></div></div>` : ""}
      <div class="homebar" style="background:#fff"></div></div>`;

  K.boardingPass = (C, style = "") => `
    <div class="pass" style="${style}">
      <div class="hd"><span>BOARDING PASS</span><b>CALAFLY</b></div>
      <div class="rt"><div><small>FROM</small><b>LON</b></div><div class="pl">✈</div><div><small>TO</small><b>${C.code}</b></div></div>
      <div class="meta"><div><small>DATA</small><b>READY</b></div><div><small>PAID</small><b>${K.offer(C) ? window.OFFERS.price(C.key) + " ONCE" : "ONCE"}</b></div><div><small>SEAT</small><b>23A</b></div></div>
      <div class="stub"><div class="bc"></div></div></div>`;

  K.laptopQR = (style = "") => {
    const Q = window.QR, m = Q.length;
    let rects = ""; for (let r = 0; r < m; r++) for (let c = 0; c < m; c++) if (Q[r][c]) rects += `<rect x="${c}" y="${r}" width="1.02" height="1.02"/>`;
    return `<div class="laptop" style="${style}"><div class="lid"><div class="disp">
      <div style="height:40px;background:var(--ink);display:flex;align-items:center;padding:0 16px;color:#fff">${K.minilogo}</div>
      <div style="display:flex;gap:26px;align-items:center;padding:30px 34px">
        <div style="flex:1"><div class="chip" style="margin-bottom:12px">Install</div><div style="font:800 40px/1 CFD;letter-spacing:-.04em;color:var(--ink)">Scan to<br><span style="color:var(--pink)">install.</span></div>
          <div style="font:500 15px/1.4 UI;color:#59616b;margin-top:12px">Open your camera and point it at the code.</div></div>
        <svg class="qrsvg" viewBox="-2 -2 ${m + 4} ${m + 4}" width="280" height="280" style="background:#fff;border:3px solid var(--ink);border-radius:14px;box-shadow:6px 6px 0 var(--teal)"><g fill="#0b0d10">${rects}</g></svg>
      </div></div></div><div class="base"></div></div>`;
  };

  K.board = (C, style = "") => {
    const flaps = (txt, n, cls = "") => `<div class="flaps">${txt.padEnd(n).slice(0, n).split("").map(ch => `<span class="flap ${cls}">${ch === " " ? "&nbsp;" : ch}</span>`).join("")}</div>`;
    const rows = [["NEW YORK", "JFK", "09:40", "BOARDING", "usa"], ["ANTALYA", "AYT", "10:15", "ON TIME", "turkey"], ["DUBAI", "DXB", "10:55", "ON TIME", "dubai"], ["ORLANDO", "MCO", "11:30", "ON TIME", "x"], ["ISTANBUL", "IST", "12:05", "ON TIME", "x"]];
    return `<div class="board" style="${style}"><div class="ttl">DEPARTURES <span>LONDON</span></div>
      ${rows.map(([city, code, t, st, k]) => `<div class="r ${k === C.key ? "hi" : ""}">${flaps(t, 5, "y")}${flaps(city, 9)}${flaps(code, 3, "y")}${flaps(st, 8, k === C.key ? "g" : "")}</div>`).join("")}
    </div>`;
  };

  // paint every canvas placeholder in a subtree
  K.paintAll = function (root = document) {
    root.querySelectorAll("canvas[data-sky]").forEach(c => K.paintSky(c, c.dataset.sky, +(c.dataset.seed || 7)));
    root.querySelectorAll("canvas[data-wall]").forEach(c => K.paintWall(c, K.COUNTRIES[c.dataset.wall].wall));
    root.querySelectorAll("canvas[data-fabric]").forEach(c => K.paintFabric(c, c.dataset.fabric));
    root.querySelectorAll("canvas[data-wood]").forEach(c => K.paintWood(c));
    root.querySelectorAll("canvas[data-cam]").forEach(c => K.paintCamera(c));
  };

  window.K = K;
})();

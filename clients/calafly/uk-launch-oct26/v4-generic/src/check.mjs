// Flags any scene object that reaches into the footer (small print + CTA) or off the canvas.
import { createRequire } from "module"; import path from "path"; import { fileURLToPath } from "url";
const require = createRequire(import.meta.url); const { chromium } = require("/opt/node-tools/node_modules/playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
for (const k of ["pack", "number", "bill", "refund", "global"]) {
  await p.goto(`file://${here}/generic.html?k=${k}`); await p.waitForSelector("body[data-ready='1']");
  const r = await p.evaluate(() => {
    const foot = [...document.querySelectorAll(".foot .small, .foot .cta")].map(e => e.getBoundingClientRect());
    const txt = [...document.querySelectorAll(".txt h1, .txt .tag, .top .lockup, .top .url")].map(e => e.getBoundingClientRect());
    const hit = (a, b) => Math.min(a.right, b.right) - Math.max(a.left, b.left) > 2 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 2;
    const out = [];
    document.querySelectorAll(".scene > *").forEach((e, i) => { const r = e.getBoundingClientRect();
      if (foot.some(f => hit(r, f))) out.push(`#${i} ${e.className} × footer`);
      if (txt.some(f => hit(r, f))) out.push(`#${i} ${e.className} × headline`);
      if (r.right > 1081 || r.left < -1) out.push(`#${i} off canvas`); });
    return out; });
  console.log(k, r.length ? r.join("; ") : "clear");
}
await b.close();

// Flags any two pieces of copy (or copy and a scene/object) whose boxes overlap, on every static.
// Usage: node check-overlap.mjs [country]   — checks round 1 (src/creative.html) and round 2 (v2-realistic/src/creative.html)
import { createRequire } from "module";
import path from "path";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const country = process.argv[2] || "usa";
const SETS = [
  [`${here}/creative.html`, ["intro", "ease", "price", "refund", "stack", "retarget"]],
  [`${here}/../v2-realistic/src/creative.html`, ["wheels", "setup", "payonce", "refund", "still"]],
];
const SIZES = { "1x1": [1080, 1080], "4x5": [1080, 1350], "9x16": [1080, 1920], "191x1": [1200, 628] };
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 1920 } });
let issues = 0;
for (const [file, concepts] of SETS) for (const k of concepts) for (const [s, [W, H]] of Object.entries(SIZES)) {
  await page.goto(`file://${file}?c=${country}&k=${k}&s=${s}`);
  await page.waitForSelector("body[data-ready='1']");
  await page.waitForTimeout(50);
  const found = await page.evaluate(([W, H]) => {
    const T = [".lockup", ".tag", "h1", ".sub", ".pline", ".small", ".cta", ".url", ".bigprice", ".codechip"];
    const V = [".visual > *", ".sticker", ".card", ".ticket"];
    const pick = sels => sels.flatMap(q => [...document.querySelectorAll("#ad " + q)])
      .filter(e => e.offsetParent !== null && getComputedStyle(e).display !== "none" && e.getBoundingClientRect().width > 0)
      .map(e => ({ e, r: ["H1", "P"].includes(e.tagName) ? (() => { const g = document.createRange(); g.selectNodeContents(e); return g.getBoundingClientRect(); })() : e.getBoundingClientRect(), n: e.className ? "." + String(e.className).split(" ")[0] : e.tagName.toLowerCase() }));
    const t = pick(T), v = pick(V), out = [];
    const hit = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) * Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
    const rel = (a, b) => a.e.contains(b.e) || b.e.contains(a.e);
    for (let i = 0; i < t.length; i++) {
      for (let j = i + 1; j < t.length; j++) if (!rel(t[i], t[j]) && hit(t[i].r, t[j].r) > 20) out.push(`${t[i].n} × ${t[j].n}`);
      for (const o of v) if (!rel(t[i], o) && hit(t[i].r, o.r) > 20) out.push(`${t[i].n} × ${o.n}`);
      const r = t[i].r; if (r.right > W + 1 || r.bottom > H + 1 || r.left < -1) out.push(`${t[i].n} off canvas`);
    }
    return [...new Set(out)];
  }, s === "191x1" ? [1920 * 0.625, 1005 * 0.625] : [W, H]);
  if (found.length) { issues++; console.log(`${path.basename(path.dirname(file))}/${k}/${s}: ${found.join(", ")}`); }
}
await browser.close();
console.log(issues ? `${issues} creatives with overlaps` : "no overlaps");

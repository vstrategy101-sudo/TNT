// Flags the person or props covering the copy (definition bar, headline, ticks, CTA, small print).
import { createRequire } from "module"; import path from "path"; import { fileURLToPath } from "url";
const require = createRequire(import.meta.url); const { chromium } = require("/opt/node-tools/node_modules/playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch({ args: ["--allow-file-access-from-files"] }); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
for (const k of ["pack", "number", "bill", "refund", "global"]) {
  await p.goto(`file://${here}/people.html?k=${k}`); await p.waitForSelector("body[data-ready='1']");
  const r = await p.evaluate(() => {
    // person: test opaque pixels, not the box
    const img = document.querySelector(".person img"), box = img.getBoundingClientRect();
    const cv = document.createElement("canvas"); cv.width = img.naturalWidth; cv.height = img.naturalHeight;
    const cx = cv.getContext("2d"); cx.drawImage(img, 0, 0); const sx = img.naturalWidth / box.width;
    const opaque = (x, y) => { const px = Math.floor((x - box.left) * sx), py = Math.floor((y - box.top) * sx);
      if (px < 0 || py < 0 || px >= cv.width || py >= cv.height) return false; return cx.getImageData(px, py, 1, 1).data[3] > 60; };
    const copy = [...document.querySelectorAll(".def, h1, .ticks li, .cta, .small, .top .lockup, .top .url")];
    const out = [];
    for (const e of copy) { const r = e.getBoundingClientRect(); let hits = 0;
      for (let x = r.left; x < r.right; x += 8) for (let y = r.top; y < r.bottom; y += 8) if (opaque(x, y)) hits++;
      if (hits) out.push(`person × ${e.className || e.tagName} (${hits})`);
      document.querySelectorAll(".prop, .propb").forEach(pr => { const q = pr.getBoundingClientRect();
        if (Math.min(r.right, q.right) - Math.max(r.left, q.left) > 4 && Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top) > 4) out.push(`prop × ${e.className || e.tagName}`); }); }
    return out; });
  console.log(k, r.length ? r.join("; ") : "clear");
}
await b.close();

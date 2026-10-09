// Renders the CalaFly brand ads with real people (4:5) from people.html.
// Usage: node render-people.mjs [concept]
import { createRequire } from "module"; import path from "path"; import fs from "fs"; import { fileURLToPath } from "url";
const require = createRequire(import.meta.url); const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, "../creatives-people"); fs.mkdirSync(out, { recursive: true });
const CONCEPTS = [["P1", "pack", "DATA-ALREADY-ON"], ["P2", "number", "SAME-NUMBER"], ["P3", "bill", "ROAMING-SHOCK"], ["P4", "refund", "100-REFUND"], ["P5", "global", "200-COUNTRIES"]];
const only = process.argv[2];
const b = await chromium.launch({ args: ["--force-color-profile=srgb"] });
const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
for (const [n, k, label] of CONCEPTS) {
  if (only && only !== k) continue;
  await p.goto(`file://${here}/people.html?k=${k}`); await p.waitForSelector("body[data-ready='1']"); await p.waitForTimeout(100);
  await p.screenshot({ path: path.join(out, `CALAFLY_PEOPLE_${n}_${label}_4x5.png`), clip: { x: 0, y: 0, width: 1080, height: 1350 } });
}
await b.close(); console.log("done");

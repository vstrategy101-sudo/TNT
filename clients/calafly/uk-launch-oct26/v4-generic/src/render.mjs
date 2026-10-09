// Renders the generic CalaFly brand creatives (4:5) from generic.html.
// Usage: node render.mjs [concept]   — add PERSON=1 to include photo cutouts from ../people/<concept>.png
import { createRequire } from "module";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, "../creatives");
fs.mkdirSync(out, { recursive: true });
const CONCEPTS = [["G1", "pack", "PASSPORT-CHARGER-DATA"], ["G2", "number", "SAME-NUMBER"], ["G3", "bill", "ROAMING-BILL"], ["G4", "refund", "MONEY-BACK"], ["G5", "global", "200-COUNTRIES"]];
const only = process.argv[2];
const browser = await chromium.launch({ args: ["--force-color-profile=srgb"] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
for (const [n, k, label] of CONCEPTS) {
  if (only && only !== k) continue;
  await page.goto(`file://${here}/generic.html?k=${k}${process.env.PERSON ? "&person=1" : ""}`);
  await page.waitForSelector("body[data-ready='1']");
  await page.waitForTimeout(80);
  await page.screenshot({ path: path.join(out, `CALAFLY_GENERIC_${n}_${label}_4x5.png`), clip: { x: 0, y: 0, width: 1080, height: 1350 } });
}
await browser.close();
console.log("done");

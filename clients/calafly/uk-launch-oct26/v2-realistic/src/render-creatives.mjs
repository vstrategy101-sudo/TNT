// Renders the realistic CalaFly statics from creative.html.
// Usage: node render-creatives.mjs [country] [concept] [size]
import { createRequire } from "module";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, "../creatives");
const COUNTRIES = ["usa", "turkey", "dubai"];
const CONCEPTS = [["R1", "wheels", "WHEELS-DOWN-DATA-ON"], ["R2", "setup", "SET-UP-FROM-THE-SOFA"], ["R3", "payonce", "PAY-ONCE-ORDER"], ["R4", "refund", "REFUND-IF-NOT-INSTALLED"], ["R5", "still", "STILL-FLYING-RETARGET"]];
const SIZES = { "1x1": [1080, 1080], "4x5": [1080, 1350], "9x16": [1080, 1920], "191x1": [1200, 628] };
const [oc, ok, os] = process.argv.slice(2).map(a => a === "-" ? undefined : a);

const browser = await chromium.launch({ args: ["--enable-gpu-rasterization", "--force-color-profile=srgb"] });
const page = await browser.newPage({ viewport: { width: 1200, height: 1920 } });
for (const c of COUNTRIES) {
  if (oc && oc !== c) continue;
  fs.mkdirSync(path.join(out, c), { recursive: true });
  for (const [n, k, label] of CONCEPTS) {
    if (ok && ok !== k) continue;
    for (const [s, [w, h]] of Object.entries(SIZES)) {
      if (os && os !== s) continue;
      await page.goto(`file://${here}/creative.html?c=${c}&k=${k}&s=${s}`);
      await page.waitForSelector("body[data-ready='1']");
      await page.waitForTimeout(60);
      await page.screenshot({ path: path.join(out, c, `CALAFLY_${c.toUpperCase()}_${n}_${label}_${s}.png`), clip: { x: 0, y: 0, width: w, height: h } });
    }
  }
}
await browser.close();
console.log("done");

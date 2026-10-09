// Renders every CalaFly static creative from creative.html.
// Usage: node render-creatives.mjs [country] [concept]
import { createRequire } from "module";
import path from "path";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, "../creatives");

const COUNTRIES = ["usa", "turkey", "dubai"];
const CONCEPTS = [
  ["01", "intro", "INTRO_MEET-CALAFLY"],
  ["02", "ease", "EASE_SET-UP-IN-MINUTES"],
  ["03", "price", "PRICE_PAY-ONCE"],
  ["04", "refund", "REFUND_IF-NOT-INSTALLED"],
  ["05", "stack", "ALL-USP_DATA-SORTED"],
  ["06", "retarget", "RETARGET_STILL-PLANNING"],
];
const SIZES = { "1x1": [1080, 1080], "4x5": [1080, 1350], "9x16": [1080, 1920], "191x1": [1200, 628] };

const [onlyC, onlyK] = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 1920 } });
const fs = await import("fs");
for (const c of COUNTRIES) {
  if (onlyC && onlyC !== c) continue;
  fs.mkdirSync(path.join(out, c), { recursive: true });
  for (const [n, k, label] of CONCEPTS) {
    if (onlyK && onlyK !== k) continue;
    for (const [s, [w, h]] of Object.entries(SIZES)) {
      await page.goto(`file://${here}/creative.html?c=${c}&k=${k}&s=${s}`);
      await page.waitForSelector("body[data-ready='1']");
      const fit = await page.evaluate(() => document.body.dataset.fit);
      const file = path.join(out, c, `CALAFLY_${c.toUpperCase()}_${n}_${label}_${s}.png`);
      await page.screenshot({ path: file, clip: { x: 0, y: 0, width: w, height: h } });
      if (fit !== "1.00") console.log(`fit ${fit}  ${path.basename(file)}`);
    }
  }
}
await browser.close();
console.log("done");

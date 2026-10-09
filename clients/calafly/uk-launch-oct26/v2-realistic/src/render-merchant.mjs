// Renders Google Merchant Center product images (1500×1500, no overlays) for every catalogue product.
// Usage: node render-merchant.mjs [product|-] [main|arrive|home|-]
import { createRequire } from "module";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, "../../../merchant-center/images");
fs.mkdirSync(out, { recursive: true });
const PRODUCTS = ["turkey", "dubai", "usa", "thailand", "spain", "france", "italy", "japan", "world500", "world1", "world3"];
const KINDS = ["main", "arrive", "home"];
const [op, ok] = process.argv.slice(2).map(a => a === "-" ? undefined : a);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1500, height: 1500 } });
for (const p of PRODUCTS) {
  if (op && op !== p) continue;
  for (const k of KINDS) {
    if (ok && ok !== k) continue;
    await page.goto(`file://${here}/merchant.html?p=${p}&k=${k}`);
    await page.waitForSelector("body[data-ready='1']");
    await page.waitForTimeout(80);
    await page.screenshot({ path: path.join(out, `calafly-${p}-esim-${k}.jpg`), type: "jpeg", quality: 92, clip: { x: 0, y: 0, width: 1500, height: 1500 } });
  }
}
await browser.close();
console.log("done");

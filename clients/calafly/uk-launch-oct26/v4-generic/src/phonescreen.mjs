// Renders screen.html to a PNG that gets warped onto a model's blank phone (see screenwarp.py).
import { createRequire } from "module"; import path from "path"; import { fileURLToPath } from "url";
const require = createRequire(import.meta.url); const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 860 }, deviceScaleFactor: 2 });
await p.goto(`file://${here}/screen.html`); await p.waitForSelector("body[data-ready='1']"); await p.waitForTimeout(80);
await p.screenshot({ path: path.resolve(here, "../people/screen_ready.png"), clip: { x: 0, y: 0, width: 390, height: 860 } });
await b.close(); console.log("done");

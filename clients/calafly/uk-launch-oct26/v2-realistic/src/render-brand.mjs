// Renders the brand campaign films (30s walkthrough + 6s bumper) silently; sound_min.py --brand adds the sound.
// Usage: node render-brand.mjs [brand|bumper|-] [country|-] [format|-] [--stills]
import { createRequire } from "module";
import { spawn } from "child_process";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, "../../v3-brand/videos"), tmp = path.resolve(here, "../.tmp"), cueDir = path.join(here, "cues");
for (const d of [out, tmp, cueDir]) fs.mkdirSync(d, { recursive: true });
const FPS = 30;
const VIDEOS = [["brand", "B1_SORTED-BEFORE-YOU-FLY_30s"], ["bumper", "B2_BUMPER_6s"]];
const COUNTRIES = ["usa", "turkey", "dubai"];
const FORMATS = { "9x16": [1080, 1920], "16x9": [1920, 1080] };
const args = process.argv.slice(2), stills = args.includes("--stills");
const [ov, oc, of] = args.filter(a => !a.startsWith("--")).map(a => a === "-" ? undefined : a);

const browser = await chromium.launch();
for (const [v, label] of VIDEOS) {
  if (ov && ov !== v) continue;
  for (const c of COUNTRIES) {
    if (oc && oc !== c) continue;
    for (const [f, [w, h]] of Object.entries(FORMATS)) {
      if (of && of !== f) continue;
      const page = await browser.newPage({ viewport: { width: w, height: h } });
      await page.goto(`file://${here}/brand.html?v=${v}&c=${c}&f=${f}`);
      await page.waitForSelector("body[data-ready='1']");
      const { cues, dur } = await page.evaluate(() => ({ cues: window.CUES, dur: window.DUR }));
      fs.writeFileSync(path.join(cueDir, `${v}.cues.json`), JSON.stringify({ dur, cues }));
      const name = `CALAFLY_${c.toUpperCase()}_${label}_${f}`;
      if (stills) {
        const ts = v === "brand" ? [1.5, 6.5, 10.5, 15.5, 20.5, 24.5, 28.5] : [0.5, 2.0, 3.0, 5.5];
        for (const t of ts) { await page.evaluate(t => window.renderFrame(t), t); await page.screenshot({ path: path.join(tmp, `${name}_t${t}.png`) }); }
        await page.close(); continue;
      }
      const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "png", "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "17", "-r", String(FPS), "-movflags", "+faststart",
        path.join(out, `${name}.mp4`)], { stdio: ["pipe", "inherit", "inherit"] });
      for (let i = 0; i < Math.round(FPS * dur); i++) {
        await page.evaluate(t => window.renderFrame(t), i / FPS);
        const buf = await page.screenshot({ type: "png" });
        if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
      }
      ff.stdin.end(); await new Promise(r => ff.on("close", r));
      await page.close();
      console.log("wrote", name);
    }
  }
}
await browser.close();

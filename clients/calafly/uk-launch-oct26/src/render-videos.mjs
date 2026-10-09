// Renders the two CalaFly videos (15s, 30fps) frame by frame and encodes with ffmpeg.
// Usage: node render-videos.mjs [intro|howto] [9x16|16x9] [--stills]
import { createRequire } from "module";
import { spawn } from "child_process";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, "../videos");
fs.mkdirSync(out, { recursive: true });

const FPS = 30, DURATION = 15;
const VIDEOS = [["intro", "01_MEET-CALAFLY"], ["howto", "02_HOW-IT-WORKS"]];
const FORMATS = { "9x16": [1080, 1920], "16x9": [1920, 1080] };
const args = process.argv.slice(2);
const stills = args.includes("--stills");
const [onlyV, onlyF] = args.filter(a => !a.startsWith("--"));

const browser = await chromium.launch();
for (const [v, label] of VIDEOS) {
  if (onlyV && onlyV !== v) continue;
  for (const [f, [w, h]] of Object.entries(FORMATS)) {
    if (onlyF && onlyF !== f) continue;
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.goto(`file://${here}/video.html?v=${v}&f=${f}`);
    await page.waitForSelector("body[data-ready='1']");
    const name = `CALAFLY_VIDEO_${label}_${f}`;
    if (stills) {
      for (const t of [1, 4, 6.5, 9.5, 12, 14.5]) {
        await page.evaluate((t) => window.renderFrame(t), t);
        await page.screenshot({ path: path.join(out, `${name}_t${t}.png`) });
      }
      await page.close();
      continue;
    }
    const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "png", "-i", "-",
      "-f", "lavfi", "-i", `anullsrc=channel_layout=stereo:sample_rate=48000`, "-shortest",
      "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", String(FPS),
      "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", path.join(out, `${name}.mp4`)], { stdio: ["pipe", "inherit", "inherit"] });
    for (let i = 0; i < FPS * DURATION; i++) {
      await page.evaluate((t) => window.renderFrame(t), i / FPS);
      const buf = await page.screenshot({ type: "png" });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
    }
    ff.stdin.end();
    await new Promise(r => ff.on("close", r));
    await page.close();
    console.log("wrote", name);
  }
}
await browser.close();

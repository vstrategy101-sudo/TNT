// Renders the realistic CalaFly videos frame by frame (30fps, 15s), writes the sound cues,
// builds the mix with sound.py and muxes it in.
// Usage: node render-videos.mjs [video|-] [country|-] [format|-] [--stills]
import { createRequire } from "module";
import { spawn, execFileSync } from "child_process";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, "../videos"), audioDir = path.resolve(here, "../audio"), tmp = path.resolve(here, "../.tmp");
for (const d of [out, audioDir, tmp]) fs.mkdirSync(d, { recursive: true });

const FPS = 30, DURATION = 15;
const VIDEOS = [["wheels", "V3_WHEELS-DOWN"], ["sofa", "V4_FROM-THE-SOFA"]];
const COUNTRIES = ["usa", "turkey", "dubai"];
const FORMATS = { "9x16": [1080, 1920], "16x9": [1920, 1080] };
const args = process.argv.slice(2);
const stills = args.includes("--stills");
const [ov, oc, of] = args.filter(a => !a.startsWith("--")).map(a => a === "-" ? undefined : a);

const browser = await chromium.launch();
for (const [v, label] of VIDEOS) {
  if (ov && ov !== v) continue;
  for (const c of COUNTRIES) {
    if (oc && oc !== c) continue;
    for (const [f, [w, h]] of Object.entries(FORMATS)) {
      if (of && of !== f) continue;
      const page = await browser.newPage({ viewport: { width: w, height: h } });
      await page.goto(`file://${here}/video.html?v=${v}&c=${c}&f=${f}`);
      await page.waitForSelector("body[data-ready='1']");
      const name = `CALAFLY_${c.toUpperCase()}_${label}_${f}`;
      if (stills) {
        for (const t of [1, 3.5, 5, 7.5, 9.8, 12, 14.5]) {
          await page.evaluate(t => window.renderFrame(t), t);
          await page.screenshot({ path: path.join(tmp, `${name}_t${t}.png`) });
        }
        await page.close(); continue;
      }
      // sound: cues come from the page so picture and audio share one timeline
      const cues = await page.evaluate(() => window.CUES);
      const cueFile = path.join(tmp, `${v}.cues.json`);
      fs.writeFileSync(cueFile, JSON.stringify(cues));
      const mixBase = path.join(audioDir, `CALAFLY_${label}`);
      if (!fs.existsSync(`${mixBase}_MIX.wav`)) execFileSync("python3", [path.join(here, "sound.py"), cueFile, mixBase, String(DURATION)], { stdio: "inherit" });

      const silent = path.join(tmp, `${name}.mp4`);
      const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "png", "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "17", "-r", String(FPS), silent], { stdio: ["pipe", "inherit", "inherit"] });
      for (let i = 0; i < FPS * DURATION; i++) {
        await page.evaluate(t => window.renderFrame(t), i / FPS);
        const buf = await page.screenshot({ type: "png" });
        if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
      }
      ff.stdin.end(); await new Promise(r => ff.on("close", r));
      execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", silent, "-i", `${mixBase}_MIX.wav`, "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-shortest", "-movflags", "+faststart", path.join(out, `${name}.mp4`)]);
      fs.unlinkSync(silent);
      await page.close();
      console.log("wrote", name);
    }
  }
}
await browser.close();

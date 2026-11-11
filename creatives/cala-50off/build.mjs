// Cala eSIM — 50% sitewide static creatives (prospecting + retargeting)
// Renders every creative at 4:5 (1080x1350) and 9:16 (1080x1920) to ./out
// Run: node creatives/cala-50off/build.mjs
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright");
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.join(dir, "out");
fs.mkdirSync(outDir, { recursive: true });
const fontCss = fs
  .readFileSync(path.join(dir, "../fonts/local.css"), "utf8")
  .replace(/url\((f\d+\.woff2)\)/g, (_, f) =>
    `url(data:font/woff2;base64,${fs.readFileSync(path.join(dir, "../fonts", f)).toString("base64")})`);

const C = { navy: "#0B1B3F", yellow: "#FFD23F", coral: "#FF5A4E", paper: "#F6F1E7", sky: "#8FD0FF", ink: "#14213D" };

// 9:16 keeps text out of the top ~13% and bottom ~22% (Reels/Stories UI). 4:5 is near full-bleed.
const SIZES = {
  "4x5": { w: 1080, h: 1350, top: 40, bottom: 40 },
  "9x16": { w: 1080, h: 1920, top: 250, bottom: 420 },
};

const wm = (color = C.navy, tag = C.coral) =>
  `<div class="wm" style="color:${color}">cala<span style="background:${tag}">eSIM</span></div>`;
const fine = (color) => `<div class="fine" style="color:${color}">50% off all plans at calafly.net. T&amp;Cs apply.</div>`;
const cta = (color, line) => `<div class="cta" style="color:${color};border-color:${line}">Get 50% off at calafly.net &rarr;</div>`;

const creatives = [
  // ---------------- PROSPECTING ----------------
  {
    id: "P1-half-cut",
    bg: C.yellow,
    html: () => `
      <div class="col">
        ${wm()}
        <div class="half">
          <div class="h top">50%</div>
          <div class="h bot">50%</div>
          <div class="cut"></div>
        </div>
        <div>
          <div class="hl" style="color:${C.navy}">Half-price<br>holiday data.</div>
          <div class="sub" style="color:${C.navy}">Every plan. Sitewide.<br>One price for the whole trip. No daily roaming.</div>
          ${cta(C.navy, C.navy)}
          ${fine(C.navy)}
        </div>
      </div>`,
    css: `
      .half{position:relative;height:440px;margin:10px 0}
      .half .h{position:absolute;left:-12px;top:0;font:800 430px/1 'Plus Jakarta Sans';letter-spacing:-28px;color:${C.navy}}
      .half .top{clip-path:inset(0 0 50% 0)}
      .half .bot{clip-path:inset(50% 0 0 0);transform:translate(70px,44px)}
      .half .cut{position:absolute;left:-80px;right:-80px;top:226px;height:8px;background:${C.coral};transform:rotate(-2deg)}`,
  },
  {
    id: "P2-roaming-receipt",
    bg: C.navy,
    html: () => `
      <div class="col">
        ${wm("#fff", C.coral)}
        <div class="rcpt">
          <div class="rh">ROAMING ABROAD</div>
          <div class="ln"><span>Day 1</span><i></i><b>£?</b></div>
          <div class="ln"><span>Day 2</span><i></i><b>£?</b></div>
          <div class="ln"><span>Day 3</span><i></i><b>£?</b></div>
          <div class="ln"><span>Day 4</span><i></i><b>£?</b></div>
          <div class="ln"><span>Day 7</span><i></i><b>£?</b></div>
          <div class="ln tot"><span>TOTAL</span><i></i><b>£???</b></div>
          <div class="sep"></div>
          <div class="rh">CALA eSIM</div>
          <div class="ln"><span>Whole trip</span><i></i><b>ONE PRICE</b></div>
          <div class="ln hi"><span>Today</span><i></i><b>50% OFF</b></div>
        </div>
        <div>
          <div class="hl" style="color:#fff">Stop paying<br>by the day.</div>
          <div class="sub" style="color:#C9D3EA">Pay once for your trip, priced in pounds.</div>
          ${cta(C.yellow, C.yellow)}
          ${fine("#8E9BBE")}
        </div>
      </div>`,
    css: `
      .rcpt{background:${C.paper};color:${C.ink};font:500 34px/1.25 'JetBrains Mono';padding:46px 56px 70px;transform:rotate(-2.2deg);margin:6px 30px 0;
        box-shadow:0 30px 60px rgba(0,0,0,.35);
        -webkit-mask:conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) 50%/36px 100%}
      .rh{font-weight:700;letter-spacing:4px;margin:6px 0 14px}
      .ln{display:flex;align-items:baseline;gap:12px;margin:6px 0}
      .ln i{flex:1;border-bottom:4px dotted #9aa}
      .ln b{font-weight:700}
      .tot b{color:${C.coral}}
      .sep{border-top:4px dashed ${C.ink};margin:26px 0 18px}
      .hi{background:${C.yellow};margin:6px -16px;padding:4px 16px}
      .hl{font-size:96px}`,
  },
  {
    id: "P3-whatsapp-no",
    bg: C.paper,
    html: () => `
      <div class="col">
        ${wm()}
        <div>
          <div class="q">&ldquo;Will I lose my<br>WhatsApp number?&rdquo;</div>
          <div class="no">No.</div>
        </div>
        <div>
          <div class="sub" style="color:${C.navy};font-size:44px;font-weight:600">Keep your number. Ditch daily roaming.<br>One price for the whole trip.</div>
          <div class="tag">50% off every plan</div>
          ${fine(C.navy)}
        </div>
      </div>`,
    css: `
      .q{font:italic 700 72px/1.12 'Playfair Display';color:${C.navy}}
      .no{font:800 470px/0.9 'Plus Jakarta Sans';letter-spacing:-26px;color:${C.coral};margin:20px 0 0 -14px}
      .tag{display:inline-block;margin-top:30px;background:${C.navy};color:${C.yellow};font:800 50px/1 'Plus Jakarta Sans';padding:20px 30px;transform:rotate(-2deg)}`,
  },
  {
    id: "P4-boarding-pass",
    bg: C.coral,
    html: () => `
      <div class="col">
        ${wm("#fff", C.navy)}
        <div class="hl" style="color:#fff;font-size:92px">Sort your data<br>before the gate.</div>
        <div class="bp">
          <div class="main">
            <div class="bphead"><span>BOARDING PASS</span><span>CALA eSIM</span></div>
            <div class="row"><div><em>FROM</em><b>Daily roaming</b></div><div class="plane">&#9992;</div><div><em>TO</em><b>One trip price</b></div></div>
            <div class="row small"><div><em>PASSENGER</em><b>You</b></div><div><em>GATE</em><b>Your sofa</b></div><div><em>FARE</em><b class="c">50% OFF</b></div></div>
          </div>
          <div class="stub"><div class="bars"></div></div>
        </div>
        <div>
          <div class="sub" style="color:#fff">Scan the QR code at home. Land connected.</div>
          ${cta("#fff", "#fff")}
          ${fine("#FFE1DD")}
        </div>
      </div>`,
    css: `
      .bp{display:flex;background:#fff;color:${C.ink};border-radius:28px;transform:rotate(-2deg);box-shadow:0 30px 60px rgba(80,0,0,.3);overflow:hidden}
      .main{flex:1;padding:40px 44px;border-right:5px dashed #d6d6d6}
      .bphead{display:flex;justify-content:space-between;font:700 26px 'JetBrains Mono';letter-spacing:4px;color:${C.coral};margin-bottom:30px}
      .row{display:flex;justify-content:space-between;align-items:flex-end;gap:18px;margin-bottom:30px}
      .row em{display:block;font:500 22px 'JetBrains Mono';letter-spacing:3px;color:#888;font-style:normal;margin-bottom:6px}
      .row b{font:800 46px/1.05 'Plus Jakarta Sans'}
      .row.small b{font-size:36px}
      .row .c{color:${C.coral}}
      .plane{font-size:60px;color:${C.navy};padding-bottom:6px}
      .stub{width:120px;display:flex;align-items:center;justify-content:center}
      .bars{width:56px;height:80%;background:repeating-linear-gradient(0deg,${C.ink} 0 6px,#fff 6px 10px,${C.ink} 10px 12px,#fff 12px 20px)}`,
  },
  {
    id: "P5-breakup-postcard",
    bg: C.sky,
    html: () => `
      <div class="col">
        ${wm()}
        <div class="pc">
          <div class="pl">
            <p>Dear daily roaming,</p>
            <p>It's not me. It's you.</p>
            <p>I've found someone who charges once for the whole trip.</p>
            <p>Don't text. I'll be on data.</p>
          </div>
          <div class="pr">
            <div class="stamp"><b>50%</b><span>OFF</span></div>
            <div class="pm">CALA &middot; AIRMAIL</div>
            <div class="addr"></div><div class="addr"></div><div class="addr"></div>
          </div>
        </div>
        <div>
          <div class="hl" style="color:${C.navy};font-size:88px">Break up<br>with roaming.</div>
          <div class="sub" style="color:${C.navy}">50% off every plan, sitewide.</div>
          ${fine(C.navy)}
        </div>
      </div>`,
    css: `
      .pc{display:flex;background:${C.paper};padding:48px;gap:36px;transform:rotate(2deg);box-shadow:0 30px 60px rgba(0,40,80,.25);min-height:560px}
      .pl{flex:1.35;font:italic 700 44px/1.28 'Playfair Display';color:${C.ink};border-right:3px solid #cfc6b4;padding-right:32px}
      .pl p{margin:0 0 22px}
      .pr{flex:1;display:flex;flex-direction:column;align-items:flex-end}
      .stamp{width:180px;height:210px;background:${C.coral};color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;
        outline:10px dotted ${C.paper};outline-offset:-5px;transform:rotate(4deg)}
      .stamp b{font:800 72px/1 'Plus Jakarta Sans'} .stamp span{font:800 40px/1 'Plus Jakarta Sans';letter-spacing:4px}
      .pm{margin:26px 0 50px;border:4px solid ${C.navy};border-radius:999px;padding:12px 22px;font:700 22px 'JetBrains Mono';color:${C.navy};transform:rotate(-8deg)}
      .addr{width:100%;border-bottom:3px solid #cfc6b4;height:64px}`,
  },

  // ---------------- RETARGETING ----------------
  {
    id: "R1-you-looked",
    bg: C.navy,
    html: () => `
      <div class="col">
        ${wm("#fff", C.coral)}
        <div class="tagwrap">
          <div class="ptag">
            <div class="hole"></div>
            <div class="old">FULL PRICE</div>
            <div class="new">50%<small>OFF</small></div>
          </div>
        </div>
        <div>
          <div class="hl" style="color:#fff">You looked.<br>It got cheaper.</div>
          <div class="sub" style="color:#C9D3EA">Same plans. Same data. Half the price.</div>
          ${cta(C.yellow, C.yellow)}
          ${fine("#8E9BBE")}
        </div>
      </div>`,
    css: `
      .tagwrap{display:flex;justify-content:center}
      .ptag{position:relative;width:560px;padding:120px 40px 56px;background:${C.yellow};color:${C.navy};text-align:center;transform:rotate(-8deg);
        clip-path:polygon(50% 0,100% 16%,100% 100%,0 100%,0 16%);box-shadow:0 30px 60px rgba(0,0,0,.4)}
      .hole{position:absolute;left:50%;top:56px;width:44px;height:44px;margin-left:-22px;border-radius:50%;background:${C.navy}}
      .old{font:700 50px 'JetBrains Mono';letter-spacing:3px;position:relative;display:inline-block}
      .old:after{content:"";position:absolute;left:-14px;right:-14px;top:50%;height:10px;background:${C.coral};transform:rotate(-6deg)}
      .new{font:800 230px/0.95 'Plus Jakarta Sans';letter-spacing:-12px;margin-top:20px}
      .new small{display:block;font-size:72px;letter-spacing:6px}`,
  },
  {
    id: "R2-packing-list",
    bg: "#D9B98C",
    html: () => `
      <div class="col">
        ${wm()}
        <div class="note">
          <div class="nt">Before I fly:</div>
          <div class="it done">1. Passport</div>
          <div class="it done">2. Chargers</div>
          <div class="it done">3. Sun cream</div>
          <div class="it last">4. Cala eSIM <span>(half price!)</span>
            <svg viewBox="0 0 700 140" preserveAspectRatio="none"><path d="M30,80 C40,10 640,0 680,60 C700,120 120,140 40,100 C10,85 30,60 70,40" fill="none" stroke="${C.coral}" stroke-width="9" stroke-linecap="round"/></svg>
          </div>
        </div>
        <div>
          <div class="hl" style="color:${C.navy};font-size:84px">Don't leave the last<br>one for the airport.</div>
          <div class="sub" style="color:${C.navy}">Install at home. Switch on when you land. 50% off every plan.</div>
          ${fine(C.navy)}
        </div>
      </div>`,
    css: `
      .note{background:${C.yellow};padding:56px 60px 70px;transform:rotate(-2.5deg);box-shadow:0 26px 50px rgba(60,30,0,.3);margin:0 20px}
      .nt{font:italic 700 66px 'Playfair Display';color:${C.ink};margin-bottom:24px}
      .it{font:600 54px/1.55 'Plus Jakarta Sans';color:${C.ink};position:relative}
      .it.done{color:#6b5a1e;text-decoration:line-through;text-decoration-thickness:6px;text-decoration-color:${C.ink}}
      .it.last{font-weight:800;margin-top:10px}
      .it.last span{color:${C.coral}}
      .it svg{position:absolute;left:-34px;top:-22px;width:110%;height:140%}`,
  },
  {
    id: "R3-install-tonight",
    bg: `radial-gradient(circle at 78% 18%, #2a3f7a 0, ${C.navy} 55%)`,
    html: () => `
      <div class="col">
        ${wm("#fff", C.coral)}
        <div>
          <div class="moon"></div>
          <div class="hl" style="color:#fff;font-size:120px">Install it<br>tonight.</div>
          <div class="hl" style="color:${C.yellow};font-size:120px;margin-top:6px">Switch it on<br>when you land.</div>
        </div>
        <div>
          <div class="tl">
            <div><b>Tonight</b><span>Scan the QR code at home</span></div>
            <div><b>Land</b><span>Switch it on. Connected.</span></div>
          </div>
          <div class="tag2">50% off every plan, sitewide</div>
          ${fine("#8E9BBE")}
        </div>
      </div>`,
    css: `
      .col{position:relative}
      .moon{position:absolute;right:30px;top:-10px;width:150px;height:150px;border-radius:50%;box-shadow:-34px 18px 0 0 ${C.yellow};transform:rotate(-10deg)}
      .tl{display:flex;gap:24px;margin-bottom:34px}
      .tl div{flex:1;border-top:6px solid ${C.coral};padding-top:18px}
      .tl b{display:block;font:700 30px 'JetBrains Mono';color:${C.coral};letter-spacing:3px;text-transform:uppercase}
      .tl span{font:600 36px/1.25 'Plus Jakarta Sans';color:#fff}
      .tag2{display:inline-block;background:${C.yellow};color:${C.navy};font:800 46px/1 'Plus Jakarta Sans';padding:20px 28px}`,
  },
  {
    id: "R4-two-minutes",
    bg: "#fff",
    html: () => `
      <div class="col">
        ${wm()}
        <div>
          <div class="clock">2<span>min</span></div>
          <div class="hl" style="color:${C.navy};font-size:92px">Holiday data,<br>sorted in 2 minutes.</div>
        </div>
        <div>
          <div class="price"><s>Full price</s> <b>Half price.</b></div>
          <div class="sub" style="color:${C.navy}">Choose your destination. Pay once. One price for the whole trip.</div>
          ${fine(C.navy)}
        </div>
      </div>`,
    css: `
      .clock{font:800 400px/0.9 'Plus Jakarta Sans';letter-spacing:-16px;color:${C.coral};margin:0 0 20px -18px}.clock span{font-size:150px;letter-spacing:-4px;margin-left:24px}
      .price{font:800 72px/1.1 'Plus Jakarta Sans';color:${C.navy};margin-bottom:22px}
      .price s{color:#9aa3b8;text-decoration-thickness:8px;text-decoration-color:${C.coral}}
      .price b{background:${C.yellow};padding:0 14px}`,
  },
];

const base = (s) => `
  ${fontCss}
  *{box-sizing:border-box}
  html,body{margin:0;width:${s.w}px;height:${s.h}px;overflow:hidden}
  .stage{position:relative;width:${s.w}px;height:${s.h}px}
  .safe{position:absolute;left:72px;right:72px;top:${s.top + 32}px;bottom:${s.bottom + 32}px}
  .col{height:100%;display:flex;flex-direction:column;justify-content:space-between}
  .wm{font:800 64px/1 'Plus Jakarta Sans';letter-spacing:-2px;display:flex;align-items:center;gap:14px}
  .wm span{font:700 22px/1 'JetBrains Mono';letter-spacing:2px;color:#fff;padding:8px 10px;border-radius:6px}
  .hl{font:800 104px/1.0 'Plus Jakarta Sans';letter-spacing:-3px}
  .sub{font:500 38px/1.3 'Plus Jakarta Sans';margin-top:22px}
  .cta{display:inline-block;margin-top:28px;font:800 40px/1 'Plus Jakarta Sans';border-bottom:5px solid;padding-bottom:8px}
  .fine{font:500 22px/1.3 'Plus Jakarta Sans';margin-top:26px;opacity:.9}
`;

const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 1 });
const made = [];
for (const c of creatives) {
  for (const [key, s] of Object.entries(SIZES)) {
    await page.setViewportSize({ width: s.w, height: s.h });
    await page.setContent(
      `<!doctype html><html><head><meta charset="utf-8"><style>${base(s)}${c.css}</style></head>
       <body><div class="stage" style="background:${c.bg}"><div class="safe">${c.html()}</div></div></body></html>`,
      { waitUntil: "load" }
    );
    await page.evaluate(() => document.fonts.ready);
    // overflow check: content must stay inside the safe box
    const over = await page.evaluate(() => {
      const safe = document.querySelector(".safe").getBoundingClientRect();
      const col = document.querySelector(".col");
      return col.scrollHeight > safe.height + 2 ? col.scrollHeight - safe.height : 0;
    });
    const file = path.join(outDir, `${c.id}_${key}.png`);
    await page.screenshot({ path: file });
    made.push(file);
    console.log(`${over ? "OVERFLOW " + over + "px  " : "ok  "}${path.basename(file)}`);
  }
}
await browser.close();

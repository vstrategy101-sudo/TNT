"""Maaya reel (real face, Reena Devi bahu): script_maaya.json -> VO + SFX -> SadTalker talking head -> v2 edit on top -> MP4.\nUsage: python3 build_real.py            # makes audio\n       python3 build_real.py talking.mp4  # composites final
Run: python3 build.py   (needs piper-tts, numpy, Pillow with raqm, ffmpeg, Noto Sans Devanagari)
"""
import json, math, subprocess, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = "/tmp/rd"
VOICE = os.environ.get("RD_VOICE", "/tmp/voice/hi_IN-priyamvada-medium.onnx")
LENGTH_SCALE = "0.8"          # <1 = faster speech; reels pace
W, H, FPS, SS = 1080, 1920, 25, 2   # SS = supersampling for the character art
GAP = 0.30                     # silence between lines (s)
SR = 22050
os.makedirs(f"{WORK}/vo", exist_ok=True)

FONT_B = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"
def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size, layout_engine=ImageFont.Layout.RAQM)

# ---------- 1. Voiceover + sound design ----------
script = json.load(open(f"{HERE}/script_maaya.json"))
OUT = os.environ.get("OUT", f"{HERE}/maaya-piles-real.mp4")
os.makedirs(f"{WORK}/vo_m", exist_ok=True)
def read_wav(p):
    with wave.open(p) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
def trim(a, thr=0.01):
    idx = np.where(np.abs(a) > thr)[0]
    return a[max(0, idx[0] - 400): idx[-1] + 800] if len(idx) else a

segs, parts, t = [], [], 0.15
parts.append(np.zeros(int(0.15 * SR), np.float32))
for s in script:
    p = f"{WORK}/vo_m/{s['id']}.wav"
    subprocess.run(["python3", "-m", "piper", "-m", VOICE, "--length-scale", LENGTH_SCALE, "-f", p],
                   input=s["text"].encode(), check=True, capture_output=True)
    a = trim(read_wav(p))
    segs.append({**s, "start": t, "end": t + len(a) / SR})
    g = s.get("gap", 0.15)
    parts += [a, np.zeros(int(g * SR), np.float32)]
    t += len(a) / SR + g
parts.append(np.zeros(int(1.6 * SR), np.float32))
voice = np.concatenate(parts)
DUR = len(voice) / SR
N = len(voice)
tt = np.arange(N) / SR
rng = np.random.default_rng(3)

def sfx(kind):
    if kind == "boom":
        n = int(0.7 * SR); x = np.arange(n) / SR
        f = 70 * np.exp(-x * 3) + 32
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 5)
        y[:200] += rng.normal(0, 0.6, 200) * np.linspace(1, 0, 200)
        return y * 0.9
    if kind == "whoosh":
        n = int(0.4 * SR); x = np.linspace(0, 1, n)
        y = rng.normal(0, 1, n)
        k = np.ones(12) / 12; y = np.convolve(y, k, "same")
        return y * np.sin(np.pi * x) ** 2 * 0.5
    if kind == "ding":
        n = int(0.9 * SR); x = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1318 * x) + 0.4 * np.sin(2 * np.pi * 2637 * x)) * np.exp(-x * 5) * 0.35
    if kind == "tick":
        n = int(1.6 * SR); y = np.zeros(n)
        for i in range(0, n - 300, int(0.11 * SR)):
            y[i:i + 300] += rng.normal(0, 1, 300) * np.exp(-np.arange(300) / 40) * 0.5
        return y
    return np.zeros(1)

fxtrack = np.zeros(N)
for s in segs:
    if s.get("fx"):
        y = sfx(s["fx"]); i0 = max(0, int((s["start"] - (0.18 if s["fx"] == "whoosh" else 0.02)) * SR))
        fxtrack[i0:i0 + len(y)] += y[:N - i0]

# rhythmic bed: soft low pulse + shaker at 104 bpm, ducked under speech
beat = 60 / 104
bed = np.zeros(N)
for k in range(int(DUR / beat)):
    i0 = int(k * beat * SR); n = int(0.25 * SR); x = np.arange(n) / SR
    kick = np.sin(2 * np.pi * (90 * np.exp(-x * 18) + 45) * x) * np.exp(-x * 14)
    bed[i0:i0 + n] += kick[:N - i0] * (1.0 if k % 2 == 0 else 0.6)
    j0 = int((k + 0.5) * beat * SR); m = 900
    if j0 + m < N: bed[j0:j0 + m] += rng.normal(0, 0.25, m) * np.exp(-np.arange(m) / 200)
sa = 138.59
bed += 0.35 * (np.sin(2 * np.pi * sa * tt) + 0.5 * np.sin(2 * np.pi * sa * 1.5 * tt))
env = np.convolve(np.abs(voice), np.ones(3000) / 3000, "same")
bed = bed / np.max(np.abs(bed)) * 0.09 * (1 - np.clip(env * 20, 0, 0.55))
mix = np.clip(voice * 1.0 + fxtrack * 0.55 + bed, -1, 1)
with wave.open(f"{WORK}/mix_m.wav", "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())

NF = int(DUR * FPS)
spf = SR / FPS
rms = np.array([np.sqrt(np.mean(voice[int(i * spf):int((i + 1) * spf)] ** 2) + 1e-9) for i in range(NF)])
rms = np.convolve(rms, [0.25, 0.5, 0.25], "same")
lvl = rms / np.percentile(rms[rms > 0.01], 90)

with wave.open(f"{WORK}/vo_only_m.wav", "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())
# ---------- 4. Overlays (v2: karaoke captions, stickers, slams, shake, flash) ----------
F_LATB = lambda n: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", n)
F_CAP = font(84)
F_SMALL = font(30, False)
EMOJI = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
_emo = {}
def emoji(e, size):
    if (e, size) not in _emo:
        im = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((8, 8), e, font=EMOJI, embedded_color=True)
        _emo[(e, size)] = im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)
    return _emo[(e, size)]

def back_ease(p):  # overshoot pop
    p = min(max(p, 0), 1); c = 2.2
    return 1 + (c + 1) * (p - 1) ** 3 + c * (p - 1) ** 2

def paste_scaled(dst, img, cx, cy, sc, rot=0):
    if sc <= 0.02: return
    im = img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.BILINEAR)
    if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    dst.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)

def text_img(txt, f, fill, stroke=0, sfill=(0, 0, 0), pad=20):
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t_, r, b = d0.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    im = Image.new("RGBA", (r - l + 2 * pad, b - t_ + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - l, pad - t_), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    return im

# word timings (proportional to word length) and 3-word caption pages
for s in segs:
    ws = s["text"].split(); tot = sum(len(w) + 1 for w in ws); t0 = s["start"]; s["words"] = []
    for w in ws:
        dt = (s["end"] - s["start"]) * (len(w) + 1) / tot; s["words"].append((t0, t0 + dt, w)); t0 += dt
    s["pages"] = [s["words"][i:i + 3] for i in range(0, len(s["words"]), 3)]

def seg_at(ts):
    return next((s for s in segs if s["start"] - 0.05 <= ts < s["end"] + s.get("gap", 0.15)), None)

def card_img(v):
    red = v.get("red")
    f = font(76)
    txt = text_img(v["t"], f, (255, 255, 255) if red else (90, 15, 30))
    bw = 150
    w = bw + txt.width + 60 + (130 if v.get("e") else 0)
    im = Image.new("RGBA", (w, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 169], 40, fill=(200, 30, 35) if red else (255, 250, 236), outline=(120, 20, 40), width=7)
    d.rounded_rectangle([16, 16, 16 + bw - 20, 153], 30, fill=(120, 20, 40))
    nb = text_img(v["n"], F_LATB(86), (255, 214, 120), pad=0)
    im.paste(nb, (16 + (bw - 20 - nb.width) // 2, 85 - nb.height // 2), nb)
    im.paste(txt, (bw + 10, 85 - txt.height // 2), txt)
    if v.get("e"): paste_scaled(im, emoji(v["e"], 110), w - 85, 85, 1)
    return im
CARDS = {s["id"]: card_img(s["vis"]) for s in segs if s["vis"]["type"] == "card"}

def draw_overlay(frame, ts):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    s = seg_at(ts)
    # progress bar + AI label + disclaimer
    d.rectangle([0, 0, int(W * ts / DUR), 14], fill=(255, 200, 60))
    d.rounded_rectangle([40, 40, 360, 92], 14, fill=(0, 0, 0, 160))
    d.text((60, 51), "AI", font=F_LATB(28), fill=(255, 255, 255))
    d.text((60 + d.textlength("AI", font=F_LATB(28)) + 4, 44), "-जनित किरदार", font=F_SMALL, fill=(255, 255, 255))
    d.rectangle([0, H - 80, W, H], fill=(30, 10, 10, 200))
    tw = d.textlength("सिर्फ़ जानकारी के लिए। इलाज के लिए डॉक्टर से सलाह लें।", font=F_SMALL)
    d.text(((W - tw) / 2, H - 70), "सिर्फ़ जानकारी के लिए। इलाज के लिए डॉक्टर से सलाह लें।", font=F_SMALL, fill=(255, 255, 255))
    if s:
        v, p = s["vis"], (ts - s["start"] + 0.05) / 0.3
        sc = back_ease(p)
        if v["type"] == "timer":
            sec = min(1, (ts - s["start"]) / (s["end"] - s["start"])) * 25 * 60
            ti = text_img(f"{int(sec // 60):02}:{int(sec % 60):02}", F_LATB(150), (255, 255, 255), 10, (200, 30, 35))
            paste_scaled(ov, emoji("🚽", 210), 230, 1000, sc, -8)
            paste_scaled(ov, emoji("📱", 190), 850, 1000, sc, 12)
            paste_scaled(ov, ti, W / 2, 1180, sc)
        elif v["type"] == "sticker":
            paste_scaled(ov, emoji(v["e"], 300), 820, 1150, sc, 10 * math.sin(ts * 6))
        elif v["type"] == "slam":
            big = v["big"]
            f = F_LATB(330) if big.isascii() else font(118)
            bi = text_img(big, f, (255, 220, 60) if big.isascii() else (255, 255, 255), 14, (150, 15, 30))
            z = 1 + 1.2 * max(0, 1 - p)         # slam in from big
            paste_scaled(ov, bi, W / 2, 1150, min(z, 2.2) if p < 1 else 1 + 0.02 * math.sin(ts * 8))
            if v["small"]:
                si = text_img(v["small"], F_LATB(34), (255, 255, 255), 0)
                dd = ImageDraw.Draw(ov); dd.rounded_rectangle([W / 2 - si.width / 2, 1330, W / 2 + si.width / 2, 1330 + si.height], 16, fill=(0, 0, 0, 170))
                ov.paste(si, (int(W / 2 - si.width / 2), 1330), si)
        elif v["type"] == "meter":
            q = min(1, (ts - s["start"]) / (s["end"] - s["start"]))
            lab = text_img(v["label"], font(64), (90, 15, 30), pad=0)
            ov.paste(lab, (100, 1030), lab)
            d.rounded_rectangle([100, 1140, 980, 1220], 40, fill=(255, 255, 255, 220), outline=(120, 20, 40), width=6)
            col = (int(80 + 175 * q), int(180 - 150 * q), 50)
            d.rounded_rectangle([110, 1150, 110 + int(860 * q), 1210], 30, fill=col)
            paste_scaled(ov, emoji("⏰", 150), 900, 1080, 1, 15 * math.sin(ts * 20) * q)
        elif v["type"] == "card":
            c = CARDS[s["id"]]
            x = W / 2 + (1 - min(1, p)) * -900
            paste_scaled(ov, c, x, 1200, 1 if p >= 1 else 0.9 + 0.1 * p)
        # karaoke captions: 3 words, current word yellow & bigger
        page = next((pg for pg in s["pages"] if pg[0][0] <= ts < pg[-1][1] + 0.15), None)
        if page:
            imgs = []
            for a, b, w in page:
                on = a <= ts < b
                imgs.append(text_img(w, F_CAP, (255, 214, 0) if on else (255, 255, 255), 9, (25, 5, 5), pad=6))
            total = sum(i.width for i in imgs) + 18 * (len(imgs) - 1)
            if total > W - 80:   # two lines
                rows = [imgs[:2], imgs[2:]]
            else:
                rows = [imgs]
            y = 1560 - 60 * (len(rows) - 1)
            for row in rows:
                tw = sum(i.width for i in row) + 18 * (len(row) - 1); x = (W - tw) / 2
                for k, im in enumerate(row):
                    a, b, w = page[imgs.index(im)]
                    pop = 1.12 if a <= ts < b else 1.0
                    paste_scaled(ov, im, x + im.width / 2, y + im.height / 2, pop); x += im.width + 18
                y += 120
    if ts > segs[-1]["end"] - 0.1:
        p = (ts - segs[-1]["end"] + 0.1) / 0.3
        ei = text_img("फ़ॉलो करें: माया", font(76), (255, 240, 210), 0, pad=24)
        bg = Image.new("RGBA", (ei.width + 60, ei.height + 20), (0, 0, 0, 0))
        ImageDraw.Draw(bg).rounded_rectangle([0, 0, bg.width - 1, bg.height - 1], 40, fill=(120, 20, 40)); bg.paste(ei, (30, 10), ei)
        paste_scaled(ov, bg, W / 2, 1720, back_ease(p))
    frame.paste(ov, (0, 0), ov)
    return frame

# ---------- 5. Composite over the talking-head video ----------
import sys
TH = sys.argv[1] if len(sys.argv) > 1 else None
if not TH:
    print("audio ready:", f"{WORK}/vo_only_m.wav", f"{DUR:.1f}s"); sys.exit(0)
probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", TH], capture_output=True, text=True).stdout.strip().split(",")
vw, vh = int(probe[0]), int(probe[1])
FACE_Y = float(os.environ.get("FACE_Y", "0.25"))   # face centre as fraction of frame height (zoom anchor)
src_p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", TH, "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
flashes = [s["start"] for s in segs if s.get("flash")]
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                       "-r", str(FPS), "-i", "-", "-i", f"{WORK}/mix_m.wav", "-c:v", "libx264", "-preset", "medium",
                       "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                       "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
r2 = np.random.default_rng(7)
last = None
for i in range(NF):
    ts = i / FPS
    buf = src_p.stdout.read(W * H * 3)
    if len(buf) == W * H * 3: last = Image.frombytes("RGB", (W, H), buf)
    base = last
    s = seg_at(ts) or segs[-1]
    z = s["zoom"] * (1 + 0.015 * max(0, ts - s["start"]))
    cw, chh = int(W / z), int(H / z)
    cx, cy = W / 2, H * FACE_Y
    x0 = int(min(max(cx - cw / 2, 0), W - cw)); y0 = int(min(max(cy - chh * FACE_Y, 0), H - chh))
    frame = base.crop((x0, y0, x0 + cw, y0 + chh)).resize((W, H), Image.BICUBIC)
    # darken the top/bottom a touch so cards and captions read on a real photo
    frame = draw_overlay(frame, ts)
    for f0 in flashes:
        dt = ts - f0
        if 0 <= dt < 0.35:
            k = 1 - dt / 0.35
            frame = Image.blend(frame, Image.new("RGB", (W, H), (220, 20, 30)), 0.4 * k)
            ox, oy = int(r2.integers(-18, 19) * k), int(r2.integers(-18, 19) * k)
            frame = frame.transform((W, H), Image.AFFINE, (1, 0, ox, 0, 1, oy), fillcolor=(30, 10, 10))
    ff.stdin.write(frame.convert("RGB").tobytes())
ff.stdin.close(); ff.wait(); src_p.kill()
print("done", OUT, f"{DUR:.1f}s")

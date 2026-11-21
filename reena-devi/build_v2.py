"""Reena Devi reel v2 (high-drama edit): script_v2.json -> VO + SFX + beat -> expressive character -> karaoke captions -> MP4.
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
script = json.load(open(f"{HERE}/script_v2.json"))
OUT = f"{HERE}/reena-devi-piles-v2.mp4"
os.makedirs(f"{WORK}/vo2", exist_ok=True)
def read_wav(p):
    with wave.open(p) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
def trim(a, thr=0.01):
    idx = np.where(np.abs(a) > thr)[0]
    return a[max(0, idx[0] - 400): idx[-1] + 800] if len(idx) else a

segs, parts, t = [], [], 0.15
parts.append(np.zeros(int(0.15 * SR), np.float32))
for s in script:
    p = f"{WORK}/vo2/{s['id']}.wav"
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
with wave.open(f"{WORK}/mix2.wav", "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())

NF = int(DUR * FPS)
spf = SR / FPS
rms = np.array([np.sqrt(np.mean(voice[int(i * spf):int((i + 1) * spf)] ** 2) + 1e-9) for i in range(NF)])
rms = np.convolve(rms, [0.25, 0.5, 0.25], "same")
lvl = rms / np.percentile(rms[rms > 0.01], 90)

# ---------- 2. Character art (drawn once) ----------
S = SS
CW, CH = 900 * S, 1400 * S
SKIN, SKIN_D = (232, 190, 156), (206, 158, 124)
HAIR = (28, 22, 22)
SAREE, SAREE_L, SAREE_D, GOLD = (196, 214, 170), (140, 214, 200), (170, 186, 140), (214, 170, 72)
BLOUSE = (238, 120, 100)

def char_base():
    """Stylised look based on the reference photo: loose middle-parted hair, sindoor, small blue bindi,
    nose-ring hoop, gold drop earrings, long black-bead mangalsutra, mint saree + gold zari, coral blouse."""
    im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = CW // 2
    # hair mass behind head, falling past the shoulders
    d.ellipse([cx - 225 * S, 150 * S, cx + 225 * S, 600 * S], fill=HAIR)
    d.polygon([(cx - 225 * S, 380 * S), (cx + 225 * S, 380 * S), (cx + 255 * S, 820 * S), (cx - 255 * S, 820 * S)], fill=HAIR)
    # shoulders: coral blouse, mint saree pallu diagonally across chest
    d.rounded_rectangle([cx - 400 * S, 790 * S, cx + 400 * S, CH + 600 * S], 220 * S, fill=BLOUSE)
    d.polygon([(cx - 400 * S, 1010 * S), (cx - 120 * S, 1000 * S), (cx + 400 * S, 790 * S), (cx + 400 * S, CH), (cx - 400 * S, CH)], fill=SAREE)
    d.polygon([(cx - 400 * S, 1060 * S), (cx - 120 * S, 1050 * S), (cx + 400 * S, 840 * S), (cx + 400 * S, 790 * S), (cx - 120 * S, 1000 * S), (cx - 400 * S, 1010 * S)], fill=SAREE_L)
    d.line([(cx - 400 * S, 1010 * S), (cx - 120 * S, 1000 * S), (cx + 400 * S, 790 * S)], fill=GOLD, width=22 * S)
    for k in range(4):   # zari pleat lines
        d.line([(cx - 60 * S + k * 110 * S, 1150 * S), (cx + 320 * S, 870 * S + k * 70 * S)], fill=SAREE_D, width=5 * S)
    # neck + neckline
    d.rounded_rectangle([cx - 85 * S, 560 * S, cx + 85 * S, 840 * S], 60 * S, fill=SKIN_D)
    d.pieslice([cx - 190 * S, 680 * S, cx + 190 * S, 980 * S], 0, 180, fill=SKIN_D)
    # long black-bead mangalsutra with gold pendant
    for k in range(41):
        a = math.radians(25 + 130 * k / 40)
        x, y = cx + 150 * S * math.cos(a), 660 * S + 330 * S * math.sin(a)
        d.ellipse([x - 5 * S, y - 5 * S, x + 5 * S, y + 5 * S], fill=(15, 15, 15) if k % 6 else GOLD)
    d.ellipse([cx - 20 * S, 975 * S, cx + 20 * S, 1025 * S], fill=GOLD, outline=(160, 110, 30), width=3 * S)
    # face (rounder)
    d.ellipse([cx - 195 * S, 200 * S, cx + 195 * S, 670 * S], fill=SKIN)
    # ears + small gold drop earrings
    for sx in (-1, 1):
        ex = cx + sx * 192 * S
        d.ellipse([ex - 26 * S, 400 * S, ex + 26 * S, 478 * S], fill=SKIN_D)
        d.ellipse([ex - 9 * S, 472 * S, ex + 9 * S, 490 * S], fill=GOLD)
        d.polygon([(ex, 486 * S), (ex - 12 * S, 515 * S), (ex, 540 * S), (ex + 12 * S, 515 * S)], fill=GOLD)
    # middle-parted hair sweeping to the temples
    for sx in (-1, 1):
        pts = []
        for k in range(21):
            a = math.radians(270 + sx * 90 * k / 20)
            pts.append((cx + 210 * S * math.cos(a), 420 * S + 245 * S * math.sin(a)))
        p0, c1, p2 = (cx + sx * 200 * S, 450 * S), (cx + sx * 80 * S, 320 * S), (cx + sx * 6 * S, 192 * S)
        for k in range(21):
            u = k / 20
            pts.append(((1-u)**2*p0[0] + 2*(1-u)*u*c1[0] + u*u*p2[0], (1-u)**2*p0[1] + 2*(1-u)*u*c1[1] + u*u*p2[1]))
        d.polygon(pts, fill=HAIR)
    # grey near the parting (early 40s) + sindoor
    d.line([(cx - 12 * S, 182 * S), (cx - 40 * S, 240 * S)], fill=(110, 105, 100), width=5 * S)
    d.line([(cx + 12 * S, 182 * S), (cx + 40 * S, 240 * S)], fill=(110, 105, 100), width=5 * S)
    d.polygon([(cx - 7 * S, 178 * S), (cx + 7 * S, 178 * S), (cx + 5 * S, 270 * S), (cx - 5 * S, 270 * S)], fill=(232, 70, 40))
    # nose + nose-ring hoop
    d.line([(cx, 420 * S), (cx - 14 * S, 520 * S), (cx + 10 * S, 528 * S)], fill=SKIN_D, width=7 * S)
    d.arc([cx + 18 * S, 505 * S, cx + 46 * S, 540 * S], 300, 240, fill=GOLD, width=4 * S)
    # small blue bindi
    d.ellipse([cx - 11 * S, 372 * S, cx + 11 * S, 394 * S], fill=(30, 110, 220))
    # subtle cheek / smile lines
    d.arc([cx - 150 * S, 500 * S, cx - 70 * S, 600 * S], 100, 160, fill=SKIN_D, width=4 * S)
    d.arc([cx + 70 * S, 500 * S, cx + 150 * S, 600 * S], 20, 80, fill=SKIN_D, width=4 * S)
    return im

def eyes(d, cx, openness):
    for sx in (-1, 1):
        ex, ey = cx + sx * 85 * S, 430 * S
        h = max(2, int(30 * S * openness))
        if openness > 0.15:
            d.ellipse([ex - 44 * S, ey - h, ex + 44 * S, ey + h], fill=(250, 246, 240))
            d.ellipse([ex - 22 * S, ey - min(h, 22 * S), ex + 22 * S, ey + min(h, 22 * S)], fill=(55, 35, 25))
            d.ellipse([ex - 10 * S, ey - min(h, 10 * S), ex + 10 * S, ey + min(h, 10 * S)], fill=(10, 8, 8))
            d.ellipse([ex + 4 * S, ey - 12 * S, ex + 11 * S, ey - 5 * S], fill=(255, 255, 255))
        d.arc([ex - 46 * S, ey - h - 4 * S, ex + 46 * S, ey + h + 4 * S], 190, 350, fill=HAIR, width=7 * S)
        if openness <= 0.15:
            d.line([(ex - 44 * S, ey), (ex + 44 * S, ey)], fill=HAIR, width=6 * S)

def mouth(d, cx, o):
    my = 585 * S
    lip = (150, 60, 60)
    if o < 0.12:
        d.arc([cx - 50 * S, my - 25 * S, cx + 50 * S, my + 15 * S], 20, 160, fill=lip, width=9 * S)
    else:
        h = int((10 + 42 * o) * S)
        w = int((44 - 6 * o) * S)
        d.ellipse([cx - w, my - h // 3, cx + w, my + h], fill=lip)
        d.ellipse([cx - w + 9 * S, my - h // 3 + 8 * S, cx + w - 9 * S, my + h - 7 * S], fill=(70, 20, 25))
        if o > 0.45:
            d.rectangle([cx - w + 16 * S, my - h // 3 + 8 * S, cx + w - 16 * S, my - h // 3 + 18 * S], fill=(245, 240, 235))

BASE = char_base()

FACES = {  # brow lift (inner, outer), eye scale, min mouth when talking, smile
    "neutral": (0, 0, 1.0, 0.0, False), "shock": (-38, -30, 1.4, 0.35, False),
    "stern": (22, -10, 0.85, 0.0, False), "worried": (-30, 6, 1.1, 0.0, False),
    "smile": (-4, -4, 0.9, 0.0, True)}

def brows(d, cx, face):
    li, lo, *_ = FACES[face]
    for sx in (-1, 1):
        pts = [(cx + sx * 35 * S, (370 + li) * S), (cx + sx * 88 * S, (350 + (li + lo) / 2 - 6) * S), (cx + sx * 148 * S, (372 + lo) * S)]
        d.line(pts, fill=HAIR, width=11 * S, joint="curve")

def character(o, eye_open, face="neutral"):
    li, lo, es, mmin, smile = FACES[face]
    im = BASE.copy()
    d = ImageDraw.Draw(im)
    cx = CW // 2
    brows(d, cx, face)
    eyes(d, cx, min(1.45, eye_open * es))
    if o > 0.05: o = max(o, mmin)
    if smile and o < 0.12:
        d.arc([cx - 62 * S, 545 * S, cx + 62 * S, 612 * S], 15, 165, fill=(150, 60, 60), width=10 * S)
    else:
        mouth(d, cx, o)
    return im.resize((CW // S, CH // S), Image.LANCZOS)

# ---------- 3. Background ----------
def background():
    bg = Image.new("RGB", (W, H))
    top, bot = np.array([246, 226, 190]), np.array([214, 160, 110])
    grad = np.linspace(0, 1, H)[:, None]
    arr = (top * (1 - grad) + bot * grad).astype(np.uint8)
    bg = Image.fromarray(np.repeat(arr[:, None, :], W, 1).reshape(H, W, 3))
    d = ImageDraw.Draw(bg)
    # jharokha-style window arch
    d.rounded_rectangle([170, 330, 910, 1350], 360, fill=(236, 205, 160))
    d.rounded_rectangle([200, 360, 880, 1350], 340, fill=(250, 236, 205))
    # tulsi pot on the right
    d.polygon([(860, 1180), (1020, 1180), (995, 1330), (885, 1330)], fill=(176, 92, 52))
    for i in range(9):
        a = -1.2 + i * 0.3
        x, y = 940 + 70 * math.sin(a), 1180 - 90 - 40 * math.cos(a * 2)
        d.ellipse([x - 22, y - 12, x + 22, y + 12], fill=(70, 130, 60))
    d.line([(940, 1180), (940, 1070)], fill=(60, 100, 50), width=6)
    return bg.filter(ImageFilter.GaussianBlur(3))
BG = background()

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
            paste_scaled(ov, emoji("🚽", 210), 230, 300, sc, -8)
            paste_scaled(ov, emoji("📱", 190), 850, 300, sc, 12)
            paste_scaled(ov, ti, W / 2, 470, sc)
        elif v["type"] == "sticker":
            paste_scaled(ov, emoji(v["e"], 300), 820, 470, sc, 10 * math.sin(ts * 6))
        elif v["type"] == "slam":
            big = v["big"]
            f = F_LATB(330) if big.isascii() else font(118)
            bi = text_img(big, f, (255, 220, 60) if big.isascii() else (255, 255, 255), 14, (150, 15, 30))
            z = 1 + 1.2 * max(0, 1 - p)         # slam in from big
            paste_scaled(ov, bi, W / 2, 470, min(z, 2.2) if p < 1 else 1 + 0.02 * math.sin(ts * 8))
            if v["small"]:
                si = text_img(v["small"], F_LATB(34), (255, 255, 255), 0)
                dd = ImageDraw.Draw(ov); dd.rounded_rectangle([W / 2 - si.width / 2, 650, W / 2 + si.width / 2, 650 + si.height], 16, fill=(0, 0, 0, 170))
                ov.paste(si, (int(W / 2 - si.width / 2), 650), si)
        elif v["type"] == "meter":
            q = min(1, (ts - s["start"]) / (s["end"] - s["start"]))
            lab = text_img(v["label"], font(64), (90, 15, 30), pad=0)
            ov.paste(lab, (100, 330), lab)
            d.rounded_rectangle([100, 440, 980, 520], 40, fill=(255, 255, 255, 220), outline=(120, 20, 40), width=6)
            col = (int(80 + 175 * q), int(180 - 150 * q), 50)
            d.rounded_rectangle([110, 450, 110 + int(860 * q), 510], 30, fill=col)
            paste_scaled(ov, emoji("⏰", 150), 900, 380, 1, 15 * math.sin(ts * 20) * q)
        elif v["type"] == "card":
            c = CARDS[s["id"]]
            x = W / 2 + (1 - min(1, p)) * -900
            paste_scaled(ov, c, x, 420, 1 if p >= 1 else 0.9 + 0.1 * p)
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
        ei = text_img("फ़ॉलो करें: रीना देवी", font(76), (255, 240, 210), 0, pad=24)
        bg = Image.new("RGBA", (ei.width + 60, ei.height + 20), (0, 0, 0, 0))
        ImageDraw.Draw(bg).rounded_rectangle([0, 0, bg.width - 1, bg.height - 1], 40, fill=(120, 20, 40)); bg.paste(ei, (30, 10), ei)
        paste_scaled(ov, bg, W / 2, 1720, back_ease(p))
    frame.paste(ov, (0, 0), ov)
    return frame

# ---------- 5. Render ----------
blink_val, tb, r2 = {}, 1.2, np.random.default_rng(7)
while tb < DUR:
    f0 = int(tb * FPS); blink_val.update({f0: 0.4, f0 + 1: 0.05, f0 + 2: 0.4}); tb += r2.uniform(2.5, 4.5)
flashes = [s["start"] for s in segs if s.get("flash")]
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                       "-r", str(FPS), "-i", "-", "-i", f"{WORK}/mix2.wav", "-c:v", "libx264", "-preset", "medium",
                       "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                       "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
cache, mo, zcur = {}, 0.0, 1.0
for i in range(NF):
    ts = i / FPS
    s = seg_at(ts) or segs[-1]
    target = float(np.clip((lvl[i] - 0.15) / 0.85, 0, 1)) if i < len(lvl) else 0
    mo += (target - mo) * 0.6
    key = (round(mo * 6) / 6, blink_val.get(i, 1.0), s["face"])
    if key not in cache: cache[key] = character(*key)
    ch = cache[key]
    # hard punch-in on line change, then slow drift
    since = ts - s["start"]
    z = s["zoom"] * (1 + 0.015 * max(0, since))
    cw, chh = int(ch.width * z), int(ch.height * z)
    chz = ch.resize((cw, chh), Image.BILINEAR)
    frame = BG.copy()
    bob = int(6 * math.sin(ts * 2.4) + 6 * min(1, lvl[i] if i < len(lvl) else 0))
    # zoom anchored on the face (face sits ~33% down the character canvas)
    fy = 0.33
    y0 = int(H - ch.height + 20 + ch.height * fy - chh * fy) + bob
    frame.paste(chz, ((W - cw) // 2 + int(5 * math.sin(ts * 0.9)), y0), chz)
    frame = draw_overlay(frame, ts)
    # shake + red flash on slam moments
    for f0 in flashes:
        dt = ts - f0
        if 0 <= dt < 0.35:
            k = 1 - dt / 0.35
            frame = Image.blend(frame, Image.new("RGB", (W, H), (220, 20, 30)), 0.45 * k)
            ox, oy = int(r2.integers(-18, 19) * k), int(r2.integers(-18, 19) * k)
            frame = frame.transform((W, H), Image.AFFINE, (1, 0, ox, 0, 1, oy), fillcolor=(30, 10, 10))
    ff.stdin.write(frame.convert("RGB").tobytes())
ff.stdin.close(); ff.wait()

def srt_t(x): return f"{int(x//3600):02}:{int(x%3600//60):02}:{int(x%60):02},{int(x%1*1000):03}"
with open(OUT.replace(".mp4", ".srt"), "w") as f:
    k = 1
    for s in segs:
        for pg in s["pages"]:
            f.write(f"{k}\n{srt_t(pg[0][0])} --> {srt_t(pg[-1][1])}\n{' '.join(w for _, _, w in pg)}\n\n"); k += 1
print(f"done: {DUR:.1f}s, {NF} frames, {len(cache)} poses")
for s in segs: print(s["id"], f"{s['start']:.2f}-{s['end']:.2f}", s["face"])

"""Reena Devi sample reel: script.json -> voiceover -> animated character -> captions/cards -> MP4.
Run: python3 build.py   (needs piper-tts, numpy, Pillow with raqm, ffmpeg, Noto Sans Devanagari)
"""
import json, math, subprocess, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = "/tmp/rd"
VOICE = os.environ.get("RD_VOICE", "/tmp/voice/hi_IN-priyamvada-medium.onnx")
LENGTH_SCALE = "0.85"          # <1 = faster speech; reels pace
W, H, FPS, SS = 1080, 1920, 25, 2   # SS = supersampling for the character art
GAP = 0.30                     # silence between lines (s)
SR = 22050
os.makedirs(f"{WORK}/vo", exist_ok=True)

FONT_B = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"
def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size, layout_engine=ImageFont.Layout.RAQM)

# ---------- 1. Voiceover ----------
script = json.load(open(f"{HERE}/script.json"))
def read_wav(p):
    with wave.open(p) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
segs, audio, t = [], [], 0.4
audio.append(np.zeros(int(0.4 * SR), np.float32))
for s in script:
    p = f"{WORK}/vo/{s['id']}.wav"
    subprocess.run(["python3", "-m", "piper", "-m", VOICE, "--length-scale", LENGTH_SCALE, "-f", p],
                   input=s["text"].encode(), check=True, capture_output=True)
    a = read_wav(p)
    segs.append({**s, "start": t, "end": t + len(a) / SR})
    audio += [a, np.zeros(int(GAP * SR), np.float32)]
    t += len(a) / SR + GAP
audio.append(np.zeros(int(1.2 * SR), np.float32))   # end-card tail
voice = np.concatenate(audio)
DUR = len(voice) / SR

# soft tanpura-like drone bed (generated, so no music licensing issue)
tt = np.arange(len(voice)) / SR
sa = 138.59
drone = sum(amp * np.sin(2 * np.pi * f * tt) for f, amp in
            [(sa, .5), (sa * 2, .25), (sa * 1.5, .3), (sa * 3, .1), (sa * 0.5, .3)])
drone *= 0.5 + 0.5 * np.sin(2 * np.pi * 0.12 * tt) ** 2
env = np.convolve(np.abs(voice), np.ones(4410) / 4410, "same")
duck = 1 - np.clip(env * 25, 0, 0.6)            # duck under speech
bed = drone / np.max(np.abs(drone)) * 0.06 * duck
mix = np.clip(voice * 0.95 + bed, -1, 1)
with wave.open(f"{WORK}/mix.wav", "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())

# per-frame loudness for lip sync
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
    # eyebrows
    for sx in (-1, 1):
        bx = cx + sx * 88 * S
        d.arc([bx - 62 * S, 345 * S, bx + 62 * S, 398 * S], 200, 340, fill=HAIR, width=9 * S)
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

def character(o, eye_open):
    im = BASE.copy()
    d = ImageDraw.Draw(im)
    cx = CW // 2
    eyes(d, cx, eye_open)
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

# ---------- 4. Overlays ----------
F_LAT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
F_TITLE, F_CAP, F_CARD, F_SMALL, F_BADGE = font(64), font(66), font(70), font(30, False), font(54)

def text_center(d, y, txt, f, fill, stroke=0, sfill=(0, 0, 0)):
    w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)

def wrap(txt, f, maxw, d):
    words, lines, cur = txt.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=f) <= maxw: cur = trial
        else: lines.append(cur); cur = wd
    lines.append(cur)
    return lines

def chunks(txt, n=4):
    w = txt.split()
    return [" ".join(w[i:i + n]) for i in range(0, len(w), n)]
for s in segs:
    cs = chunks(s["text"])
    total = sum(len(c) for c in cs)
    t0, s["chunks"] = s["start"], []
    for c in cs:
        dt = (s["end"] - s["start"]) * len(c) / total
        s["chunks"].append((t0, t0 + dt, c)); t0 += dt

def overlay(d, ts):
    # header bar
    d.rounded_rectangle([60, 90, W - 60, 200], 30, fill=(120, 20, 40))
    text_center(d, 100, "बवासीर: 5 घरेलू बातें", F_TITLE, (255, 240, 210))
    # disclosure (IT Rules 2026 synthetic-content label + medical disclaimer)
    d.rounded_rectangle([60, 222, 400, 274], 14, fill=(0, 0, 0, 160))
    d.text((80, 233), "AI", font=F_LAT, fill=(255, 255, 255))
    d.text((80 + d.textlength("AI", font=F_LAT) + 4, 226), "-जनित किरदार", font=F_SMALL, fill=(255, 255, 255))
    d.rectangle([0, H - 86, W, H], fill=(30, 10, 10, 190))
    text_center(d, H - 74, "सिर्फ़ जानकारी के लिए। इलाज के लिए डॉक्टर से सलाह लें।", F_SMALL, (255, 255, 255))
    seg = next((s for s in segs if s["start"] - GAP <= ts < s["end"] + GAP), None)
    if seg and seg["card"]:
        c = seg["card"]
        p = min(1, (ts - seg["start"] + GAP) / 0.25)        # slide-in
        x0 = int(-700 + 760 * p)
        red = "red" in c
        col = (190, 30, 30) if red else (255, 250, 238)
        if red:
            d.rounded_rectangle([x0, 300, x0 + 960, 330 + 92 + 70 * len(c["red"])], 36, fill=col)
            d.text((x0 + 40, 315), c["t"], font=F_CARD, fill=(255, 255, 255))
            for i, r in enumerate(c["red"]):
                d.ellipse([x0 + 60, 448 + 70 * i, x0 + 78, 466 + 70 * i], fill=(255, 220, 140))
                d.text((x0 + 98, 415 + 70 * i), r, font=font(52), fill=(255, 235, 235))
        else:
            d.rounded_rectangle([x0, 300, x0 + 900, 430], 36, fill=col, outline=(120, 20, 40), width=6)
            bw = max(110, int(d.textlength(c["n"], font=F_BADGE)) + 50)
            d.rounded_rectangle([x0 + 20, 315, x0 + 20 + bw, 415], 26, fill=(120, 20, 40))
            d.text((x0 + 20 + (bw - d.textlength(c["n"], font=F_BADGE)) / 2, 318), c["n"], font=F_BADGE, fill=(255, 220, 140))
            d.text((x0 + 50 + bw, 322), c["t"], font=F_CARD, fill=(90, 15, 30))
    # caption
    for s in segs:
        for a, b, c in s.get("chunks", []):
            if a <= ts < b:
                lines = wrap(c, F_CAP, W - 160, d)
                y = 1640 - 50 * (len(lines) - 1)
                d.rounded_rectangle([60, y - 10, W - 60, y + 100 * len(lines) + 10], 30, fill=(40, 10, 10, 170))
                for ln in lines:
                    text_center(d, y, ln, F_CAP, (255, 255, 255), stroke=7, sfill=(40, 10, 10)); y += 100
    # end card
    if ts > segs[-1]["end"] - 0.2:
        d.rounded_rectangle([140, 1630, W - 140, 1780], 40, fill=(120, 20, 40))
        text_center(d, 1648, "फ़ॉलो करें: रीना देवी", F_TITLE, (255, 240, 210))

# ---------- 5. Render ----------
blink_val = {}
tb = 1.5; rng = np.random.default_rng(7)
while tb < DUR:
    f0 = int(tb * FPS); blink_val.update({f0: 0.4, f0 + 1: 0.05, f0 + 2: 0.4}); tb += rng.uniform(2.5, 5)

ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                       "-r", str(FPS), "-i", "-", "-i", f"{WORK}/mix.wav", "-c:v", "libx264", "-preset", "medium",
                       "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest",
                       "-movflags", "+faststart", f"{HERE}/reena-devi-piles-sample.mp4"], stdin=subprocess.PIPE)
cache = {}
mo = 0.0
for i in range(NF):
    ts = i / FPS
    target = float(np.clip((lvl[i] - 0.15) / 0.85, 0, 1)) if i < len(lvl) else 0
    mo = mo + (target - mo) * 0.6
    q = round(mo * 6) / 6
    e = blink_val.get(i, 1.0)
    key = (q, e)
    if key not in cache: cache[key] = character(q, e)
    ch = cache[key]
    seg = next((s for s in segs if s["start"] - GAP <= ts < s["end"] + GAP), segs[-1])
    z = seg["zoom"] * (1 + 0.004 * math.sin(ts * 1.3))      # jump-cut zoom + breathing
    cw, chh = int(ch.width * z), int(ch.height * z)
    chz = ch.resize((cw, chh), Image.BILINEAR)
    frame = BG.copy()
    bob = int(6 * math.sin(ts * 2.1) + 5 * min(1, lvl[i] if i < len(lvl) else 0))
    frame.paste(chz, ((W - cw) // 2 + int(4 * math.sin(ts * 0.9)), H - chh + 20 + bob), chz)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay(ImageDraw.Draw(ov), ts)
    frame.paste(ov, (0, 0), ov)
    ff.stdin.write(frame.tobytes())
ff.stdin.close(); ff.wait()

# subtitle file + timing sheet for the editor
def srt_t(x): return f"{int(x//3600):02}:{int(x%3600//60):02}:{int(x%60):02},{int(x%1*1000):03}"
with open(f"{HERE}/reena-devi-piles-sample.srt", "w") as f:
    k = 1
    for s in segs:
        for a, b, c in s["chunks"]:
            f.write(f"{k}\n{srt_t(a)} --> {srt_t(b)}\n{c}\n\n"); k += 1
print(f"done: {DUR:.1f}s, {NF} frames, {len(cache)} cached poses")
for s in segs: print(s["id"], f"{s['start']:.2f}-{s['end']:.2f}")

"""CalaFly minimal sound design: no music, a few quiet, clean product-film sounds.

Principles: soft attacks (no clicks), sine/mallet tones instead of FM bells, gentle filtered-air swishes,
a short bright room reverb, nothing above ~9 kHz that could sound harsh on phone speakers,
and plenty of silence between cues. Mixed to -16 LUFS integrated, -1 dBTP.

Usage: python3 sound_min.py   (builds both mixes, writes stems, remuxes all 12 films)
"""
import json, os, subprocess, sys, tempfile
import numpy as np
from scipy import signal
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SR = 48000
DUR = 15.0
rng = np.random.default_rng(11)


def t_(d): return np.arange(int(d * SR)) / SR
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, "lowpass", fs=SR, output="sos"), x)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, "highpass", fs=SR, output="sos"), x)
def bp(x, a, b, o=2): return signal.sosfilt(signal.butter(o, [a, b], "bandpass", fs=SR, output="sos"), x)
def fade(x, a=0.004, r=0.02):
    n = len(x); e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.sin(np.linspace(0, np.pi / 2, na)) ** 2
    if nr: e[-nr:] *= np.cos(np.linspace(0, np.pi / 2, nr)) ** 2
    return x * e if x.ndim == 1 else x * e[:, None]
def st(x, pan=0.0, width=0.0):
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    d = int(width * 0.0006 * SR)
    return np.stack([x * l, np.roll(x, d) * r], 1)
def db(v): return 10 ** (v / 20)


# short, bright "studio" room: 0.7 s, dark above 7 kHz
def _ir():
    n = int(0.7 * SR); t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)) * np.exp(-t * 7.5)[:, None]
    ir = np.stack([lp(hp(ir[:, 0], 200), 7000), lp(hp(ir[:, 1], 200), 7000)], 1)
    return ir / np.sqrt((ir ** 2).sum())
IR = _ir()
def room(x, wet=0.18):
    if x.ndim == 1: x = st(x)
    y = np.stack([signal.fftconvolve(x[:, 0], IR[:, 0]), signal.fftconvolve(x[:, 1], IR[:, 1])], 1)
    out = np.zeros_like(y); out[: len(x)] = x * (1 - wet)
    return out + y * wet


# ---------- palette ----------
def mallet(f, d=0.6, bright=0.25):
    """soft marimba-like tone: fundamental + quick 4x partial, rounded attack"""
    t = t_(d)
    y = np.sin(2 * np.pi * f * t) * np.exp(-t * 7) + bright * np.sin(2 * np.pi * f * 3.98 * t) * np.exp(-t * 38)
    return fade(y, 0.003, 0.05)

def glass(f, d=0.5):
    """clean glassy tick: two slightly inharmonic sines"""
    t = t_(d)
    y = np.sin(2 * np.pi * f * t) * np.exp(-t * 14) + 0.22 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 34)
    return lp(fade(y, 0.003, 0.04), 5200)

def air(d=0.55, lo=700, hi=3200, up=True):
    """quiet swish: band-limited noise with a smooth swell, slight stereo drift"""
    n = int(d * SR); x = bp(rng.standard_normal(n), lo, hi)
    e = np.sin(np.pi * np.linspace(0, 1, n)) ** 2.2
    e *= np.linspace(0.6, 1, n) if up else np.linspace(1, 0.6, n)
    y = x * e
    pan = np.linspace(-0.35, 0.35, n)
    return np.stack([y * np.cos((pan + 1) * np.pi / 4), y * np.sin((pan + 1) * np.pi / 4)], 1)

def SWISH(): return room(air(0.5), 0.12) * db(-24)
def TAP():
    n = int(0.03 * SR); t = np.arange(n) / SR
    y = lp(hp(rng.standard_normal(n), 1800), 6000) * np.exp(-t * 700) * 0.5 + np.sin(2 * np.pi * 1700 * t) * np.exp(-t * 260) * 0.35
    return room(st(fade(y, 0.0005, 0.005)), 0.1) * db(-18)
def SHUTTER():  # camera focus lock: two tiny ticks
    y = np.zeros(int(0.12 * SR))
    for o in (0.0, 0.055):
        g = glass(2400, 0.05) * 0.6; s = int(o * SR); y[s: s + len(g)] += g
    return room(st(y), 0.1) * db(-22)
def NOTIF(level=-19):  # soft two-note glass, rising
    y = np.zeros(int(0.8 * SR)); a = glass(1567.98, 0.5); b = glass(2349.32, 0.6)
    y[: len(a)] += a; s = int(0.085 * SR); y[s: s + len(b)] += b * 0.85
    return room(st(y, 0.1, 0.5), 0.2) * db(level)
def CONFIRM(level=-15):  # success: three soft mallet notes, major sixth shape
    y = np.zeros(int(1.0 * SR))
    for i, f in enumerate([783.99, 987.77, 1318.51]):
        m = mallet(f, 0.6) * (1 - i * 0.12); s = int(i * 0.07 * SR); y[s: s + len(m)] += m
    return room(st(y, 0.0, 0.6), 0.22) * db(level)
def CHIME():  # cabin-style two-note, very soft sine (not an airline's chime)
    y = np.zeros(int(2.0 * SR)); a = mallet(659.25, 1.2, 0.08); b = mallet(523.25, 1.4, 0.08)
    y[: len(a)] += a; s = int(0.5 * SR); y[s: s + len(b)] += b
    return room(st(lp(y, 4000)), 0.28) * db(-21)
def TOUCHDOWN():  # soft low thump with a short tyre-on-tarmac texture, no screech
    t = t_(0.9)
    thump = np.sin(2 * np.pi * (52 + 30 * np.exp(-t * 25)) * t) * np.exp(-t * 9)
    tex = lp(rng.standard_normal(len(t)), 500, 4) * np.exp(-t * 6) * 0.6
    return st(fade(thump + tex, 0.004, 0.1)) * db(-13)
def AIR_BED(d):  # cabin air: smooth, high-passed so it never rumbles
    n = int(d * SR); x = lp(hp(rng.standard_normal(n), 120), 1600, 4)
    e = np.minimum(1, np.arange(n) / (0.8 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.8 * SR))
    return np.stack([x * e, np.roll(x, 700) * e], 1) * db(-38)
def ROOM_BED(d):
    n = int(d * SR); x = lp(hp(rng.standard_normal(n), 150), 1200, 2)
    e = np.minimum(1, np.arange(n) / (0.8 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.8 * SR))
    return np.stack([x * e, np.roll(x, 500) * e], 1) * db(-44)
def FLAPS(d=1.6):  # departure board: soft, sparse, filtered clicks that settle
    n = int(d * SR); y = np.zeros(n); t = 0.0
    while t < d:
        cl = int(0.003 * SR); s = int(t * SR)
        if s + cl < n:
            y[s: s + cl] += lp(bp(rng.standard_normal(cl), 1500, 5000), 6000) * np.exp(-np.arange(cl) / SR * 1600) * (0.4 + 0.6 * rng.random())
        t += (0.012 + 0.07 * (t / d) ** 2) * (0.5 + rng.random())
    y *= np.minimum(1, (n - np.arange(n)) / (0.25 * SR))
    return room(np.stack([y, np.roll(y, 29)], 1), 0.15) * db(-22)
def LOGO():  # end card: warm soft swell + one mallet note, short and calm
    d = 2.0; t = t_(d); y = np.zeros(len(t))
    for f in (261.63, 392.0, 493.88, 659.25):
        y += np.sin(2 * np.pi * f * t) * 0.18 + np.sin(2 * np.pi * f * 1.002 * t) * 0.12
    y = lp(y, 2400) * (np.minimum(1, t / 0.25) * np.exp(-np.maximum(0, t - 0.25) * 1.6))
    m = mallet(1046.5, 1.2, 0.15) * 0.7; y[: len(m)] += m
    return room(st(fade(y, 0.01, 0.3), 0.0, 0.8), 0.25) * db(-14)


CUES = {
    "wheels": [(0.0, "air", 6.2), (0.35, "chime"), (1.55, "touchdown"), (3.0, "swish"), (3.9, "notif"), (4.7, "notif_soft"),
               (6.0, "swish"), (6.7, "shutter"), (8.35, "confirm"), (8.6, "swish"), (10.8, "swish"), (11.6, "tap"),
               (11.9, "confirm_soft"), (13.0, "logo")],
    "sofa": [(0.0, "roomtone", 6.4), (0.25, "swish"), (2.4, "swish"), (3.4, "shutter"), (5.4, "confirm"), (6.2, "swish"),
             (6.5, "flaps", 1.6), (9.0, "swish"), (9.0, "air", 3.4), (9.6, "chime"), (10.6, "notif"), (11.4, "notif_soft"), (12.4, "logo")],
}
MAKE = {"air": AIR_BED, "roomtone": ROOM_BED, "chime": lambda a: CHIME(), "touchdown": lambda a: TOUCHDOWN(), "swish": lambda a: SWISH(),
        "notif": lambda a: NOTIF(), "notif_soft": lambda a: NOTIF(-23), "shutter": lambda a: SHUTTER(), "confirm": lambda a: CONFIRM(),
        "confirm_soft": lambda a: CONFIRM(-19), "tap": lambda a: TAP(), "flaps": lambda a: FLAPS(a or 1.6), "logo": lambda a: LOGO()}


def build(cues):
    n = int(DUR * SR) + 2 * SR; mix = np.zeros((n, 2))
    for c in cues:
        at, kind = c[0], c[1]; arg = c[2] if len(c) > 2 else None
        x = MAKE[kind](arg); s = int(at * SR); x = x[: n - s]; mix[s: s + len(x)] += x
    mix = mix[: int(DUR * SR)]
    mix = np.stack([hp(mix[:, 0], 35), hp(mix[:, 1], 35)], 1)
    f = int(0.3 * SR); mix[-f:] *= np.linspace(1, 0, f)[:, None] ** 2
    return mix


def loudnorm(x, out, target=-16):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fh: raw = fh.name
    wavfile.write(raw, SR, x.astype(np.float32))
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", f"loudnorm=I={target}:TP=-1.0:LRA=15:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(p[p.rindex("{"): p.rindex("}") + 1])
    af = (f"loudnorm=I={target}:TP=-1.0:LRA=15:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ar", str(SR), "-c:a", "pcm_s24le", out], check=True)
    os.remove(raw)


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    from music import remux
    codes = {"wheels": "V3_WHEELS-DOWN", "sofa": "V4_FROM-THE-SOFA"}
    import glob
    for v, code in codes.items():
        base = os.path.join(ROOT, "audio", f"CALAFLY_{code}")
        for old in glob.glob(base + "_*.wav"): os.remove(old)
        loudnorm(build(CUES[v]), base + "_MINIMAL.wav")
        print("mixed", os.path.basename(base) + "_MINIMAL.wav")
        if "--dry" in sys.argv: continue
        for f in sorted(glob.glob(os.path.join(ROOT, "videos", f"CALAFLY_*_{code}_*.mp4"))):
            tmp = f + ".tmp.mp4"; remux(f, base + "_MINIMAL.wav", tmp); os.replace(tmp, f)
            print("  remuxed", os.path.basename(f))

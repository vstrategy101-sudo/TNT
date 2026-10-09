"""CalaFly sound design: synthesises every SFX and the music bed, mixes them to the video cues.

Usage: python3 sound.py cues.json out_base duration
Writes out_base_MIX.wav (-14 LUFS, -1 dBTP), out_base_MUSIC.wav and out_base_SFX.wav stems (48 kHz stereo).
All sounds are generated here, so there is nothing to license.
"""
import json, subprocess, sys
import numpy as np
from scipy import signal

SR = 48000
rng = np.random.default_rng(26)


def t_(d): return np.arange(int(d * SR)) / SR
def env_ad(n, a, d, curve=4.0):
    """attack (s) then exponential decay over d seconds"""
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-4), np.exp(-(t - a) * curve / max(d, 1e-4)))
    return e
def bp(x, lo, hi, order=2): return signal.sosfilt(signal.butter(order, [lo, hi], "bandpass", fs=SR, output="sos"), x)
def lp(x, f, order=2): return signal.sosfilt(signal.butter(order, f, "lowpass", fs=SR, output="sos"), x)
def hp(x, f, order=2): return signal.sosfilt(signal.butter(order, f, "highpass", fs=SR, output="sos"), x)
def st(x, pan=0.0):
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    return np.stack([x * l, x * r], 1)
def put(y, x, o=0):
    """add x into y at sample offset o, growing y if needed"""
    end = o + len(x)
    if end > len(y): y = np.concatenate([y, np.zeros((end - len(y),) + y.shape[1:])])
    y[o:end] += x
    return y
def norm(x, peak=0.9): m = np.max(np.abs(x)) or 1; return x / m * peak
def bell(f, d, ratio=1.4, index=2.2, amp=1.0):
    t = t_(d); e = np.exp(-t * 5 / d)
    mod = np.sin(2 * np.pi * f * ratio * t) * index * e
    return amp * np.sin(2 * np.pi * f * t + mod) * e * np.minimum(1, t / 0.004)


# ---------- reverb ----------
def make_ir(dur=1.8, decay=3.2, tone=6500):
    n = int(dur * SR); t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)) * np.exp(-t * decay)[:, None]
    ir = np.stack([lp(ir[:, 0], tone), lp(ir[:, 1], tone)], 1)
    ir[: int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))[:, None]  # pre-delay softness
    return ir / np.sqrt(np.sum(ir ** 2))
IR = make_ir()
def reverb(x, wet=0.25):
    if x.ndim == 1: x = st(x)
    y = np.stack([signal.fftconvolve(x[:, 0], IR[:, 0]), signal.fftconvolve(x[:, 1], IR[:, 1])], 1)[: len(x) + int(1.2 * SR)]
    out = np.zeros_like(y); out[: len(x)] = x * (1 - wet)
    return out + y * wet


# ---------- SFX ----------
def whoosh(d=0.7, up=False):
    n = int(d * SR); x = rng.standard_normal(n)
    # time-varying band-pass: crossfade 24 filtered slices with a sweeping centre
    out = np.zeros(n); seg = n // 24; win = np.hanning(seg * 2)
    for i in range(24):
        fc = (300 * (14 ** (i / 23))) if up else (3800 * (0.12 ** (i / 23)) + 250)
        y = bp(x, max(60, fc * 0.6), min(SR / 2 - 100, fc * 1.6))
        s0 = max(0, i * seg - seg // 2); s1 = min(n, s0 + 2 * seg)
        out[s0:s1] += y[s0:s1] * win[: s1 - s0]
    e = np.sin(np.pi * np.linspace(0, 1, n)) ** (1.6 if up else 1.2)
    if up: e *= np.linspace(0.3, 1, n)
    y = out * e
    pan = np.linspace(-0.7, 0.7, n)
    return norm(np.stack([y * np.cos((pan + 1) * np.pi / 4), y * np.sin((pan + 1) * np.pi / 4)], 1), 0.7)

def tap():
    n = int(0.06 * SR); t = np.arange(n) / SR
    click = hp(rng.standard_normal(n), 2500) * np.exp(-t * 900)
    body = np.sin(2 * np.pi * 1350 * t) * np.exp(-t * 160) * 0.5
    return st(norm(click * 0.6 + body, 0.6), 0.05)

def pop():
    n = int(0.12 * SR); t = np.arange(n) / SR
    f = 900 * np.exp(-t * 18) + 500
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38)
    return st(norm(y, 0.55), 0.1)

def notif(soft=False):
    a = bell(1318.5, 0.9, ratio=3.01, index=0.9) ; b = bell(1975.5, 1.0, ratio=3.01, index=0.8)
    y = put(put(np.zeros(1), a * 0.8, 0), b, int(0.11 * SR))
    return reverb(st(norm(y, 0.5 if soft else 0.75), 0.15), 0.22)

def chime_seatbelt():
    a = bell(880, 1.6, ratio=2.0, index=0.6); b = bell(698.5, 1.9, ratio=2.0, index=0.6)
    y = put(put(np.zeros(1), a, 0), b, int(0.55 * SR))
    return reverb(st(lp(norm(y, 0.6), 5000)), 0.35)

def success():
    notes = [1046.5, 1318.5, 1568.0, 2093.0]; y = np.zeros(int(1.6 * SR))
    for i, f in enumerate(notes):
        y = put(y, bell(f, 1.1, ratio=1.41, index=1.6, amp=0.9 - i * 0.12), int(i * 0.075 * SR))
    return reverb(st(norm(y, 0.7)), 0.3)

def focus_beep():
    y = np.zeros(int(0.25 * SR))
    for o in (0, 0.09):
        t = t_(0.05); y = put(y, np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 60), int(o * SR))
    return st(norm(y, 0.35))

def progress(d=1.4):
    t = t_(d); f = 420 * (2 ** (t / d * 1.0))
    y = (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.2)
    return reverb(st(norm(y, 0.18)), 0.3)

def toast():
    w = whoosh(0.35, up=False) * 0.5; c = notif(True) * 0.6
    y = put(put(np.zeros((1, 2)), w, 0), c, int(0.15 * SR))
    return y

def landing():
    n = int(2.6 * SR); t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (48 + 40 * np.exp(-t * 12)) * t) * np.exp(-t * 7)
    screech = bp(rng.standard_normal(n), 900, 2600) * np.exp(-((t - 0.05) ** 2) / 0.004) * 0.25
    rumble = lp(rng.standard_normal(n), 160, 4) * (np.minimum(1, t / 0.1) * np.exp(-t * 1.1)) * 3
    y = thump * 1.0 + screech + rumble
    return reverb(st(norm(y, 0.9)), 0.15)

def ambience(d=6.0):
    n = int(d * SR); b = np.cumsum(rng.standard_normal(n)); b = hp(b, 20); b = lp(b, 380, 4)
    hiss = lp(hp(rng.standard_normal(n), 2000), 7000) * 0.05
    e = np.minimum(1, np.arange(n) / (0.4 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.6 * SR))
    l = norm(b, 0.22) + hiss; r = norm(np.roll(b, 900), 0.22) + np.roll(hiss, 500)
    return np.stack([l * e, r * e], 1)

def room(d=6.0):
    n = int(d * SR); x = lp(hp(rng.standard_normal(n), 80), 900, 2)
    e = np.minimum(1, np.arange(n) / (0.5 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.6 * SR))
    return st(norm(x, 0.07) * e)

def flaps(d=1.7):
    n = int(d * SR); y = np.zeros(n); t = 0.0
    while t < d:
        dens = 0.006 + 0.05 * (t / d) ** 2      # clicks thin out as the board settles
        cl = int(0.004 * SR); s = int(t * SR)
        if s + cl < n:
            c = bp(rng.standard_normal(cl), 1800 + rng.random() * 2500, 7000) * np.exp(-np.arange(cl) / SR * 1400) * (0.5 + rng.random() * 0.5)
            y[s: s + cl] += c
        t += dens * (0.4 + rng.random())
    y = y * np.minimum(1, (n - np.arange(n)) / (0.2 * SR))
    return reverb(np.stack([y, np.roll(y, 37)], 1) * 0.6, 0.18)

def riser(d=0.5):
    t = t_(d); f = 200 * (2 ** (t / d * 3))
    y = 0.4 * np.sin(2 * np.pi * np.cumsum(f) / SR) + hp(rng.standard_normal(len(t)), 3000) * (t / d) * 0.6
    return reverb(st(norm(y * (t / d) ** 1.5, 0.45)), 0.3)

def sting():
    chord = [261.63, 329.63, 392.0, 493.88, 587.33]; d = 2.0; t = t_(d); y = np.zeros(len(t))
    for i, f in enumerate(chord):
        for det in (-0.004, 0.004):
            y += signal.sawtooth(2 * np.pi * f * (1 + det) * t) * 0.12
    y = lp(y, 2200) * np.minimum(1, t / 0.03) * np.exp(-t * 1.4)
    y = put(y, bell(1568, 1.6, ratio=1.41, index=1.2) * 0.6, 0)
    return reverb(st(norm(y, 0.8)), 0.4)


# ---------- music bed: 112 bpm, Cmaj7 – Am9 – Fmaj7 – G6sus ----------
def ks_pluck(f, d, bright=0.5):
    n = int(d * SR); p = int(SR / f); buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; buf[i % p] = 0.996 * (bright * buf[i % p] + (1 - bright) * buf[(i + 1) % p])
    return out * np.exp(-np.arange(n) / SR * 3)

def music(dur):
    bpm = 112; beat = 60 / bpm; bar = beat * 4; n = int(dur * SR)
    chords = [[48, 55, 64, 71], [45, 52, 60, 67, 71], [41, 48, 57, 64], [43, 50, 59, 64]]
    mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
    pad = np.zeros(n); pl = np.zeros(n); kick = np.zeros(n); hat = np.zeros(n)
    t = np.arange(n) / SR
    cache = {}
    for b in range(int(dur / bar) + 1):
        ch = chords[b % 4]; s0 = int(b * bar * SR); s1 = min(n, int((b + 1) * bar * SR) + int(0.3 * SR))
        if s0 >= n: break
        tt = np.arange(s1 - s0) / SR
        e = np.minimum(1, tt / 0.4) * np.minimum(1, (s1 - s0 - np.arange(s1 - s0)) / (0.3 * SR))
        for m in ch:
            f = mtof(m + 12)
            for det in (-0.003, 0.0, 0.003):
                pad[s0:s1] += signal.sawtooth(2 * np.pi * f * (1 + det) * tt) * e * 0.05
        arp = [ch[1] + 24, ch[2] + 24, ch[3] + 24, ch[2] + 24]
        for k in range(8):
            s = int((b * bar + k * beat / 2) * SR)
            if s >= n: break
            m = arp[k % 4]
            if m not in cache: cache[m] = ks_pluck(mtof(m), 0.6, 0.55)
            p = cache[m][: n - s]; pl[s: s + len(p)] += p * (0.55 if k % 2 == 0 else 0.4)
        for k in range(4):
            s = int((b * bar + k * beat) * SR)
            if s >= n: break
            if k in (0, 2):
                kt = np.arange(int(0.35 * SR)) / SR; kk = np.sin(2 * np.pi * (50 + 70 * np.exp(-kt * 30)) * kt) * np.exp(-kt * 9)
                kick[s: s + len(kk)] += kk[: n - s]
            for h in (0, 0.5):
                hs = s + int(h * beat * SR); hn = int(0.04 * SR)
                if hs + hn < n: hat[hs: hs + hn] += hp(rng.standard_normal(hn), 7000) * np.exp(-np.arange(hn) / SR * 120) * (0.25 if h else 0.15)
    pad = lp(pad, 1500, 2)
    fade = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 1.2)
    L = pad * 0.9 + pl * 0.35 + kick * 0.5 + hat * 0.6
    R = np.roll(pad, 300) * 0.9 + np.roll(pl, 150) * 0.45 + kick * 0.5 + np.roll(hat, 80) * 0.5
    return reverb(np.stack([L * fade, R * fade], 1) * 0.55, 0.25)[:n]


SFX = {"whoosh": lambda a: whoosh(0.7), "whoosh_up": lambda a: whoosh(0.9, True), "tap": lambda a: tap(), "pop": lambda a: pop(),
       "notif": lambda a: notif(), "notif_soft": lambda a: notif(True), "chime_seatbelt": lambda a: chime_seatbelt(), "success": lambda a: success(),
       "focus_beep": lambda a: focus_beep(), "progress": lambda a: progress(a or 1.4), "toast": lambda a: toast(), "landing": lambda a: landing(),
       "ambience": lambda a: ambience(a or 6), "room": lambda a: room(a or 6), "flaps": lambda a: flaps(a or 1.7), "riser": lambda a: riser(a or 0.5),
       "sting": lambda a: sting()}
GAIN = {"whoosh": 0.55, "whoosh_up": 0.55, "tap": 0.7, "pop": 0.55, "notif": 0.7, "notif_soft": 0.5, "chime_seatbelt": 0.6, "success": 0.65,
        "focus_beep": 0.5, "progress": 0.5, "toast": 0.6, "landing": 0.85, "ambience": 0.4, "room": 0.6, "flaps": 0.75, "riser": 0.5, "sting": 0.75}


def build(cues, dur):
    n = int(dur * SR) + SR
    sfx = np.zeros((n, 2)); mus = np.zeros((n, 2)); duck = np.ones(n)
    for cue in cues:
        at, kind = cue[0], cue[1]; arg = cue[2] if len(cue) > 2 else None
        s = int(at * SR)
        if kind == "music":
            m = music(arg or dur); mus[s: s + len(m)] += m[: n - s]; continue
        x = SFX[kind](arg) * GAIN[kind]
        x = x[: n - s]; sfx[s: s + len(x)] += x
        if kind not in ("ambience", "room"):  # sidechain the music under each hit
            dl = min(len(x), int(0.5 * SR)); duck[s: s + dl] = np.minimum(duck[s: s + dl], 0.6)
    duck = signal.sosfiltfilt(signal.butter(1, 6, fs=SR, output="sos"), duck)
    mus *= duck[:, None]
    mix = mus * 0.8 + sfx
    mix = np.stack([hp(mix[:, 0], 28), hp(mix[:, 1], 28)], 1)
    mix = np.tanh(mix * 1.2) / np.tanh(1.2)  # gentle saturation / soft limiter
    cut = int(dur * SR)
    return mix[:cut], mus[:cut], sfx[:cut]


def write(path, x):
    from scipy.io import wavfile
    wavfile.write(path, SR, (np.clip(x, -1, 1) * 32767).astype(np.int16))


if __name__ == "__main__":
    cues = json.load(open(sys.argv[1])); base = sys.argv[2]; dur = float(sys.argv[3])
    mix, mus, sfx = build(cues, dur)
    write(base + "_RAW.wav", mix); write(base + "_MUSIC.wav", norm(mus, 0.8)); write(base + "_SFX.wav", norm(sfx, 0.9))
    # two-pass-free loudness target for social: -14 LUFS integrated, -1 dBTP
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", base + "_RAW.wav", "-af", "loudnorm=I=-14:TP=-1.0:LRA=11", "-ar", str(SR), base + "_MIX.wav"], check=True)
    import os; os.remove(base + "_RAW.wav")
    print("mixed", base)

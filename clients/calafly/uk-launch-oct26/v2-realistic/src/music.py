"""Licensed-music drop-in for the CalaFly films.

Cuts a licensed track (WAV/MP3/AIFF from Artlist, Epidemic Sound, Musicbed, etc.) to the film length
the way an editor would, keeping the track's own ending:

  body (from a strong downbeat) ──beat-aligned crossfade──► the track's real ending ("button")

then mixes it with the film's sound effects, ducks the music under each effect, normalises to
-14 LUFS / -1 dBTP and remuxes every film without re-rendering the picture.

Usage:
  python3 music.py --track wheels=path/to/trackA.wav --track sofa=path/to/trackB.wav \
                   [--sfx-dir path/to/licensed_sfx] [--synth-sfx] [--start wheels=12.3] [--dry]

Effects: a file in --sfx-dir named after a cue (whoosh.wav, notif.wav, landing.wav, chime_seatbelt.wav,
success.wav, tap.wav, pop.wav, flaps.wav, focus_beep.wav, toast.wav, riser.wav, sting.wav,
ambience.wav, room.wav, progress.wav, whoosh_up.wav, notif_soft.wav) is used for that cue.
Cues with no file are left silent unless --synth-sfx is given (then the built-in synth sounds fill in, -8 dB).
"""
import argparse, glob, json, os, subprocess, sys, tempfile
import numpy as np
from scipy import signal
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SR = 48000
DUR = 15.0
END_CARD = {"wheels": 13.0, "sofa": 12.4}   # where the end card lands; the button should arrive around here
VIDEO_CODE = {"wheels": "V3_WHEELS-DOWN", "sofa": "V4_FROM-THE-SOFA"}


def load(path):
    """decode anything ffmpeg reads to 48 kHz stereo float"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp = f.name
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", tmp], check=True)
    sr, x = wavfile.read(tmp); os.remove(tmp)
    return x.astype(np.float64)


def beats(x):
    import librosa
    mono = librosa.resample(x.mean(1), orig_sr=SR, target_sr=22050)
    tempo, bt = librosa.beat.beat_track(y=mono, sr=22050, units="time")
    onset = librosa.onset.onset_strength(y=mono, sr=22050)
    return float(np.atleast_1d(tempo)[0]), np.asarray(bt), onset


def rms_db(x, win):
    p = np.convolve((x ** 2).mean(1), np.ones(win) / win, mode="same")
    return 10 * np.log10(p + 1e-12)


def cut_to_length(x, dur=DUR, start=None, button_at=13.0):
    """Return (edit, info). The body starts on a strong beat; the track's final hit (its "button") lands on the end card."""
    import librosa
    tempo, bt, onset = beats(x)
    level = rms_db(x, int(0.4 * SR))
    loud = np.percentile(level, 70)
    end_ns = np.max(np.nonzero(level > loud - 30)[0]) / SR          # end of the audible ending incl. tail
    # final hit = last strong onset in the closing 8 s
    ot = librosa.frames_to_time(np.arange(len(onset)), sr=22050)
    win = (ot > end_ns - 8) & (ot < end_ns)
    if win.any():
        peak = onset[win].max(); idx = np.nonzero(win & (onset >= 0.5 * peak))[0]
        hit = float(ot[idx[-1]])
    else:
        hit = end_ns - (dur - button_at)
    # the ending starts one bar before the hit, on a beat, so the build-up into the button is kept
    bar = 4 * 60.0 / max(tempo, 1)
    pre = bt[(bt <= hit - 0.05) & (bt >= hit - bar - 0.3)]
    e0 = float(pre[0]) if len(pre) else max(0.0, hit - bar)
    lead = hit - e0                                                    # seconds from ending start to the hit
    # body: from a strong beat after any quiet intro
    if start is None:
        cand = [b for b in bt if b < e0 - dur and level[min(len(level) - 1, int((b + 1.0) * SR))] > loud - 3]
        start = cand[0] if cand else (bt[0] if len(bt) else 0.0)
    need = button_at - lead                                            # body length that lands the hit on the end card
    body_beats = bt[(bt > start) & (bt < e0)]
    cut = body_beats[np.argmin(np.abs((body_beats - start) - need))] if len(body_beats) else start + need
    body = x[int(start * SR): int(cut * SR)]
    ending = x[int(e0 * SR):]

    xf = int(0.045 * SR)  # equal-power crossfade at the splice
    if len(body) > xf and len(ending) > xf:
        t = np.linspace(0, np.pi / 2, xf)[:, None]
        edit = np.concatenate([body[:-xf], body[-xf:] * np.cos(t) + ending[:xf] * np.sin(t), ending[xf:]])
    else:
        edit = np.concatenate([body, ending])
    n = int(dur * SR)
    if len(edit) < n:
        edit = np.concatenate([edit, np.zeros((n - len(edit), 2))])
    edit = edit[:n]
    fo = int(0.35 * SR); edit[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2          # tail fades with the last frame
    fi = int(0.012 * SR); edit[:fi] *= np.linspace(0, 1, fi)[:, None]
    info = {"tempo": round(tempo, 1), "body_from": round(float(start), 2), "splice_at": round(float(cut), 2),
            "final_hit_in_track": round(hit, 2), "final_hit_lands": round(len(body) / SR - 0.045 + lead, 2), "end_card": button_at}
    return edit, info


def sfx_layer(cues, sfx_dir, synth):
    import sound
    n = int(DUR * SR) + SR
    out = np.zeros((n, 2)); hits = np.zeros(n)
    for cue in cues:
        at, kind = cue[0], cue[1]; arg = cue[2] if len(cue) > 2 else None
        if kind == "music": continue
        s = int(at * SR); x = None
        f = next((p for p in glob.glob(os.path.join(sfx_dir, kind + ".*"))), None) if sfx_dir else None
        if f:
            x = load(f) * 0.8
            if kind in ("ambience", "room") and arg:          # loop/trim beds to the cue length
                need = int(arg * SR); reps = int(np.ceil(need / len(x))); x = np.tile(x, (reps, 1))[:need]
                fd = int(0.5 * SR); x[-fd:] *= np.linspace(1, 0, fd)[:, None]
        elif synth:
            x = sound.SFX[kind](arg) * sound.GAIN[kind] * 0.4  # -8 dB: sits under licensed music
        if x is None: continue
        x = x[: n - s]; out[s: s + len(x)] += x
        if kind not in ("ambience", "room"): hits[s: s + min(len(x), int(0.45 * SR))] = 1
    return out[: int(DUR * SR)], hits[: int(DUR * SR)]


def mix(music, sfx, hits, duck_db=-4.0):
    g = np.where(hits > 0, 10 ** (duck_db / 20), 1.0)
    g = signal.sosfiltfilt(signal.butter(1, 5, fs=SR, output="sos"), g)       # smooth duck, no pumping clicks
    m = music * g[:, None] + sfx
    return m


def loudnorm(x, out_path):
    """two-pass EBU R128 to -14 LUFS / -1 dBTP"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        raw = f.name
    wavfile.write(raw, SR, np.clip(x, -4, 4).astype(np.float32))
    p1 = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    m = json.loads(p1[p1.rindex("{"): p1.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ar", str(SR), "-c:a", "pcm_s24le", out_path], check=True)
    os.remove(raw)


def remux(video_in, audio, video_out):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video_in, "-i", audio, "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", str(SR), "-shortest", "-movflags", "+faststart", video_out], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", action="append", default=[], help="video=path (video is wheels or sofa)")
    ap.add_argument("--start", action="append", default=[], help="video=seconds to force where the body starts")
    ap.add_argument("--sfx-dir", default=None)
    ap.add_argument("--synth-sfx", action="store_true")
    ap.add_argument("--dry", action="store_true", help="build the mixes only, don't touch the videos")
    a = ap.parse_args()
    sys.path.insert(0, HERE)
    starts = dict(s.split("=", 1) for s in a.start)
    for spec in a.track:
        v, path = spec.split("=", 1)
        x = load(path)
        edit, info = cut_to_length(x, start=float(starts[v]) if v in starts else None, button_at=END_CARD[v])
        cues = json.load(open(os.path.join(HERE, "cues", f"{v}.cues.json")))
        sfx, hits = sfx_layer(cues, a.sfx_dir, a.synth_sfx)
        base = os.path.join(ROOT, ".tmp" if a.dry else "audio", f"CALAFLY_{VIDEO_CODE[v]}")
        wavfile.write(base + "_MUSIC-EDIT.wav", SR, (edit * 0.9 / max(1e-9, np.abs(edit).max())).astype(np.float32))
        loudnorm(mix(edit, sfx, hits), base + "_MIX.wav")
        print(v, "edit:", info)
        if a.dry: continue
        for f in sorted(glob.glob(os.path.join(ROOT, "videos", f"CALAFLY_*_{VIDEO_CODE[v]}_*.mp4"))):
            tmp = f + ".tmp.mp4"; remux(f, base + "_MIX.wav", tmp); os.replace(tmp, f)
            print("  remuxed", os.path.basename(f))


if __name__ == "__main__":
    main()

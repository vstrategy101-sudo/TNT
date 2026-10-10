"""Warp a rendered CalaFly phone screen onto a model's blank phone, under their fingers.
Only dark (glass) pixels inside the phone outline are replaced, so fingers overlapping the screen stay on top."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
P = HERE.parent / "people"

def coeffs(src, dst):
    # perspective coefficients mapping output (dst) points back to input (src) points
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()

def warp(name, quad, screen="screen_ready.png", inset=0.035, blur=2.2):
    person = Image.open(P / f"{name}.png").convert("RGBA")
    scr = Image.open(P / screen).convert("RGBA")
    W, H = scr.size
    # shrink the quad slightly toward its centre so the bezel stays visible
    q = np.array(quad, float); c = q.mean(0); q = c + (q - c) * (1 - inset)
    warped = scr.filter(ImageFilter.GaussianBlur(blur)).transform(person.size, Image.PERSPECTIVE, coeffs([(0, 0), (W, 0), (W, H), (0, H)], q.tolist()), Image.BICUBIC)
    poly = Image.new("L", person.size, 0); ImageDraw.Draw(poly).polygon([tuple(p) for p in q], fill=255)
    rgb = np.asarray(person)[..., :3].astype(int)
    glass = (rgb.max(-1) < 70).astype(np.uint8) * 255
    m = np.minimum(np.asarray(poly), glass)
    m = Image.fromarray(m).filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.MinFilter(13)).filter(ImageFilter.GaussianBlur(1.2))  # close dust specks, keep fingers
    m = np.minimum(np.asarray(m), np.asarray(poly))
    out = person.copy(); out.paste(warped, (0, 0), Image.fromarray(m))
    out.save(P / f"{name}.png")
    print(name, "screen placed")

# White-tee man holding his phone out to camera. The cutout is mirrored so the phone sits on the right,
# so corners are the measured ones flipped across the 1515px width (TL, TR, BR, BL).
W = 1515
warp("pack", [(W - 449, 470), (W - 171, 458), (W - 144, 1069), (W - 428, 1084)])

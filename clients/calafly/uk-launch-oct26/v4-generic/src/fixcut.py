"""Patch cutouts where the model slipped, using the photo's plain studio backdrop as a colour key.

restore: inside a box, pixels that differ from the backdrop colour are added back (e.g. a black phone the model dropped).
defringe: in a band along the cutout's edge, pixels close to the backdrop colour are faded out (white halo in curly hair).
Boxes are in the photo's own pixel coordinates, before the cutout's crop.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from rembg import new_session, remove

HERE = Path(__file__).resolve().parent
RAW, OUT = HERE.parent / "people" / "raw", HERE.parent / "people"
session = new_session("u2net_human_seg")

def key(rgb, bg, lo, hi):
    """0 at the backdrop colour, 1 when the colour distance reaches hi."""
    d = np.sqrt(((rgb - bg) ** 2).sum(-1))
    return np.clip((d - lo) / (hi - lo), 0, 1)

def run(name, restore=None, defringe=None, bgpatch=(10, 10, 80, 80)):
    img = Image.open(RAW / f"{name}.jpg").convert("RGB")
    cut = remove(img, session=session, alpha_matting=True, alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=12, alpha_matting_erode_size=8)
    rgb = np.asarray(img).astype(np.float32)
    a = np.asarray(cut.getchannel("A")).astype(np.float32) / 255
    x0, y0, x1, y1 = bgpatch
    bg = rgb[y0:y1, x0:x1].reshape(-1, 3).mean(0)
    if restore:
        for (bx0, by0, bx1, by1) in restore:
            k = key(rgb[by0:by1, bx0:bx1], bg, 18, 45)
            a[by0:by1, bx0:bx1] = np.maximum(a[by0:by1, bx0:bx1], k)
    if defringe:
        hard = Image.fromarray((a > 0.5).astype(np.uint8) * 255)
        inner = np.asarray(hard.filter(ImageFilter.MinFilter(defringe * 2 + 1))) > 0
        band = (a > 0) & ~inner
        k = key(rgb, bg, 14, 40)
        a = np.where(band, np.minimum(a, k), a)
    # soften the hard key edges a touch
    al = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    out = img.convert("RGBA"); out.putalpha(al)
    box = al.point(lambda v: 255 if v > 20 else 0).getbbox()
    out = out.crop(box)
    out.save(OUT / f"{name}.png")
    print(name, out.size, "backdrop", bg.round())

# White-tee man: the phone and the hand holding it sit inside this box on a plain lavender backdrop.
run("pack", restore=[(150, 700, 720, 1430)], bgpatch=(1700, 60, 1880, 300))
# Shocked redhead: white backdrop leaking into the curls.
run("bill", defringe=26, bgpatch=(40, 40, 300, 300))

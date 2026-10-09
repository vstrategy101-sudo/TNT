"""Turn model photos into clean cutouts for the CalaFly brand ads.

Drop photos into ../people/raw/ named after the concept they're for (pack.jpg, number.jpg, bill.jpg,
refund.jpg, global.jpg). This removes the background, trims to the person and saves ../people/<concept>.png,
which generic.html picks up automatically.

Usage: python3 cutout.py            # every photo in people/raw
       python3 cutout.py bill.jpg   # one photo
"""
import sys
from pathlib import Path
from PIL import Image
from rembg import new_session, remove

HERE = Path(__file__).resolve().parent
RAW, OUT = HERE.parent / "people" / "raw", HERE.parent / "people"
OUT.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)

# People-tuned model that fits in this workspace's memory (the larger BiRefNet portrait model does not).
session = new_session("u2net_human_seg")

files = [RAW / a for a in sys.argv[1:]] or sorted(p for p in RAW.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})
for f in files:
    img = Image.open(f).convert("RGB")
    if max(img.size) > 2400:  # keep it quick; ads never need more
        img.thumbnail((2400, 2400))
    cut = remove(img, session=session, alpha_matting=True, alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=12, alpha_matting_erode_size=8)
    box = cut.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()
    if box:
        cut = cut.crop(box)
    dest = OUT / (f.stem + ".png")
    cut.save(dest)
    print(f"{f.name} -> {dest.name} {cut.size[0]}x{cut.size[1]}")

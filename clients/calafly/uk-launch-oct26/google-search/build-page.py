"""Builds plan.html (the shareable Google Search plan) from the Ads Editor files in editor/."""
import csv, json, os, io, base64
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ED = os.path.join(HERE, "editor")
rd = lambda n: list(csv.DictReader(open(os.path.join(ED, n))))

ads = rd("04_responsive_search_ads.csv")
kws = rd("03_keywords.csv")
groups = {}
for a in ads:
    g = a["Ad group"]
    groups[g] = {
        "campaign": a["Campaign"], "url": a["Final URL"], "p1": a["Path 1"], "p2": a["Path 2"],
        "h": [a[f"Headline {i}"] for i in range(1, 16) if a[f"Headline {i}"]],
        "d": [[a[f"Description {i}"], a[f"Description {i} position"]] for i in range(1, 5)],
        "kw": sorted({k["Keyword"] for k in kws if k["Ad group"] == g}),
    }
neg = [r["Keyword"] for r in rd("06_negatives_shared_list.csv")]
sl = [r for r in rd("07_sitelinks.csv") if r["Campaign"] == "CF_UK_SEARCH_DESTINATIONS"]
co = [r["Callout text"] for r in rd("08_callouts.csv") if r["Campaign"] == "CF_UK_SEARCH_DESTINATIONS"]

def thumb(name, w):
    im = Image.open(os.path.join(HERE, "images", name)).convert("RGB")
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=78)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
imgs = {k: {"sq": thumb(f"calafly-{k}-arrive-1x1.jpg", 360), "wide": thumb(f"calafly-{k}-home-191x1.jpg", 520)}
        for k in ("usa", "turkey", "dubai")}

data = {"groups": groups, "neg": neg, "sl": sl, "co": co, "imgs": imgs}
tpl = open(os.path.join(HERE, "plan.template.html")).read()
open(os.path.join(HERE, "plan.html"), "w").write(tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False)))
print("wrote plan.html", os.path.getsize(os.path.join(HERE, "plan.html")) // 1024, "KB")

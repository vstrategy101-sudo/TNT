"""Builds review.html: the launch playbook page with the creative gallery, videos and ad copy."""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
copy = json.load(open(os.path.join(ROOT, "copy", "copy.json")))

CONCEPTS = [
    ("01", "INTRO_MEET-CALAFLY", "Intro", "Meet CalaFly", "Prospecting"),
    ("02", "EASE_SET-UP-IN-MINUTES", "Easy setup", "Set up in minutes. From the sofa.", "Prospecting"),
    ("03", "PRICE_PAY-ONCE", "Pay once", "Pay once. Not per day.", "Prospecting"),
    ("04", "REFUND_IF-NOT-INSTALLED", "Refund", "Plans changed? Get a refund.", "Prospecting + retargeting"),
    ("05", "ALL-USP_DATA-SORTED", "All USPs", "{c} data, sorted.", "Prospecting, Google image assets"),
    ("06", "RETARGET_STILL-PLANNING", "Retarget", "Still planning {c}?", "Retargeting"),
]
COUNTRIES = [("usa", "USA"), ("turkey", "Turkey"), ("dubai", "Dubai")]
SIZES = [("1x1", "1:1"), ("4x5", "4:5"), ("9x16", "9:16"), ("191x1", "1.91:1")]

CONCEPTS_V2 = [
    ("R1", "WHEELS-DOWN-DATA-ON", "Wheels down. Data on.", "", "Prospecting · intro"),
    ("R2", "SET-UP-FROM-THE-SOFA", "Set up from the sofa", "", "Prospecting · easy setup"),
    ("R3", "PAY-ONCE-ORDER", "Pay once. Not per day.", "", "Prospecting · pricing"),
    ("R4", "REFUND-IF-NOT-INSTALLED", "Refund if not installed", "", "Prospecting + retargeting"),
    ("R5", "STILL-FLYING-RETARGET", "Still flying to …?", "", "Retargeting"),
]

def gallery(concepts=CONCEPTS, root="creatives"):
    out = []
    for key, label in COUNTRIES:
        cards = []
        for n, slug, name, head, role in concepts:
            base = f"{root}/{key}/CALAFLY_{key.upper()}_{n}_{slug.replace('SOFA', 'COUCH') if key == 'usa' else slug}"
            imgs = "".join(
                f'<img data-size="{s}" src="{base}_{s}.png" alt="{html.escape(name)} creative for {label}, {r}" loading="lazy"{" hidden" if s != "1x1" else ""}>'
                for s, r in SIZES)
            cards.append(f'''<figure class="ad">
  <div class="frame">{imgs}</div>
  <figcaption><span class="num">{n}</span><b>{name}</b><span class="role">{role}</span></figcaption>
</figure>''')
        out.append(f'<div class="grid" data-country="{key}"{" hidden" if key != "usa" else ""}>{"".join(cards)}</div>')
    return "\n".join(out)

def copy_blocks():
    out = []
    for key, label in COUNTRIES:
        g = copy["google"][key]
        m = copy["meta"][key]
        hl = "".join(f"<li><span>{html.escape(h)}</span><i>{len(h)}/30</i></li>" for h in g["headlines"])
        ds = "".join(f"<li><span>{html.escape(d)}</span><i>{len(d)}/90</i></li>" for d in g["descriptions"])
        meta_rows = ""
        for stage in ("prospecting", "retargeting"):
            for r in m[stage]:
                meta_rows += f'''<tr><td><span class="pill {stage}">{stage}</span><br><code>{r["creative"]}</code></td>
<td class="pt">{html.escape(r["primary"]).replace(chr(10), "<br>")}</td><td><b>{html.escape(r["headline"])}</b><br><span class="muted">{html.escape(r["description"])}</span></td></tr>'''
        kw = "".join(f"<div class=\"kwg\"><h5>{html.escape(grp)}</h5><p>{', '.join(html.escape(k) for k in kws)}</p></div>" for grp, kws in copy["keywords"][key].items())
        out.append(f'''<div class="copyset" data-country="{key}"{" hidden" if key != "usa" else ""}>
  <div class="two">
    <div><h4>Google RSA headlines</h4><ol class="lines">{hl}</ol></div>
    <div><h4>Google RSA descriptions</h4><ol class="lines">{ds}</ol>
      <h4 style="margin-top:28px">Keywords (phrase + exact)</h4>{kw}</div>
  </div>
  <h4 style="margin-top:36px">Meta ads</h4>
  <div class="tablewrap"><table class="meta"><thead><tr><th>Ad</th><th>Primary text</th><th>Headline / description</th></tr></thead><tbody>{meta_rows}</tbody></table></div>
</div>''')
    return "\n".join(out)

page = open(os.path.join(HERE, "review.template.html")).read()
def videos_v2():
    out = []
    for key, label in COUNTRIES:
        vids = []
        for code, name, note in [("V3_WHEELS-DOWN", "V3 · Wheels down", "Prospecting: Meta, YouTube, Demand Gen"), ("V4_FROM-THE-SOFA", "V4 · From the sofa", "Retargeting and mid-funnel")]:
            b = f"v2-realistic/videos/CALAFLY_{key.upper()}_{code.replace('SOFA', 'COUCH') if key == 'usa' else code}"
            vids.append(f'''<div class="video"><h3>{name}</h3><p class="muted">{note}</p>
  <div class="players"><video src="{b}_9x16.mp4" controls playsinline preload="metadata"></video><video src="{b}_16x9.mp4" controls playsinline preload="metadata"></video></div></div>''')
        out.append(f'<div class="vset videos" data-country="{key}"{" hidden" if key != "usa" else ""}>{"".join(vids)}</div>')
    return "\n".join(out)

def videos_brand():
    out = []
    for key, label in COUNTRIES:
        vids = []
        for code, name, note in [("B1_SORTED-BEFORE-YOU-FLY_30s", "B1 · Sorted before you fly (30s)", "Hero walkthrough: YouTube in-stream, Demand Gen, Reels"), ("B2_BUMPER_6s", "B2 · Bumper (6s)", "YouTube bumpers, Reels, Stories")]:
            b = f"v3-brand/videos/CALAFLY_{key.upper()}_{code}"
            vids.append(f'''<div class="video"><h3>{name}</h3><p class="muted">{note}</p>
  <div class="players"><video src="{b}_9x16.mp4" controls playsinline preload="metadata"></video><video src="{b}_16x9.mp4" controls playsinline preload="metadata"></video></div></div>''')
        out.append(f'<div class="vset videos" data-country="{key}"{" hidden" if key != "usa" else ""}>{"".join(vids)}</div>')
    return "\n".join(out)

page = page.replace("<!--BRAND_VIDEOS-->", videos_brand())
page = page.replace("<!--GALLERY_V2-->", gallery(CONCEPTS_V2, "v2-realistic/creatives")).replace("<!--VIDEOS_V2-->", videos_v2())
page = page.replace("<!--GALLERY-->", gallery()).replace("<!--COPY-->", copy_blocks())
page = page.replace("<!--NEG-->", ", ".join(html.escape(n) for n in copy["negatives"]))
page = page.replace("<!--BRAND-->", ", ".join(html.escape(n) for n in copy["brand"]))
open(os.path.join(ROOT, "review.html"), "w").write(page)
print("wrote review.html")

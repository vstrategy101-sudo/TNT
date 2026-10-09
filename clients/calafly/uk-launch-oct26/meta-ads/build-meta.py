"""Builds plan.html, the step-by-step Meta Ads launch guide for CalaFly (UK → USA, Dubai, Turkey).
Copy comes from ../copy/copy.json (written by src/build-copy.py) so the guide always matches the approved ad text.
Run: python3 build-meta.py
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
copy = json.load(open(os.path.join(HERE, "..", "copy", "copy.json")))

UTM = "utm_source=meta&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}"
# Destinations with a confirmed price go live first; the others join once their price lines are confirmed.
COUNTRIES = [("usa", "USA", True), ("dubai", "Dubai", False), ("turkey", "Turkey", False)]

def meta(key, stage, cre):
    for a in copy["meta"][key][stage]:
        if a["creative"] == cre: return a
    raise KeyError(cre)

def ads(key, label):
    K = label.upper()
    couch = "COUCH" if key == "usa" else "SOFA"
    p = [  # (ad name, creative files, copy key)
        (f"{K}_V3_WHEELS-DOWN", [f"v2-realistic/videos/CALAFLY_{K}_V3_WHEELS-DOWN_9x16.mp4", f"v2-realistic/videos/CALAFLY_{K}_V3_WHEELS-DOWN_16x9.mp4"], "VIDEO_01"),
        (f"{K}_R3_PAY-ONCE", [f"v2-realistic/creatives/{key}/CALAFLY_{K}_R3_PAY-ONCE-ORDER_4x5.png", f"v2-realistic/creatives/{key}/CALAFLY_{K}_R3_PAY-ONCE-ORDER_9x16.png"], "03_PRICE"),
        (f"{K}_03_PRICE-TICKET", [f"creatives/{key}/CALAFLY_{K}_03_PRICE_PAY-ONCE_4x5.png", f"creatives/{key}/CALAFLY_{K}_03_PRICE_PAY-ONCE_9x16.png"], "03_PRICE"),
        (f"{K}_05_ALL-USP", [f"creatives/{key}/CALAFLY_{K}_05_ALL-USP_DATA-SORTED_4x5.png", f"creatives/{key}/CALAFLY_{K}_05_ALL-USP_DATA-SORTED_9x16.png"], "05_ALL-USP"),
        (f"{K}_R2_SET-UP", [f"v2-realistic/creatives/{key}/CALAFLY_{K}_R2_SET-UP-FROM-THE-{couch}_4x5.png", f"v2-realistic/creatives/{key}/CALAFLY_{K}_R2_SET-UP-FROM-THE-{couch}_9x16.png"], "02_EASE"),
    ]
    r = [
        (f"{K}_R5_STILL-FLYING", [f"v2-realistic/creatives/{key}/CALAFLY_{K}_R5_STILL-FLYING-RETARGET_4x5.png", f"v2-realistic/creatives/{key}/CALAFLY_{K}_R5_STILL-FLYING-RETARGET_9x16.png"], "06_RETARGET"),
        (f"{K}_R4_REFUND", [f"v2-realistic/creatives/{key}/CALAFLY_{K}_R4_REFUND-IF-NOT-INSTALLED_4x5.png", f"v2-realistic/creatives/{key}/CALAFLY_{K}_R4_REFUND-IF-NOT-INSTALLED_9x16.png"], "04_REFUND"),
        (f"{K}_V4_SET-UP", [f"v2-realistic/videos/CALAFLY_{K}_V4_FROM-THE-{couch}_9x16.mp4", f"v2-realistic/videos/CALAFLY_{K}_V4_FROM-THE-{couch}_16x9.mp4"], "VIDEO_02"),
    ]
    out = {}
    for stage, rows, src in (("prospecting", p, "prospecting"), ("retargeting", r, "retargeting")):
        out[stage] = []
        for name, files, cre in rows:
            m = meta(key, src if cre != "VIDEO_02" or stage == "retargeting" else "prospecting", cre)
            out[stage].append({"name": name, "files": files, "primary": m["primary"], "headline": m["headline"],
                               "description": m["description"], "url": f"https://calafly.net/{key}"})
    return out

data = {"utm": UTM, "countries": [{"key": k, "label": l, "live": live, "ads": ads(k, l)} for k, l, live in COUNTRIES]}
tpl = open(os.path.join(HERE, "plan.template.html")).read()
tpl = tpl.replace("<!--STYLE-->", open(os.path.join(HERE, "_style.html")).read())
open(os.path.join(HERE, "plan.html"), "w").write(tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False)))
print("wrote plan.html", os.path.getsize(os.path.join(HERE, "plan.html")) // 1024, "KB")

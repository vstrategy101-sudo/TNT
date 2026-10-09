"""Builds the CalaFly ad copy sheets and checks every line against platform character limits.

Outputs ../copy/google_rsa.csv, ../copy/google_keywords.csv, ../copy/meta_ads.csv and ../copy/copy.json.
Google RSA limits: headline 30, description 90, path 15. Meta: headline ~40, description ~30 recommended.
"""
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "copy")
os.makedirs(OUT, exist_ok=True)

COUNTRIES = {
    "usa":    {"name": "the USA", "short": "USA",    "path": "usa",    "cities": ["New York", "Orlando", "Las Vegas"]},
    "turkey": {"name": "Turkey",  "short": "Turkey", "path": "turkey", "cities": ["Istanbul", "Antalya", "Dalaman"]},
    "dubai":  {"name": "Dubai",   "short": "Dubai",  "path": "dubai",  "cities": ["Dubai"]},
}

def rsa(c):
    s, n = c["short"], c["name"]
    headlines = [
        f"{s} eSIM by CalaFly",          # pin 1 option
        f"Mobile Data for {s}",
        f"Get Your {s} eSIM",
        "Set Up in Minutes",
        "Pay Once, Not Per Day",
        "One Price for Your Trip",
        "Refund if Not Installed",
        "Scan a QR Code at Home",
        "Land Connected",
        "Sorted Before You Fly",
        "Data-Only Travel eSIM",
        "Keep Your WhatsApp Number",
        f"Travel Data for {s}",
        "No Daily Charges From Us",
        "Official Site: CalaFly",
    ]
    descriptions = [
        f"Mobile data for {n}, sorted before you leave the UK. Scan a QR code, land connected.",
        "Pay once for your whole trip, not per day. Set up in minutes from the sofa.",
        "Plans changed? Get a refund if your eSIM is never installed. T&Cs apply.",
        "Data-only eSIM for unlocked, eSIM-compatible phones. Your WhatsApp number stays.",
    ]
    return headlines, descriptions

KEYWORDS = {
    "usa": {
        "eSIM": ["usa esim", "esim usa", "esim for usa", "us esim", "esim for america", "best esim for usa"],
        "Data / SIM": ["usa data sim", "us sim card for travel", "usa travel sim", "mobile data usa holiday", "sim card for usa from uk"],
        "Roaming intent": ["roaming in usa", "using phone in usa from uk", "mobile data in america from uk"],
        "Destinations": ["new york esim", "orlando esim", "florida esim", "las vegas esim"],
    },
    "turkey": {
        "eSIM": ["turkey esim", "esim turkey", "esim for turkey", "best esim for turkey"],
        "Data / SIM": ["turkey data sim", "turkey travel sim", "sim card for turkey from uk", "mobile data turkey holiday"],
        "Roaming intent": ["roaming in turkey", "using phone in turkey from uk", "mobile data in turkey"],
        "Destinations": ["istanbul esim", "antalya esim", "antalya sim card", "dalaman sim card"],
    },
    "dubai": {
        "eSIM": ["dubai esim", "esim dubai", "uae esim", "esim for dubai", "best esim for dubai"],
        "Data / SIM": ["dubai data sim", "dubai tourist sim", "sim card for dubai from uk", "mobile data dubai holiday"],
        "Roaming intent": ["roaming in dubai", "using phone in dubai from uk", "mobile data in uae"],
        "Destinations": ["abu dhabi esim", "uae travel sim"],
    },
}
BRAND = ["calafly", "cala fly", "calafly esim", "cala esim", "calafly.net"]
NEGATIVES = ["free", "jobs", "job", "career", "login", "log in", "my account", "customer service", "contact number",
             "phone number", "contract", "sim only deal", "pay monthly", "broadband", "wifi router", "pocket wifi",
             "apn settings", "unlock", "hack", "reddit"]

META = {
    "prospecting": [
        ("01_INTRO", "Meet CalaFly: mobile data for {n}, sorted before you leave the UK.\n\nPick your {s} plan, scan the QR code at home and land connected. One price for the whole trip, not per day. And if you never install it, you can get a refund (T&Cs apply).",
         "Meet CalaFly", "{s} data, sorted before you fly"),
        ("02_EASE", "Set up your {s} data in minutes, from the sofa.\n\n1. Pick your plan\n2. Scan the QR code\n3. Land connected\n\nData-only eSIM. Your WhatsApp number stays the same.",
         "Set up in minutes", "Scan a QR code at home"),
        ("03_PRICE", "Pay once. Not per day.\n\nCalaFly gives you one price for your whole trip to {n}. No daily charges from us, whether you stay for a long weekend or two weeks.",
         "Pay once, not per day", "One price for your whole trip"),
        ("04_REFUND", "Plans changed? If you never install your {s} eSIM, you can get your money back.\n\nRefund if not installed. T&Cs apply, see calafly.net.",
         "Refund if not installed", "Book your data with confidence"),
        ("05_ALL-USP", "{s} data, sorted.\n\n✓ Set up in minutes\n✓ Pay once, not per day\n✓ Refund if not installed (T&Cs apply)\n\nData-only eSIM for unlocked, eSIM-compatible phones.",
         "{s} data, sorted", "Set up in minutes. Pay once."),
        ("VIDEO_01", "Flying from the UK to {n}? Meet CalaFly. Set up in minutes, pay once (not per day), and get a refund if you never install it. T&Cs apply.",
         "Meet CalaFly", "Data for {n}, sorted"),
        ("VIDEO_02", "How CalaFly works: pick your {s} plan, scan the QR code at home, land connected. One price for the trip.",
         "Land connected in {s}", "Three steps, done before you fly"),
    ],
    "retargeting": [
        ("06_RETARGET", "Still planning {n}? Your data can be sorted tonight.\n\nOne price for the trip, set up in minutes, and a refund if you never install it (T&Cs apply).",
         "Still planning {s}?", "Your data, sorted tonight"),
        ("04_REFUND", "Not sure your plans are fixed? Book your {s} eSIM now. If you never install it, you can get a refund. T&Cs apply.",
         "Refund if not installed", "Book now, decide later"),
        ("VIDEO_02", "Three steps and you're connected in {n}. Pick, scan, land. Pay once, not per day.",
         "Pick. Scan. Land connected.", "Set up in minutes"),
    ],
}

problems = []
def check(kind, text, limit, where):
    if len(text) > limit:
        problems.append(f"{where}: {kind} is {len(text)} > {limit}: {text!r}")

copy = {"google": {}, "meta": {}, "keywords": KEYWORDS, "brand": BRAND, "negatives": NEGATIVES}
with open(os.path.join(OUT, "google_rsa.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Campaign", "Ad group", "Final URL", "Path 1", "Path 2"] + [f"Headline {i}" for i in range(1, 16)] + [f"Description {i}" for i in range(1, 5)])
    for key, c in COUNTRIES.items():
        h, d = rsa(c)
        for i, x in enumerate(h): check("headline", x, 30, f"{key} H{i+1}")
        for i, x in enumerate(d): check("description", x, 90, f"{key} D{i+1}")
        p1, p2 = c["path"], "esim"
        check("path", p1, 15, key)
        copy["google"][key] = {"headlines": h, "descriptions": d}
        w.writerow([f"CF_UK_SEARCH_{key.upper()}", "All ad groups", f"https://calafly.net/{c['path']}", p1, p2] + h + d)
    h = ["CalaFly Official Site", "CalaFly Travel eSIM", "USA, Turkey and Dubai", "Set Up in Minutes", "Pay Once, Not Per Day",
         "Refund if Not Installed", "Scan a QR Code at Home", "Land Connected", "Data-Only Travel eSIM", "Keep Your WhatsApp Number"]
    d = ["Travel eSIM data for the USA, Turkey and Dubai, sorted before you leave the UK.",
         "Pay once for your whole trip, not per day. Set up in minutes from the sofa.",
         "Refund if your eSIM is never installed. T&Cs apply.",
         "Data-only eSIM for unlocked, eSIM-compatible phones. Your WhatsApp number stays."]
    for i, x in enumerate(h): check("headline", x, 30, f"brand H{i+1}")
    for i, x in enumerate(d): check("description", x, 90, f"brand D{i+1}")
    copy["google"]["brand"] = {"headlines": h, "descriptions": d}
    w.writerow(["CF_UK_SEARCH_BRAND", "Brand", "https://calafly.net", "", ""] + h + [""] * (15 - len(h)) + d)

with open(os.path.join(OUT, "google_keywords.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Campaign", "Ad group", "Keyword", "Match type"])
    for key, groups in KEYWORDS.items():
        for g, kws in groups.items():
            for k in kws:
                w.writerow([f"CF_UK_SEARCH_{key.upper()}", g, k, "Phrase"])
                w.writerow([f"CF_UK_SEARCH_{key.upper()}", g, k, "Exact"])
    for k in BRAND:
        w.writerow(["CF_UK_SEARCH_BRAND", "Brand", k, "Exact"])
        w.writerow(["CF_UK_SEARCH_BRAND", "Brand", k, "Phrase"])
    for k in NEGATIVES:
        w.writerow(["ALL NON-BRAND (shared list)", "Negative", k, "Phrase (negative)"])

with open(os.path.join(OUT, "meta_ads.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Campaign", "Ad set", "Creative", "Primary text", "Headline", "Description", "CTA", "URL"])
    for key, c in COUNTRIES.items():
        copy["meta"][key] = {}
        for stage, rows in META.items():
            out = []
            for cre, pt, hl, ds in rows:
                pt, hl, ds = (x.format(n=c["name"], s=c["short"]) for x in (pt, hl, ds))
                check("meta headline", hl, 40, f"{key} {cre}")
                check("meta description", ds, 40, f"{key} {cre}")
                out.append({"creative": cre, "primary": pt, "headline": hl, "description": ds})
                camp = "CF_UK_META_PROSPECTING" if stage == "prospecting" else "CF_UK_META_RETARGETING"
                w.writerow([camp, f"{key.upper()}", cre, pt, hl, ds, "Shop now", f"https://calafly.net/{c['path']}"])
            copy["meta"][key][stage] = out

json.dump(copy, open(os.path.join(OUT, "copy.json"), "w"), indent=1, ensure_ascii=False)
if problems:
    print("\n".join(problems)); sys.exit(1)
print("all copy within limits")

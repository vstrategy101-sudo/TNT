"""Builds the CalaFly UK Google Search account as Google Ads Editor import files.

One destination campaign (USA, Turkey, Dubai) plus a small brand campaign.
Outputs editor/*.csv and images/*.jpg. Every line is checked against Google's limits:
headline 30, description 90, path 15, sitelink 25/35, callout 25, snippet value 25.
Run: python3 build-search.py
"""
import csv, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ED = os.path.join(HERE, "editor")
MC_IMG = os.path.join(HERE, "..", "..", "merchant-center", "images")

CAMP = "CF_UK_SEARCH_DESTINATIONS"
BRAND_CAMP = "CF_UK_SEARCH_BRAND"
SITE = "https://calafly.net"

COUNTRIES = {
    "usa":    {"S": "USA",    "n": "the USA", "path": "usa",
               "cities": ["New York", "Orlando", "Las Vegas"]},
    "turkey": {"S": "Turkey", "n": "Turkey",  "path": "turkey",
               "cities": ["Istanbul", "Antalya", "Dalaman"]},
    "dubai":  {"S": "Dubai",  "n": "Dubai",   "path": "dubai",
               "cities": ["Dubai", "Abu Dhabi", "the UAE"]},
}

# ad group theme -> keywords per country (phrase + exact for each)
KEYWORDS = {
    "usa": {
        "eSIM": ["usa esim", "esim usa", "esim for usa", "us esim", "esim for america", "best esim for usa",
                 "usa esim uk", "esim for usa trip", "esim usa holiday"],
        "Data SIM": ["usa data sim", "usa sim card", "us sim card for travel", "usa travel sim", "sim card for usa from uk",
                     "mobile data usa holiday", "usa sim card for tourists", "internet in usa for tourists"],
        "Roaming": ["roaming in usa", "using phone in usa from uk", "mobile data in america from uk", "usa roaming charges",
                    "phone data in usa", "ee roaming usa", "vodafone roaming usa", "o2 roaming usa", "three roaming usa"],
        "Cities": ["new york esim", "nyc esim", "orlando esim", "florida esim", "las vegas esim", "new york sim card",
                   "orlando sim card", "florida sim card"],
    },
    "turkey": {
        "eSIM": ["turkey esim", "esim turkey", "esim for turkey", "best esim for turkey", "turkiye esim",
                 "turkey esim uk", "esim turkey holiday"],
        "Data SIM": ["turkey data sim", "turkey sim card", "turkey travel sim", "sim card for turkey from uk",
                     "mobile data turkey holiday", "turkey sim card for tourists", "internet in turkey for tourists"],
        "Roaming": ["roaming in turkey", "using phone in turkey from uk", "mobile data in turkey", "turkey roaming charges",
                    "phone data in turkey", "ee roaming turkey", "vodafone roaming turkey", "o2 roaming turkey", "three roaming turkey"],
        "Cities": ["istanbul esim", "antalya esim", "dalaman esim", "bodrum esim", "antalya sim card", "dalaman sim card",
                   "istanbul sim card", "bodrum sim card"],
    },
    "dubai": {
        "eSIM": ["dubai esim", "esim dubai", "uae esim", "esim for dubai", "esim uae", "best esim for dubai",
                 "dubai esim uk", "esim dubai holiday"],
        "Data SIM": ["dubai data sim", "dubai sim card", "dubai tourist sim", "uae tourist sim", "sim card for dubai from uk",
                     "mobile data dubai holiday", "internet in dubai for tourists", "uae sim card"],
        "Roaming": ["roaming in dubai", "using phone in dubai from uk", "mobile data in uae", "dubai roaming charges",
                    "phone data in dubai", "ee roaming dubai", "vodafone roaming dubai", "o2 roaming dubai", "three roaming dubai"],
        "Cities": ["abu dhabi esim", "abu dhabi sim card", "uae travel sim", "esim for abu dhabi"],
    },
}
BRAND_KW = ["calafly", "cala fly", "calafly esim", "cala esim", "calafly.net", "cala eSIM uk"]

# Campaign-level negatives on the destination campaign (brand lives in its own campaign)
NEG_CAMPAIGN = ["calafly", "cala fly", "cala esim"]
# Shared list "CF_UK_NEGATIVES" on both campaigns
NEG_SHARED = [
    "free", "jobs", "job", "career", "careers", "login", "log in", "my account", "customer service", "contact number",
    "phone number", "contract", "sim only deal", "sim only", "pay monthly", "broadband", "home internet", "wifi router",
    "pocket wifi", "mifi", "apn settings", "unlock", "unlocked phone", "hack", "reddit", "not working", "how to cancel",
    "refund status", "transfer esim", "esim to physical sim", "wikipedia", "meaning", "what is esim",
    "uk esim for tourists", "esim for uk", "visiting uk", "europe", "eu roaming", "spain", "france", "italy", "greece",
    "portugal", "cheap flights", "flights", "hotel", "hotels", "visa", "weather", "currency",
    # competitor names: off at launch, so the account isn't paying for other brands' searches
    "holafly", "airalo", "nomad esim", "ubigi", "saily", "esim4travel", "gigsky", "maya mobile", "simoptions", "drimsim",
]

COMMON_H = ["Set Up in Minutes", "Pay Once, Not Per Day", "One Price for Your Trip", "Refund if Not Installed",
            "Scan a QR Code at Home", "QR Code Sent by Email", "Land Connected", "Sorted Before You Fly",
            "Data-Only Travel eSIM", "Keep Your WhatsApp Number", "No Daily Charges From Us"]

def headlines(theme, c):
    S, n, cities = c["S"], c["n"], c["cities"]
    first = {
        "eSIM":     [f"{S} eSIM by CalaFly", f"Get Your {S} eSIM", f"{S} Travel eSIM", "Official Site: CalaFly"],
        "Data SIM": [f"Mobile Data for {S}", f"{S} Travel SIM, as eSIM", "No SIM Card to Collect", f"{S} eSIM by CalaFly"],
        "Roaming":  [f"Using Your Phone in {S}?", f"Holiday Data for {S}", f"Travel Data for {S}", f"{S} eSIM by CalaFly"],
        "Cities":   [f"eSIM for {x.replace('the ', '')}" for x in cities] + [f"{S} eSIM by CalaFly"],
    }[theme]
    h = first + [x for x in COMMON_H if x not in first]
    return h[:15]

def descriptions(theme, c):
    n = c["n"]
    d1 = {
        "Roaming": f"Heading to {n}? One price for your trip's data, with no daily charges from us.",
        "Cities":  f"Data for {', '.join(c['cities'][:2])} and all of {n if n != 'Dubai' else 'the UAE'}. Set up before you leave the UK.",
    }.get(theme, f"Mobile data for {n}, sorted before you leave the UK. Scan a QR code, land connected.")
    # (text, pin). The two refund lines are both pinned to description 2, so a T&Cs line is in every ad shown.
    return [(d1, ""),
            ("Plans changed? Get a refund if your eSIM is never installed. T&Cs apply.", "2"),
            ("Pay once, not per day. Refund if your eSIM is never installed. T&Cs apply.", "2"),
            ("Data-only eSIM for unlocked, eSIM-compatible phones. Your WhatsApp number stays.", "")]

PATH2 = {"eSIM": "esim", "Data SIM": "data", "Roaming": "roaming", "Cities": "cities"}
BRAND_H = ["CalaFly Official Site", "CalaFly Travel eSIM", "USA, Turkey and Dubai", "Set Up in Minutes",
           "Pay Once, Not Per Day", "Refund if Not Installed", "Scan a QR Code at Home", "Land Connected",
           "Data-Only Travel eSIM", "Keep Your WhatsApp Number", "QR Code Sent by Email", "Sorted Before You Fly"]
BRAND_D = [("Travel eSIM data for the USA, Turkey and Dubai, sorted before you leave the UK.", ""),
           ("Plans changed? Get a refund if your eSIM is never installed. T&Cs apply.", "2"),
           ("Pay once, not per day. Refund if your eSIM is never installed. T&Cs apply.", "2"),
           ("Data-only eSIM for unlocked, eSIM-compatible phones. Your WhatsApp number stays.", "")]

# Sitelinks: URLs marked VERIFY must be checked on calafly.net before upload
SITELINKS = [
    (CAMP, "", "How It Works", "Pick a plan and scan a QR code", "Install at home before you fly", f"{SITE}/how-it-works"),
    (CAMP, "", "Refund Policy", "Refund if never installed", "See the full terms", f"{SITE}/refund-policy"),
    (CAMP, "", "Compatible Phones", "Check your phone supports eSIM", "Unlocked phones only", f"{SITE}/compatible-devices"),
    (CAMP, "", "Help and FAQs", "Install, data and refunds", "Answers before you buy", f"{SITE}/faq"),
    (CAMP, "", "USA eSIM", "Mobile data for the USA", "Set up in minutes", f"{SITE}/usa"),
    (CAMP, "", "Turkey eSIM", "Mobile data for Turkey", "Set up in minutes", f"{SITE}/turkey"),
    (CAMP, "", "Dubai eSIM", "Mobile data for Dubai and UAE", "Set up in minutes", f"{SITE}/dubai"),
    (CAMP, "", "Global eSIM", "One eSIM for 200+ countries", "Pay once for the plan", f"{SITE}/global"),
]
CALLOUTS = ["Set Up in Minutes", "Pay Once, Not Per Day", "Refund if Not Installed", "QR Code by Email",
            "Data-Only eSIM", "Keep Your WhatsApp Number", "Install Before You Fly", "No Daily Charges From Us"]
SNIPPET = ("Destinations", ["USA", "Turkey", "Dubai", "Spain", "France", "Italy", "Japan", "Thailand"])

problems = []
def chk(kind, s, lim, where):
    if len(s) > lim: problems.append(f"{where}: {kind} {len(s)}>{lim}: {s!r}")

def ag(key, theme): return f"{COUNTRIES[key]['S'].upper()} | {theme}"

def w(name, header, rows):
    with open(os.path.join(ED, name), "w", newline="") as f:
        x = csv.writer(f); x.writerow(header); x.writerows(rows)

# 1. Campaigns
w("01_campaigns.csv",
  ["Campaign", "Campaign Type", "Campaign Status", "Networks", "Budget", "Budget type", "Bid Strategy Type",
   "Max CPC Bid Limit", "Languages", "Location", "Targeting method", "Exclusion method", "Ad rotation",
   "Final URL suffix", "Start Date"],
  [[CAMP, "Search", "Paused", "Google search", "FILL daily", "Daily", "Maximize clicks", "0.60", "en",
    "United Kingdom", "Location of presence", "Location of presence", "Optimize",
    "utm_source=google&utm_medium=cpc&utm_campaign=cf_uk_search_destinations&utm_content={adgroupid}&utm_term={keyword}", ""],
   [BRAND_CAMP, "Search", "Paused", "Google search", "FILL daily", "Daily", "Maximize clicks", "0.30", "en",
    "United Kingdom", "Location of presence", "Location of presence", "Optimize",
    "utm_source=google&utm_medium=cpc&utm_campaign=cf_uk_search_brand&utm_content={adgroupid}&utm_term={keyword}", ""]])

# 2. Ad groups + 3. Keywords + 4. RSAs
groups, kws, ads = [], [], []
for key, themes in KEYWORDS.items():
    c = COUNTRIES[key]
    for theme, words in themes.items():
        g = ag(key, theme)
        url = f"{SITE}/{c['path']}"
        groups.append([CAMP, g, "Enabled", "Standard", url])
        for k in words:
            kws += [[CAMP, g, k, "Phrase", "Enabled"], [CAMP, g, k, "Exact", "Enabled"]]
        h, d = headlines(theme, c), descriptions(theme, c)
        for i, x in enumerate(h): chk("headline", x, 30, f"{g} H{i+1}")
        for i, (x, _) in enumerate(d): chk("description", x, 90, f"{g} D{i+1}")
        chk("path", c["path"], 15, g); chk("path", PATH2[theme], 15, g)
        ads.append([CAMP, g, "Responsive search ad", "Enabled", url, c["path"], PATH2[theme]]
                   + h + [""] * (15 - len(h)) + [x for x, _ in d] + [p for _, p in d])
groups.append([BRAND_CAMP, "Brand", "Enabled", "Standard", SITE])
for k in BRAND_KW:
    kws += [[BRAND_CAMP, "Brand", k.lower(), "Exact", "Enabled"], [BRAND_CAMP, "Brand", k.lower(), "Phrase", "Enabled"]]
for i, x in enumerate(BRAND_H): chk("headline", x, 30, f"brand H{i+1}")
for i, (x, _) in enumerate(BRAND_D): chk("description", x, 90, f"brand D{i+1}")
ads.append([BRAND_CAMP, "Brand", "Responsive search ad", "Enabled", SITE, "esim", "official"]
           + BRAND_H + [""] * (15 - len(BRAND_H)) + [x for x, _ in BRAND_D] + [p for _, p in BRAND_D])

w("02_ad_groups.csv", ["Campaign", "Ad group", "Ad group status", "Ad group type", "Final URL"], groups)
w("03_keywords.csv", ["Campaign", "Ad group", "Keyword", "Criterion Type", "Status"], kws)
w("04_responsive_search_ads.csv",
  ["Campaign", "Ad group", "Ad type", "Status", "Final URL", "Path 1", "Path 2"]
  + [f"Headline {i}" for i in range(1, 16)] + [f"Description {i}" for i in range(1, 5)]
  + [f"Description {i} position" for i in range(1, 5)], ads)

# 5. Negatives
neg = [[CAMP, "", k, "Campaign Negative Phrase"] for k in NEG_CAMPAIGN]
w("05_negatives_campaign.csv", ["Campaign", "Ad group", "Keyword", "Criterion Type"], neg)
w("06_negatives_shared_list.csv", ["Shared set name", "Keyword", "Criterion Type"],
  [["CF_UK_NEGATIVES", k, "Negative Phrase"] for k in NEG_SHARED])

# 6. Assets
sl = []
for camp, g, t, d1, d2, url in SITELINKS:
    chk("sitelink text", t, 25, t); chk("sitelink desc", d1, 35, t); chk("sitelink desc", d2, 35, t)
    sl.append([camp, g, t, d1, d2, url])
for t, d1, d2, url in [("Turkey eSIM", "Mobile data for Turkey", "Set up in minutes", f"{SITE}/turkey"),
                       ("How It Works", "Pick a plan and scan a QR code", "Install at home before you fly", f"{SITE}/how-it-works"),
                       ("Refund Policy", "Refund if never installed", "See the full terms", f"{SITE}/refund-policy"),
                       ("Compatible Phones", "Check your phone supports eSIM", "Unlocked phones only", f"{SITE}/compatible-devices")]:
    sl.append([BRAND_CAMP, "", t, d1, d2, url])
w("07_sitelinks.csv", ["Campaign", "Ad group", "Link text", "Description line 1", "Description line 2", "Final URL"], sl)
for x in CALLOUTS: chk("callout", x, 25, x)
w("08_callouts.csv", ["Campaign", "Callout text"], [[cmp, x] for cmp in (CAMP, BRAND_CAMP) for x in CALLOUTS])
for v in SNIPPET[1]: chk("snippet", v, 25, v)
w("09_structured_snippets.csv", ["Campaign", "Header", "Values"],
  [[cmp, SNIPPET[0], ";".join(SNIPPET[1])] for cmp in (CAMP, BRAND_CAMP)])

# 7. Image assets: Google Search images can't carry overlaid text or logos, so these are crops of the
# text-free Merchant Center lifestyle shots (1:1 1200x1200 and 1.91:1 1200x628), assigned per ad group country.
imgs = []
for key in COUNTRIES:
    for kind in ("arrive", "home"):
        src = Image.open(os.path.join(MC_IMG, f"calafly-{key}-esim-{kind}.jpg")).convert("RGB")
        sq = src.resize((1200, 1200), Image.LANCZOS)
        a = f"calafly-{key}-{kind}-1x1.jpg"; sq.save(os.path.join(HERE, "images", a), quality=90)
        top = int(1500 * (0.18 if kind == "arrive" else 0.08))
        wide = src.crop((0, top, 1500, top + 785)).resize((1200, 628), Image.LANCZOS)
        b = f"calafly-{key}-{kind}-191x1.jpg"; wide.save(os.path.join(HERE, "images", b), quality=90)
        for t in KEYWORDS[key]:
            imgs += [[CAMP, ag(key, t), a], [CAMP, ag(key, t), b]]
w("10_image_assets.csv", ["Campaign", "Ad group", "Image file (in images/)"], imgs)

if problems:
    print("\n".join(problems)); sys.exit(1)
print(f"ok: {len(groups)} ad groups, {len(kws)} keywords, {len(ads)} RSAs, {len(NEG_SHARED)} shared negatives, "
      f"{len(sl)} sitelinks, {len(imgs)} image links")

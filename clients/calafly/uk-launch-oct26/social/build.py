#!/usr/bin/env python3
"""CalaFly organic Instagram + Facebook posting plan.

One source for the calendar and captions. Writes:
  ../social-plan.html          the plan the team works from (open it from this folder, file links are relative)
  posting_schedule.csv         the same schedule as a sheet (import into Sheets / Meta Business Suite planning)

Run: python3 social/build.py   (from uk-launch-oct26/)
"""
import csv, html, os
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

C = {
    "usa":    dict(name="USA",    plan="3GB for 15 days", price="£7",  code="USA10",    url="calafly.net/destinations/esim-usa", tags="#USAtravel #NewYork #Florida"),
    "turkey": dict(name="Turkey", plan="10GB for 7 days", price="£11", code="TURKEY10", url="calafly.net/turkey",                tags="#Turkey #Antalya #Istanbul"),
    "dubai":  dict(name="Dubai",  plan="10GB for 7 days", price="£18", code="DUBAI10",  url="calafly.net/dubai",                 tags="#Dubai #WinterSun #DubaiTravel"),
}
ORDER = ["usa", "turkey", "dubai"]
BASE_TAGS = "#travelesim #esim #CalaFly"
REFUND_FINE = "100% refund if your eSIM is unused. T&Cs apply."
CODE_FINE = "10% off your first order, new customers only."

# ---------- asset paths ----------
def r1(c, n):  # round 1 statics
    names = {1: "01_INTRO_MEET-CALAFLY", 2: "02_EASE_SET-UP-IN-MINUTES", 3: "03_PRICE_PAY-ONCE",
             4: "04_REFUND_IF-NOT-INSTALLED", 5: "05_ALL-USP_DATA-SORTED", 6: "06_RETARGET_STILL-PLANNING"}
    return f"creatives/{c}/CALAFLY_{c.upper()}_{names[n]}"
def r2(c, n):  # round 2 realistic statics
    sofa = "COUCH" if c == "usa" else "SOFA"
    names = {1: "R1_WHEELS-DOWN-DATA-ON", 2: f"R2_SET-UP-FROM-THE-{sofa}", 3: "R3_PAY-ONCE-ORDER",
             4: "R4_REFUND-IF-NOT-INSTALLED", 5: "R5_STILL-FLYING-RETARGET"}
    return f"v2-realistic/creatives/{c}/CALAFLY_{c.upper()}_{names[n]}"
GEN = {1: "creatives/CALAFLY_GENERIC_G1_PASSPORT-CHARGER-DATA", 2: "creatives/CALAFLY_GENERIC_G2_SAME-NUMBER",
       3: "creatives/CALAFLY_GENERIC_G3_ROAMING-BILL", 4: "creatives/CALAFLY_GENERIC_G4_MONEY-BACK",
       5: "creatives/CALAFLY_GENERIC_G5_200-COUNTRIES"}
PPL = {1: "creatives-people/CALAFLY_PEOPLE_P1_DATA-ALREADY-ON", 2: "creatives-people/CALAFLY_PEOPLE_P2_SAME-NUMBER",
       3: "creatives-people/CALAFLY_PEOPLE_P3_ROAMING-SHOCK", 4: "creatives-people/CALAFLY_PEOPLE_P4_100-REFUND",
       5: "creatives-people/CALAFLY_PEOPLE_P5_200-COUNTRIES"}
def g(n): return f"v4-generic/{GEN[n]}"
def p(n): return f"v4-generic/{PPL[n]}"
def vid(key, c=None):
    if key == "V1": return "videos/CALAFLY_VIDEO_01_MEET-CALAFLY"
    if key == "V2": return "videos/CALAFLY_VIDEO_02_HOW-IT-WORKS"
    if key == "V3": return f"v2-realistic/videos/CALAFLY_{c.upper()}_V3_WHEELS-DOWN"
    if key == "V4": return f"v2-realistic/videos/CALAFLY_{c.upper()}_V4_FROM-THE-{'COUCH' if c == 'usa' else 'SOFA'}"
    if key == "B1": return f"v3-brand/videos/CALAFLY_{c.upper()}_B1_SORTED-BEFORE-YOU-FLY_30s"
    if key == "B2": return f"v3-brand/videos/CALAFLY_{c.upper()}_B2_BUMPER_6s"

def cover(v): return "social/covers/" + os.path.basename(v) + "_9x16.jpg"

# ---------- captions ----------
def offer(c):
    k = C[c]
    return f"{k['name']}: {k['plan']}, {k['price']}. New here? Code {k['code']} = {CODE_FINE.lower()}"

def tags(*cs):
    extra = " ".join(C[c]["tags"] for c in cs)
    return (BASE_TAGS + " " + extra).strip()

def all_offers():
    return "\n".join(f"{C[c]['name']}: {C[c]['plan']}, {C[c]['price']} (code {C[c]['code']})" for c in ORDER)

# Each post: day offset, time, format, files, caption, country (None = all/brand), title, cover/notes
P = []
def post(when, time, fmt, title, files, caption, c=None, note=""):
    P.append(dict(when=when, time=time, fmt=fmt, title=title, files=files, caption=caption.strip(), c=c, note=note))

LAUNCH = date(2026, 10, 19)          # Mon 19 Oct: launch grid over three days
W1 = date(2026, 10, 26)              # Mon 26 Oct: weekly rhythm starts (October half-term week)
def wk(n, dow): return W1 + timedelta(weeks=n - 1, days=dow)   # dow 0=Mon .. 5=Sat
MON, TUE, WED, THU, SAT = 0, 1, 2, 3, 5

# ===== Launch grid: 9 posts in 3 days. Posting order = bottom-right first, so P1 + the film end top-left. =====
post(LAUNCH, "10:00", "Feed", "P5 · One eSIM. 200+ countries.", [p(5) + "_4x5.png"], f"""
One eSIM. 200+ countries.

CalaFly is a travel eSIM: mobile data for your phone abroad, set up at home before you fly. Pick your destination, scan a QR code, and your data is ready when you land.

Pay once, not per day. Keep your own number and WhatsApp. {REFUND_FINE}

Link in bio.

{BASE_TAGS} #travel #UKtravel""")
post(LAUNCH, "13:00", "Feed", "G1 · Passport. Charger. Data.", [g(1) + "_4x5.png"], f"""
Passport. Charger. Data.

Add one more thing to the packing list. Set up your CalaFly eSIM from the sofa the week before you go, and you land with data already on.

Data-only eSIM for unlocked, eSIM-compatible phones. Link in bio.

{BASE_TAGS} #packinglist #holidayprep""")
post(LAUNCH, "18:00", "Feed", "01 · Meet CalaFly (USA)", [r1("usa", 1) + "_4x5.png"], f"""
Meet CalaFly. 👋

Mobile data for the USA, sorted before you leave the UK.

{offer('usa')}

Turkey and Dubai plans are live too. Link in bio.

{tags('usa')}""")
post(LAUNCH + timedelta(1), "10:00", "Feed", "P4 · Trip cancelled? 100% refund.", [p(4) + "_4x5.png"], f"""
Trip cancelled? 100% refund.

Buy your data early without the worry. If plans change and you never use your eSIM, you get your money back.

{REFUND_FINE} Link in bio.

{BASE_TAGS} #travelplans""")
post(LAUNCH + timedelta(1), "13:00", "Feed", "R1 · Wheels down. Data on. (Dubai)", [r2("dubai", 1) + "_4x5.png"], f"""
Wheels down. Data on.

Switch off flight mode in Dubai and your messages are already coming in. No airport SIM queue, no hunting for Wi-Fi.

{offer('dubai')}

Link in bio.

{tags('dubai')}""")
post(LAUNCH + timedelta(1), "18:00", "Feed", "G2 · Same number. Same WhatsApp.", [g(2) + "_4x5.png"], f"""
Same number. Same WhatsApp. No roaming.

Your normal SIM stays in your phone for calls, texts and WhatsApp. CalaFly only adds the data. Nothing to swap, nothing to lose.

Data-only eSIM for unlocked, eSIM-compatible phones. Link in bio.

{BASE_TAGS} #WhatsApp #roaming""")
post(LAUNCH + timedelta(2), "10:00", "Carousel", "05 · Data, sorted (USA, Turkey, Dubai)",
     [r1(c, 5) + "_4x5.png" for c in ["dubai", "usa", "turkey"]], f"""
Where are you off to? Swipe for your plan. ➡️

{all_offers()}

Every plan: set up in minutes, pay once (not per day), {REFUND_FINE.lower()}
Codes: {CODE_FINE}

Link in bio.

{tags('dubai', 'usa', 'turkey')}""", note="Slide order: Dubai, USA, Turkey (winter priority).")
post(LAUNCH + timedelta(2), "13:00", "Feed", "P1 · Land abroad. Data's already on.", [p(1) + "_4x5.png"], f"""
Land abroad. Data's already on.

That's the whole idea. Sort your data at home, and the first thing you do on arrival is message home, not look for Wi-Fi.

Pay once, not per day. Keep your number and WhatsApp. {REFUND_FINE}

Link in bio.

{BASE_TAGS} #arrivals #travel""")
post(LAUNCH + timedelta(2), "19:00", "Reel", "B1 · Sorted before you fly (Dubai, 30s)", [vid("B1", "dubai") + "_9x16.mp4"], f"""
Sorted before you fly. ✈️

1. Pick Dubai
2. Pay once
3. Scan the QR code at home
4. Land with data on

{offer('dubai')}
{REFUND_FINE}

Link in bio.

{tags('dubai')}""", note="Last launch post, so it sits top-left of the grid. Pin it.")

# ===== Week 1 · Easy: set up from the sofa (half-term week) =====
post(wk(1, MON), "12:30", "Feed", "R2 · Set up from the sofa (Dubai)", [r2("dubai", 2) + "_4x5.png"], f"""
Set up in minutes. From the sofa.

Laptop open on calafly.net, phone camera on the QR code, eSIM installed. Done before the kettle boils.

{offer('dubai')}

Link in bio.

{tags('dubai')}""")
post(wk(1, TUE), "19:00", "Reel", "V4 · From the sofa (Dubai, 15s)", [vid("V4", "dubai") + "_9x16.mp4"], f"""
Sofa → departures board → Dubai, with data on. 🛋️✈️

Install your CalaFly eSIM at home, then forget about it until you land.

{offer('dubai')}

Link in bio.

{tags('dubai')}""")
post(wk(1, WED), "12:30", "Carousel", "02 · Set up in minutes (USA, Turkey, Dubai)",
     [r1(c, 2) + "_4x5.png" for c in ["turkey", "usa", "dubai"]], f"""
Set up in minutes. Three steps, whichever way you're flying. ➡️

1. Pick your plan
2. Scan the QR code at home
3. Land connected

{all_offers()}
Codes: {CODE_FINE}

Link in bio.

{tags('turkey', 'usa', 'dubai')}""", note="Turkey first: half-term week.")
post(wk(1, THU), "19:00", "Reel", "B2 · Bumper (Turkey, 6s)", [vid("B2", "turkey") + "_9x16.mp4"], f"""
Half-term in Turkey? Sort the data tonight. 🇹🇷

{offer('turkey')}

Link in bio.

{tags('turkey')} #halfterm""")
post(wk(1, SAT), "10:00", "Feed", "R1 · Wheels down. Data on. (Turkey)", [r2("turkey", 1) + "_4x5.png"], f"""
Wheels down in Antalya. Data on.

Your CalaFly eSIM connects when you land, so the family group chat gets the "we're here" photo before you reach passport control.

{offer('turkey')}

Link in bio.

{tags('turkey')}""")

# ===== Week 2 · Fair: pay once, not per day =====
post(wk(2, MON), "12:30", "Feed", "G3 · The roaming bill you won't get", [g(3) + "_4x5.png"], f"""
The roaming bill you won't get.

Daily roaming passes add up: two weeks at £5 a day is £70. With CalaFly you pay once for the whole trip.

£5 a day is an example UK network daily pass. Link in bio.

{BASE_TAGS} #roaming #holidaymoney""")
post(wk(2, TUE), "19:00", "Reel", "V3 · Wheels down (USA, 15s)", [vid("V3", "usa") + "_9x16.mp4"], f"""
Touchdown at JFK. Phone wakes up. Messages arrive. 📲

{offer('usa')}
{REFUND_FINE}

Link in bio.

{tags('usa')}""")
post(wk(2, WED), "12:30", "Carousel", "R3 · Pay once. Not per day. (USA, Turkey, Dubai)",
     [r2(c, 3) + "_4x5.png" for c in ["usa", "dubai", "turkey"]], f"""
Pay once. Not per day. ➡️

One price for your whole trip:
{all_offers()}

No daily charges from us. Codes: {CODE_FINE}

Link in bio.

{tags('usa', 'dubai', 'turkey')}""")
post(wk(2, THU), "19:00", "Reel", "B1 · Sorted before you fly (USA, 30s)", [vid("B1", "usa") + "_9x16.mp4"], f"""
New York for Christmas? Sort the data before you fly. 🎄🗽

Pick, pay once, scan at home, land with data on.

{offer('usa')}
{REFUND_FINE}

Link in bio.

{tags('usa')}""")
post(wk(2, SAT), "10:00", "Feed", "P3 · £70 to use your phone abroad?", [p(3) + "_4x5.png"], f"""
£70 to use your phone abroad? Not this trip.

Pay once for your data, keep your number and WhatsApp, and get a 100% refund if you never use it.

£70 = an example UK network daily pass of £5 over 14 days. T&Cs apply. Link in bio.

{BASE_TAGS} #roaming #travelhacks""")

# ===== Week 3 · Safe: refund if unused =====
post(wk(3, MON), "12:30", "Feed", "G4 · Trip off? Money back.", [g(4) + "_4x5.png"], f"""
Trip off? Money back.

Book your data the day you book the flights. If the trip doesn't happen and the eSIM is never used, you get a 100% refund.

T&Cs apply. Link in bio.

{BASE_TAGS} #travelplans""")
post(wk(3, TUE), "19:00", "Reel", "V2 · How it works (15s)", [vid("V2") + "_9x16.mp4"], f"""
How CalaFly works, in 15 seconds. ⏱️

Pick. Scan. Land connected. One price, and a refund if you never install it.

Plans for the USA, Turkey, Dubai and 200+ countries. Link in bio.

{BASE_TAGS} #howitworks""")
post(wk(3, WED), "12:30", "Carousel", "R4 · Plans changed? Get a refund. (USA, Turkey, Dubai)",
     [r2(c, 4) + "_4x5.png" for c in ["dubai", "usa", "turkey"]], f"""
Plans changed? Get a refund. ➡️

Not installed → Request refund → done. It works the same on every plan.

{all_offers()}
{REFUND_FINE}

Link in bio.

{tags('dubai', 'usa', 'turkey')}""")
post(wk(3, THU), "19:00", "Reel", "V3 · Wheels down (Dubai, 15s)", [vid("V3", "dubai") + "_9x16.mp4"], f"""
Winter sun, data on. ☀️

Land in Dubai with your CalaFly eSIM already installed.

{offer('dubai')}

Link in bio.

{tags('dubai')}""")
post(wk(3, SAT), "10:00", "Feed", "P2 · Same number. No roaming bill.", [p(2) + "_4x5.png"], f"""
"Still on your normal number?" Yes. 😄

CalaFly adds data only. Your own SIM keeps your number, texts and WhatsApp, so nobody needs a new contact for you.

Pay once, not per day. {REFUND_FINE} Link in bio.

{BASE_TAGS} #WhatsApp #familytravel""")

# ===== Week 4 · Destinations =====
post(wk(4, MON), "12:30", "Feed", "01 · Meet CalaFly (Turkey)", [r1("turkey", 1) + "_4x5.png"], f"""
Meet CalaFly: mobile data for Turkey, sorted before you leave the UK.

{offer('turkey')}

Link in bio.

{tags('turkey')}""")
post(wk(4, TUE), "19:00", "Reel", "B1 · Sorted before you fly (Turkey, 30s)", [vid("B1", "turkey") + "_9x16.mp4"], f"""
Sorted before you fly. Turkey edition. 🇹🇷

Pick Turkey, pay once, scan at home, land with data on.

{offer('turkey')}
{REFUND_FINE}

Link in bio.

{tags('turkey')}""")
post(wk(4, WED), "12:30", "Carousel", "03 · Pay once (USA, Turkey, Dubai)",
     [r1(c, 3) + "_4x5.png" for c in ["dubai", "usa", "turkey"]], f"""
One price for your whole trip. Which one's yours? ➡️

{all_offers()}

Pay once, not per day. Codes: {CODE_FINE}

Link in bio.

{tags('dubai', 'usa', 'turkey')}""")
post(wk(4, THU), "19:00", "Reel", "V4 · From the couch (USA, 15s)", [vid("V4", "usa") + "_9x16.mp4"], f"""
Florida or New York, the setup is the same: couch, QR code, done. 🛋️

{offer('usa')}

Link in bio.

{tags('usa')}""")
post(wk(4, SAT), "10:00", "Feed", "G5 · One eSIM app. 200+ countries.", [g(5) + "_4x5.png"], f"""
One eSIM app. 200+ countries.

JFK, IST, DXB, BCN, BKK… find your tag. CalaFly has plans for 200+ destinations, all set up the same way.

Link in bio.

{BASE_TAGS} #travel #wanderlust""")

# ===== Week 5 · Christmas trips: New York and winter sun =====
post(wk(5, MON), "12:30", "Feed", "R2 · Set up from the couch (USA)", [r2("usa", 2) + "_4x5.png"], f"""
Christmas in New York? Sort the data from the couch tonight.

Scan the QR code at home and your eSIM is ready when you land.

{offer('usa')}

Link in bio.

{tags('usa')} #NYCatChristmas""")
post(wk(5, TUE), "19:00", "Reel", "V4 · From the sofa (Turkey, 15s)", [vid("V4", "turkey") + "_9x16.mp4"], f"""
Booked Turkey for next summer? The data takes two minutes now and it's refundable if you never install it. 🛋️

{offer('turkey')}
{REFUND_FINE}

Link in bio.

{tags('turkey')}""")
post(wk(5, WED), "12:30", "Carousel", "R5 · Still flying to…? (USA, Turkey, Dubai)",
     [r2(c, 5) + "_4x5.png" for c in ["usa", "dubai", "turkey"]], f"""
Still flying to the USA, Dubai or Turkey? Your data can be sorted tonight. ➡️

{all_offers()}

Pay once. {REFUND_FINE}

Link in bio.

{tags('usa', 'dubai', 'turkey')}""")
post(wk(5, THU), "19:00", "Reel", "B2 · Bumper (USA, 6s)", [vid("B2", "usa") + "_9x16.mp4"], f"""
USA data, sorted. 6 seconds, that's all. 🇺🇸

{offer('usa')}

Link in bio.

{tags('usa')}""")
post(wk(5, SAT), "10:00", "Feed", "R1 · Wheels down. Data on. (USA)", [r2("usa", 1) + "_4x5.png"], f"""
Wheels down. Data on. 🇺🇸

The first message from JFK should be "landed!", not "anyone know the Wi-Fi password?"

{offer('usa')}

Link in bio.

{tags('usa')}""")

# ===== Week 6 · Last call before the Christmas getaway =====
post(wk(6, MON), "12:30", "Feed", "01 · Meet CalaFly (Dubai)", [r1("dubai", 1) + "_4x5.png"], f"""
Dubai for winter sun? Meet CalaFly.

Mobile data for Dubai, sorted before you leave the UK.

{offer('dubai')}

Link in bio.

{tags('dubai')}""")
post(wk(6, TUE), "19:00", "Reel", "V3 · Wheels down (Turkey, 15s)", [vid("V3", "turkey") + "_9x16.mp4"], f"""
Landing in Turkey, connected. 🇹🇷

{offer('turkey')}
{REFUND_FINE}

Link in bio.

{tags('turkey')}""")
post(wk(6, WED), "12:30", "Carousel", "04 · Plans changed? 100% refund. (USA, Turkey, Dubai)",
     [r1(c, 4) + "_4x5.png" for c in ["dubai", "usa", "turkey"]], f"""
Booking early for next year? You can buy the data now too. ➡️

If your plans change and the eSIM is never used, it's a 100% refund.

{all_offers()}
T&Cs apply. Link in bio.

{tags('dubai', 'usa', 'turkey')}""")
post(wk(6, THU), "19:00", "Reel", "V1 · Meet CalaFly (15s)", [vid("V1") + "_9x16.mp4"], f"""
Meet CalaFly. 👋

Travel eSIM data, set up at home before you fly. Pay once, not per day, and get a refund if you never install it.

Link in bio.

{BASE_TAGS} #travel""")
post(wk(6, SAT), "10:00", "Feed", "R2 · Set up from the sofa (Turkey)", [r2("turkey", 2) + "_4x5.png"], f"""
Set up in minutes. From the sofa.

Turkey plans: {C['turkey']['plan']}, {C['turkey']['price']}. Install it whenever you like and it's ready when you land.

New here? Code TURKEY10: {CODE_FINE.lower()} Link in bio.

{tags('turkey')}""")

post(LAUNCH, "19:00", "Reel", "B2 · Bumper (Dubai, 6s)", [vid("B2", "dubai") + "_9x16.mp4"], f"""
Dubai data, sorted. Six seconds, that's the whole pitch. ☀️

{offer('dubai')}

Link in bio.

{tags('dubai')}""")

# ---------- the real schedule ----------
# Phase 1 (populate): 18 posts over two days, before the ads go live, so anyone who taps through from an ad
# lands on a full profile. Order = bottom-right of the grid first; the last post lands top-left.
# Phase 2 (daily): one post a day from the day the ads start.
POP1 = date(2026, 10, 14)
POP2 = date(2026, 10, 15)
DAILY = date(2026, 10, 16)
POP_TIMES = ["09:00", "09:45", "10:30", "11:15", "12:00", "13:30", "14:15", "15:00", "16:00"]
POPULATE = [
    # Day 1: rows 6, 5 and 4 of the grid (right to left)
    "P5 · One eSIM. 200+ countries.", "V2 · How it works (15s)", "01 · Meet CalaFly (USA)",
    "P2 · Same number. No roaming bill.", "B1 · Sorted before you fly (Turkey, 30s)", "R4 · Plans changed? Get a refund. (USA, Turkey, Dubai)",
    "V3 · Wheels down (Dubai, 15s)", "G1 · Passport. Charger. Data.", "P3 · £70 to use your phone abroad?",
    # Day 2: rows 3, 2 and 1
    "B1 · Sorted before you fly (USA, 30s)", "R3 · Pay once. Not per day. (USA, Turkey, Dubai)", "R1 · Wheels down. Data on. (Dubai)",
    "P4 · Trip cancelled? 100% refund.", "V4 · From the couch (USA, 15s)", "G2 · Same number. Same WhatsApp.",
    "05 · Data, sorted (USA, Turkey, Dubai)", "P1 · Land abroad. Data's already on.", "B1 · Sorted before you fly (Dubai, 30s)",
]
DAILY_ORDER = [
    "G3 · The roaming bill you won't get", "V4 · From the sofa (Dubai, 15s)", "02 · Set up in minutes (USA, Turkey, Dubai)",
    "B2 · Bumper (Turkey, 6s)", "R1 · Wheels down. Data on. (Turkey)", "V3 · Wheels down (Turkey, 15s)",
    "R2 · Set up from the sofa (Turkey)", "03 · Pay once (USA, Turkey, Dubai)", "V3 · Wheels down (USA, 15s)",
    "G4 · Trip off? Money back.", "B2 · Bumper (USA, 6s)", "R2 · Set up from the couch (USA)",
    "R5 · Still flying to…? (USA, Turkey, Dubai)", "V1 · Meet CalaFly (15s)", "01 · Meet CalaFly (Dubai)",
    "V4 · From the sofa (Turkey, 15s)", "G5 · One eSIM app. 200+ countries.", "B2 · Bumper (Dubai, 6s)",
    "04 · Plans changed? 100% refund. (USA, Turkey, Dubai)", "R1 · Wheels down. Data on. (USA)", "R2 · Set up from the sofa (Dubai)",
    "01 · Meet CalaFly (Turkey)",
]
_by = {x["title"]: x for x in P}
assert len(_by) == len(P) == len(POPULATE) + len(DAILY_ORDER), (len(_by), len(P))
assert set(POPULATE) | set(DAILY_ORDER) == set(_by)
_new = []
for i, t in enumerate(POPULATE):
    x = _by[t]; x["when"] = POP1 if i < 9 else POP2; x["time"] = POP_TIMES[i % 9]; x["phase"] = "populate"; _new.append(x)
for i, t in enumerate(DAILY_ORDER):
    x = _by[t]; x["when"] = DAILY + timedelta(i)
    weekend = x["when"].weekday() >= 5
    x["time"] = "19:00" if x["fmt"] == "Reel" else ("10:00" if weekend else "12:30")
    x["phase"] = "daily"; _new.append(x)
P[:] = _new
_by["B1 · Sorted before you fly (Dubai, 30s)"]["note"] = "Last populate post, so it sits top-left of the grid. Pin it."
_by["05 · Data, sorted (USA, Turkey, Dubai)"]["note"] = "Slide order: Dubai, USA, Turkey (winter priority). Pin it."
_by["P1 · Land abroad. Data's already on."]["note"] = "Pin it."
_by["B2 · Bumper (Turkey, 6s)"]["note"] = "October half-term starts the following weekend."

# ---------- story-only assets ----------
STORIES = [
    (DAILY + timedelta(3), "Story", "06 · Still planning Turkey?", [r1("turkey", 6) + "_9x16.png"], "turkey", "Link sticker → calafly.net/turkey. The week before half-term."),
    (DAILY + timedelta(10), "Story", "06 · Still planning USA?", [r1("usa", 6) + "_9x16.png"], "usa", "Link sticker → calafly.net/destinations/esim-usa."),
    (DAILY + timedelta(17), "Story", "06 · Still planning Dubai?", [r1("dubai", 6) + "_9x16.png"], "dubai", "Link sticker → calafly.net/dubai."),
]

HIGHLIGHTS = [
    ("How it works", [r2(c, 2) + "_9x16.png" for c in ORDER] + [vid("V2") + "_9x16.mp4"]),
    ("Prices", [r1(c, 5) + "_9x16.png" for c in ORDER]),
    ("Refunds", [r2(c, 4) + "_9x16.png" for c in ORDER]),
    ("USA", [r2("usa", 1) + "_9x16.png", r2("usa", 3) + "_9x16.png", vid("B2", "usa") + "_9x16.mp4"]),
    ("Turkey", [r2("turkey", 1) + "_9x16.png", r2("turkey", 3) + "_9x16.png", vid("B2", "turkey") + "_9x16.mp4"]),
    ("Dubai", [r2("dubai", 1) + "_9x16.png", r2("dubai", 3) + "_9x16.png", vid("B2", "dubai") + "_9x16.mp4"]),
]

def story_version(f):
    """9:16 version of a feed file, for the same-day story reshare."""
    if f.endswith("_4x5.png") and "v4-generic" not in f:
        return f.replace("_4x5.png", "_9x16.png")
    return None

def fb_caption(cap, c):
    url = C[c]["url"] if c else "calafly.net"
    return cap.replace("Link in bio.", f"Get yours: https://{url}")

# ---------- checks ----------
def check():
    missing = []
    for x in P:
        for f in x["files"]:
            if not os.path.exists(os.path.join(ROOT, f)): missing.append(f)
            if f.endswith(".mp4") and not os.path.exists(os.path.join(ROOT, cover(f[:-9]))): missing.append(cover(f[:-9]))
    for s in STORIES:
        for f in s[3]:
            if not os.path.exists(os.path.join(ROOT, f)): missing.append(f)
    for _, fs in HIGHLIGHTS:
        for f in fs:
            if not os.path.exists(os.path.join(ROOT, f)): missing.append(f)
    for x in P:
        if len(x["caption"]) > 2200: missing.append("caption too long: " + x["title"])
        if x["caption"].count("#") > 30: missing.append("too many hashtags: " + x["title"])
    assert not missing, "\n".join(missing)

def country_of(x):
    t = x["title"]
    if "(" not in t: return None
    inside = [w.strip() for w in t.rsplit("(", 1)[1].rstrip(")").split(",")]
    hits = [c for c in ORDER if C[c]["name"] in inside]
    return hits[0] if len(hits) == 1 else None

for x in P: x["c"] = country_of(x)

# ---------- CSV ----------
def write_csv():
    with open(os.path.join(ROOT, "social", "posting_schedule.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["#", "Date", "Day", "Time (UK)", "Format", "Post", "Files (in order)", "Instagram caption", "Facebook caption", "Reel cover", "Story reshare file", "Notes"])
        for i, x in enumerate(P, 1):
            vids = [f for f in x["files"] if f.endswith(".mp4")]
            cov = cover(vids[0][:-9]) if vids else ""
            sv = story_version(x["files"][0]) or (x["files"][0] if vids else "")
            w.writerow([i, x["when"].isoformat(), x["when"].strftime("%a"), x["time"], x["fmt"], x["title"],
                        " | ".join(x["files"]), x["caption"], fb_caption(x["caption"], x["c"]), cov, sv, x["note"]])
        for s in STORIES:
            w.writerow(["S", s[0].isoformat(), s[0].strftime("%a"), "18:00", s[1], s[2], " | ".join(s[3]), "", "", "", "", s[5]])

# ---------- HTML ----------
E = html.escape
def media(f, cls=""):
    if f.endswith(".mp4"):
        c = cover(f[:-9]) if "_9x16" in f else ""
        return f'<video class="m {cls}" src="{E(f)}" poster="{E(c)}" controls muted playsinline preload="none"></video>'
    return f'<img class="m {cls}" src="{E(f)}" alt="" loading="lazy">'

def filelink(f):
    return f'<a class="file" href="{E(f)}" target="_blank" rel="noopener">{E(os.path.basename(f))}</a>'

def post_card(i, x):
    vids = [f for f in x["files"] if f.endswith(".mp4")]
    thumbs = "".join(media(f) for f in x["files"])
    multi = " multi" if len(x["files"]) > 1 else ""
    fmtcls = x["fmt"].lower()
    extra = []
    if vids:
        extra.append(f'<div class="kv"><span>Reel cover</span>{filelink(cover(vids[0][:-9]))}</div>')
    sv = story_version(x["files"][0])
    if sv:
        extra.append(f'<div class="kv"><span>Story reshare</span>{filelink(sv)}</div>')
    elif vids:
        extra.append('<div class="kv"><span>Story reshare</span><em>Share the Reel to Story</em></div>')
    else:
        extra.append('<div class="kv"><span>Story reshare</span><em>Share the post to Story</em></div>')
    if x["note"]:
        extra.append(f'<div class="kv"><span>Note</span>{E(x["note"])}</div>')
    fb = fb_caption(x["caption"], x["c"])
    return f'''
<article class="post" id="post-{i}">
  <div class="thumbs{multi}">{thumbs}</div>
  <div class="pbody">
    <div class="phead"><span class="num">#{i:02d}</span><span class="fmt {fmtcls}">{E(x["fmt"])}</span><span class="when">{x["when"].strftime("%a %-d %b")} · {x["time"]}</span></div>
    <h4>{E(x["title"])}</h4>
    <div class="files"><span>Files</span>{"".join(filelink(f) for f in x["files"])}</div>
    {"".join(extra)}
    <div class="caps">
      <div class="cap"><div class="caphead"><b>Instagram</b><button type="button" class="copy" data-t="ig{i}">Copy</button></div><pre id="ig{i}">{E(x["caption"])}</pre></div>
      <div class="cap"><div class="caphead"><b>Facebook</b><button type="button" class="copy" data-t="fb{i}">Copy</button></div><pre id="fb{i}">{E(fb)}</pre></div>
    </div>
  </div>
</article>'''

def grid_preview():
    newest_first = list(reversed([x for x in P if x["phase"] == "populate"]))
    cells = []
    for x in newest_first:
        f = x["files"][0]
        src = cover(f[:-9]) if f.endswith(".mp4") else f
        badge = {"Reel": "▶", "Carousel": "❐"}.get(x["fmt"], "")
        cells.append(f'<div class="cell"><img src="{E(src)}" alt="{E(x["title"])}" loading="lazy">{f"<i>{badge}</i>" if badge else ""}</div>')
    return "".join(cells)

def week_blocks():
    pop = [x for x in P if x["phase"] == "populate"]
    blocks = [
        ("Populate · Day 1", POP1.strftime("%a %-d %b"), "Nine posts, about 45 minutes apart. These become the bottom three rows of the grid. Post them in exactly this order.", pop[:9], "populate"),
        ("Populate · Day 2", POP2.strftime("%a %-d %b"), "Nine more, same spacing. These become the top three rows. The last one (the Dubai film) ends up top-left. Pin it, P1 and the prices carousel. Switch the ads on once this day is done.", pop[9:], "populate"),
    ]
    daily = [x for x in P if x["phase"] == "daily"]
    weeks = {}
    for x in daily:
        monday = x["when"] - timedelta(days=x["when"].weekday())
        weeks.setdefault(monday, []).append(x)
    notes = ["The ads go live. One post a day from here, alternating images and Reels.",
             "October half-term week: lead with Turkey and the setup story.",
             "Start the Christmas push: New York and Dubai winter sun.",
             "Last week of the current set. Plan new content for after this (see the end of the calendar)."]
    for n, (monday, xs) in enumerate(sorted(weeks.items())):
        rng = f"{xs[0]['when'].strftime('%a %-d %b')} – {xs[-1]['when'].strftime('%a %-d %b')}"
        blocks.append((f"Daily · week of {monday.strftime('%-d %b')}", rng, notes[min(n, len(notes) - 1)], xs, "daily"))
    out, i = [], 0
    for title, dates, desc, posts, phase in blocks:
        cards = []
        for x in posts:
            i += 1
            cards.append(post_card(i, x))
        out.append(f'<section class="week {phase}"><div class="whead"><h3>{E(title)}</h3><span class="dates">{E(dates)}</span></div><p class="muted">{E(desc)}</p>{"".join(cards)}</section>')
    return "".join(out)

def calendar_table():
    rows = []
    for i, x in enumerate(P, 1):
        rows.append((x["when"], x["time"], f'<tr><td class="n">{i:02d}</td><td>{x["when"].strftime("%a %-d %b")}</td><td class="n">{x["time"]}</td><td><span class="fmt {x["fmt"].lower()}">{E(x["fmt"])}</span></td><td><a href="#post-{i}">{E(x["title"])}</a></td></tr>'))
    for s in STORIES:
        rows.append((s[0], "18:00", f'<tr><td class="n">S</td><td>{s[0].strftime("%a %-d %b")}</td><td class="n">18:00</td><td><span class="fmt story">Story</span></td><td><a href="#stories">{E(s[2])}</a></td></tr>'))
    rows.sort(key=lambda r: (r[0], r[1]))
    return "".join(r[2] for r in rows)

def stories_block():
    cards = []
    for s in STORIES:
        cards.append(f'<div class="scard">{media(s[3][0], "tall")}<div><b>{E(s[2])}</b><p class="muted">{s[0].strftime("%a %-d %b")} · 18:00</p><p>{E(s[5])}</p>{filelink(s[3][0])}</div></div>')
    return "".join(cards)

def highlights_block():
    out = []
    for name, fs in HIGHLIGHTS:
        out.append(f'<div class="hl"><b>{E(name)}</b><ul>{"".join(f"<li>{filelink(f)}</li>" for f in fs)}</ul></div>')
    return "".join(out)

def counts():
    feed = sum(1 for x in P if x["fmt"] == "Feed"); car = sum(1 for x in P if x["fmt"] == "Carousel"); reel = sum(1 for x in P if x["fmt"] == "Reel")
    files = set(f for x in P for f in x["files"]) | set(f for s in STORIES for f in s[3])
    return len(P), feed, car, reel, len(files)

def write_html():
    total, feed, car, reel, nfiles = counts()
    npop = sum(1 for x in P if x["phase"] == "populate"); nday = total - npop
    last = P[-1]["when"].strftime("%a %-d %b")
    tpl = open(os.path.join(ROOT, "social", "plan.template.html")).read()
    out = (tpl.replace("{{GRID}}", grid_preview()).replace("{{WEEKS}}", week_blocks())
              .replace("{{CAL}}", calendar_table()).replace("{{STORIES}}", stories_block())
              .replace("{{HIGHLIGHTS}}", highlights_block())
              .replace("{{TOTAL}}", str(total)).replace("{{FEED}}", str(feed)).replace("{{CAR}}", str(car))
              .replace("{{REEL}}", str(reel)).replace("{{NFILES}}", str(nfiles)).replace("{{NSTORY}}", str(len(STORIES)))
              .replace("{{NPOP}}", str(npop)).replace("{{NDAY}}", str(nday)).replace("{{LAST}}", last))
    open(os.path.join(ROOT, "social-plan.html"), "w").write(out)

def used_files():
    fs = set(f for x in P for f in x["files"]) | set(f for s in STORIES for f in s[3]) | set(f for _, l in HIGHLIGHTS for f in l)
    for x in P:
        sv = story_version(x["files"][0])
        if sv: fs.add(sv)
        for f in x["files"]:
            if f.endswith(".mp4"): fs.add(cover(f[:-9]))
    fs |= {"social/profile/calafly-logo-square-1200-ink.png", "social/profile/calafly-logo-square-1200-white.png",
           "social/covers/CALAFLY_DUBAI_B1_SORTED-BEFORE-YOU-FLY_30s_16x9.jpg", "v3-brand/videos/CALAFLY_DUBAI_B1_SORTED-BEFORE-YOU-FLY_30s_16x9.mp4",
           "social/posting_schedule.csv"}
    return sorted(fs)

if __name__ == "__main__":
    import sys
    check()
    write_csv()
    write_html()
    if "--files" in sys.argv:
        print("\n".join(used_files()))
    else:
        print(f"{len(P)} posts, {len(STORIES)} story-only, {counts()[4]} files. Wrote social-plan.html and social/posting_schedule.csv")

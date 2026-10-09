"""Builds the CalaFly Merchant Center supplemental feed (overrides titles, descriptions, images, categories,
highlights and bid labels on the products already in Merchant Center) plus a new-product file for Dubai.

Prices and landing-page links are NOT overridden: they must keep matching calafly.net exactly.
Repeated headers (additional_image_link, product_highlight, product_detail) are how Merchant Center
accepts multiple values in a CSV/Sheets source.
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
BRANCH = "claude/claude-cloud-status-glwjyq"
IMG = f"https://raw.githubusercontent.com/vstrategy101-sudo/TNT/refs/heads/{BRANCH}/clients/calafly/merchant-center/images"
CATEGORY = "Electronics > Communications > Telephony > Mobile Phone Accessories > Mobile Phone Pre-Paid Cards & SIM Cards"

# id = the Product ID shown in Merchant Center (screenshot, 9 Oct 2026)
PRODUCTS = [
    # id,          key,       destination,  region,          priority,        price_band, data
    ("G-62589218", "turkey",   "Turkey",    "Europe",        "uk_core",       "low",  None),
    ("G-62589214", "usa",      "USA",       "North America", "uk_core",       "low",  None),
    ("G-62589216", "spain",    "Spain",     "Europe",        "uk_secondary",  "mid",  None),
    ("G-62589215", "france",   "France",    "Europe",        "uk_secondary",  "low",  None),
    ("G-62589213", "italy",    "Italy",     "Europe",        "uk_secondary",  "mid",  None),
    ("G-62589212", "japan",    "Japan",     "Asia",          "long_haul",     "low",  None),
    ("G-62589217", "thailand", "Thailand",  "Asia",          "long_haul",     "low",  None),
    ("G-62589209", "world500", "Global",    "Global",        "global",        "mid",  "500 MB"),
    ("G-62589210", "world1",   "Global",    "Global",        "global",        "mid",  "1 GB"),
    ("G-62589211", "world3",   "Global",    "Global",        "global",        "high", "3 GB"),
]

def title(dest, data):
    if dest == "Global":
        return f"Global eSIM {data} – Travel Data in 200+ Countries | QR Code by Email | CalaFly"
    return f"{dest} eSIM – Travel Mobile Data for {dest} | Install Before You Fly | CalaFly"

def description(dest, data):
    where = "in 200+ countries" if dest == "Global" else f"in {'the USA' if dest == 'USA' else dest}"
    plan = f"{data} of data" if data else "mobile data"
    return (f"CalaFly {dest} eSIM gives you {plan} on your phone while you travel {where}. "
            "Buy online and your eSIM QR code arrives by email. Scan it at home, install it before you fly, "
            "and switch it on when you land. It's a data-only eSIM, so your main SIM, phone number and WhatsApp "
            "stay the same. You pay once for the plan, with no daily roaming charges from us. If you never install "
            "your eSIM you can get a refund (terms apply, see calafly.net). Requires an unlocked, eSIM-compatible phone.")

def highlights(dest):
    where = "200+ countries" if dest == "Global" else ("the USA" if dest == "USA" else dest)
    return [f"Mobile data for {where} on your existing phone",
            "QR code delivered by email, install at home in minutes",
            "Data-only eSIM: your number and WhatsApp stay the same",
            "Pay once for the plan, no daily roaming charges from us",
            "Refund if your eSIM is not installed (terms apply)",
            "Works with unlocked, eSIM-compatible phones"]

def details(dest, data):
    d = [f"eSIM:Type:Data-only eSIM", "eSIM:Delivery:QR code by email",
         f"eSIM:Coverage:{'200+ countries' if dest == 'Global' else dest}",
         "Compatibility:Phone:Unlocked, eSIM-compatible"]
    if data: d.insert(1, f"eSIM:Data:{data}")
    return d

header = (["id", "title", "description", "image_link"] + ["additional_image_link"] * 2 + ["lifestyle_image_link",
          "google_product_category", "product_type", "brand", "identifier_exists", "condition"]
          + ["product_highlight"] * 6 + ["product_detail"] * 5 + ["custom_label_0", "custom_label_1", "custom_label_2"])

def row(pid, key, dest, region, prio, band, data):
    det = details(dest, data); det += [""] * (5 - len(det))
    return ([pid, title(dest, data), description(dest, data), f"{IMG}/calafly-{key}-esim-main.jpg",
             f"{IMG}/calafly-{key}-esim-arrive.jpg", f"{IMG}/calafly-{key}-esim-home.jpg", f"{IMG}/calafly-{key}-esim-arrive.jpg",
             CATEGORY, (f"eSIM > Global > {data}" if data else f"eSIM > {region} > {dest}"), "CalaFly", "no", "new"]
            + highlights(dest) + det + [prio, region.lower().replace(" ", "_"), band])

problems = []
for p in PRODUCTS:
    t = title(p[2], p[6])
    if len(t) > 150: problems.append(f"title too long: {t}")
    for h in highlights(p[2]):
        if len(h) > 150: problems.append(f"highlight too long: {h}")

with open(os.path.join(HERE, "feed", "calafly_supplemental_feed.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(header)
    for p in PRODUCTS: w.writerow(row(*p))

# Dubai is the second-biggest UK market in the plan and is missing from Merchant Center.
# Price and link must be filled from calafly.net before upload.
new_header = ["id", "title", "description", "link", "price", "availability"] + header[3:]
with open(os.path.join(HERE, "feed", "calafly_new_product_dubai.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(new_header)
    r = row("CALAFLY-DUBAI", "dubai", "Dubai", "Middle East", "uk_core", "low", None)
    w.writerow(r[:3] + ["FILL: calafly.net Dubai plan URL", "FILL: price exactly as on site, e.g. 5.00 GBP", "in_stock"] + r[3:])

print("problems:", problems or "none")
print("rows:", len(PRODUCTS), "+ Dubai")

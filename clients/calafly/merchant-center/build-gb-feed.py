"""Primary product file for UK Shopping (feed label GB, prices in GBP).

The products created by hand in Merchant Center carry the India feed label (IN), so UK Shopping campaigns can't use
them. This file is uploaded as a new product source with country of sale United Kingdom and feed label GB.
Prices and links must match the landing pages exactly (hero plans, 9 Oct 2026).
Run: python3 build-gb-feed.py
"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "https://raw.githubusercontent.com/vstrategy101-sudo/TNT/refs/heads/claude/claude-cloud-status-glwjyq/clients/calafly/merchant-center/images"
CAT = "Electronics > Communications > Telephony > Mobile Phone Accessories > Mobile Phone Pre-Paid Cards & SIM Cards"
PLANS = [  # id, key, destination, data, days, price GBP, url
    ("CF-GB-USA-3GB-30D",     "usa",    "USA",    "3GB",  30, 7.00,  "https://calafly.net/usa"),
    ("CF-GB-TURKEY-10GB-7D",  "turkey", "Turkey", "10GB", 7,  11.00, "https://calafly.net/turkey"),
    ("CF-GB-DUBAI-10GB-7D",   "dubai",  "Dubai",  "10GB", 7,  18.00, "https://calafly.net/dubai"),
]
H = ["id", "title", "description", "link", "image_link", "additional_image_link", "additional_image_link",
     "price", "availability", "condition", "brand", "identifier_exists", "google_product_category", "product_type",
     "shipping", "product_highlight", "product_highlight", "product_highlight", "product_highlight",
     "custom_label_0", "custom_label_1"]
rows = []
for pid, key, dest, data, days, price, url in PLANS:
    where = "the USA" if dest == "USA" else dest
    title = f"{dest} eSIM {data} {days} Days – Travel Mobile Data for {where} | QR Code by Email | CalaFly"
    desc = (f"CalaFly {dest} eSIM with {data} of mobile data for {days} days while you travel in {where}. "
            "Buy online and your eSIM QR code arrives by email. Scan it at home, install it before you fly, and switch it on "
            "when you land. It's a data-only eSIM, so your main SIM, phone number and WhatsApp stay the same. You pay once "
            "for the plan, with no daily roaming charges from us. 100% refund if your eSIM is unused (terms apply, see "
            "calafly.net/legal/terms). Requires an unlocked eSIM-compatible phone.")
    assert len(title) <= 150, title
    rows.append([pid, title, desc, url, f"{IMG}/calafly-{key}-esim-main.jpg", f"{IMG}/calafly-{key}-esim-arrive.jpg",
                 f"{IMG}/calafly-{key}-esim-home.jpg", f"{price:.2f} GBP", "in_stock", "new", "CalaFly", "no", CAT,
                 f"eSIM > {dest} > {data} {days} days", "GB:::0.00 GBP",
                 f"{data} of mobile data for {days} days in {where}", "QR code by email: install at home in minutes",
                 "Data-only eSIM: your number and WhatsApp stay the same", "100% refund if unused (terms apply)",
                 "uk_core", key])
out = os.path.join(HERE, "feed", "calafly_primary_feed_GB.csv")
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(H); w.writerows(rows)
print("wrote", out, len(rows), "products")

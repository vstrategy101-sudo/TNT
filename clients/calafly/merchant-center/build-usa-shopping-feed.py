"""USA-only Shopping feed (UK sale, feed label GB, GBP), with every attribute that helps the product win Shopping auctions.

Landing page: https://calafly.net/destinations/esim-usa. The price must match what that page shows a UK visitor.
Run: python3 build-usa-shopping-feed.py
"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "https://raw.githubusercontent.com/vstrategy101-sudo/TNT/refs/heads/claude/claude-cloud-status-glwjyq/clients/calafly/merchant-center/images"
row = {
    "id": "CF-GB-USA-3GB-15D",
    # searched words first: "usa esim", then the plan, then what makes it different
    "title": "USA eSIM 3GB 15 Days – Travel Data eSIM for the USA, Instant QR Code by Email | CalaFly",
    "description": ("USA eSIM with 3GB of mobile data for 15 days, for travel anywhere in the USA. Buy online and your eSIM QR "
                    "code arrives by email in minutes. Scan it at home, install it before you fly and switch it on when you "
                    "land in New York, Orlando, Las Vegas or anywhere in the USA. It's a data-only eSIM, so your main SIM, "
                    "phone number and WhatsApp stay the same. Pay once for the plan, with no daily roaming charges from us. "
                    "100% refund if your eSIM is unused (terms apply: calafly.net/legal/terms). Works with unlocked "
                    "eSIM-compatible iPhone, Samsung Galaxy and Google Pixel phones."),
    "link": "https://calafly.net/destinations/esim-usa",
    "image_link": f"{IMG}/calafly-usa-esim-main.jpg",
    "additional_image_link": [f"{IMG}/calafly-usa-esim-arrive.jpg", f"{IMG}/calafly-usa-esim-home.jpg"],
    "lifestyle_image_link": f"{IMG}/calafly-usa-esim-arrive.jpg",
    "price": "7.00 GBP",
    "availability": "in_stock",
    "condition": "new",
    "brand": "CalaFly",
    "identifier_exists": "no",
    "google_product_category": "Electronics > Communications > Telephony > Mobile Phone Accessories > Mobile Phone Pre-Paid Cards & SIM Cards",
    "product_type": "eSIM > USA > 3GB 15 days",
    "shipping": "GB:::0.00 GBP",
    "is_bundle": "no",
    "product_highlight": ["3GB of mobile data for 15 days anywhere in the USA",
                          "QR code by email: install at home in minutes",
                          "Data-only eSIM: your number and WhatsApp stay the same",
                          "Pay once with no daily roaming charges from us",
                          "100% refund if your eSIM is unused (terms apply)",
                          "Works with unlocked eSIM-compatible phones"],
    "product_detail": ["eSIM:Data:3GB", "eSIM:Validity:15 days", "eSIM:Coverage:USA",
                       "eSIM:Delivery:QR code by email", "Compatibility:Phone:Unlocked eSIM-compatible phone"],
    "custom_label_0": "uk_core", "custom_label_1": "usa", "custom_label_2": "hero_plan",
}
header, values = [], []
for k, v in row.items():
    for x in (v if isinstance(v, list) else [v]):
        assert "," not in x or k in ("description", "title"), (k, x)   # commas split repeated fields
        header.append(k); values.append(x)
assert len(row["title"]) <= 150
out = os.path.join(HERE, "feed", "calafly_usa_shopping_feed_GB.csv")
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(header); w.writerow(values)
print("wrote", out, len(row["title"]), "char title")

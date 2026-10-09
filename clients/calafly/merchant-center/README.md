# CalaFly · Google Merchant Center kit

Account: **Calafly · 5858054381**. Built from the catalogue as it stood on 9 Oct 2026: 10 products, Turkey not approved, Dubai missing.

## What's in this folder

| Folder | Contents |
|---|---|
| `images/` | 33 product images at 1500×1500 JPG. For each of the 10 products plus Dubai: `-main` (product on a clean light background), `-arrive` (lifestyle: plane window, phone showing the CalaFly line), `-home` (lifestyle: boarding pass and the install screen). None carry promotional text, badges, borders or watermarks, as Google's image rules require. |
| `logos/` | Square 1200×1200, wide 4:1 (1200×300) and wide 2:1 (1200×600) logos, each on white and on ink |
| `feed/calafly_supplemental_feed.csv` | New titles, descriptions, images, category, product type, brand, highlights, details and custom labels for all 10 products, matched by Product ID |
| `feed/calafly_new_product_dubai.csv` | A complete Dubai listing. Fill in the price and URL from calafly.net before uploading. |
| `build-feed.py` | Regenerates the feed. Edit a line and run `python3 build-feed.py`. |

Image links in the feed point to this GitHub repo so Google can fetch them straight away. Once the client's site can host them, move them to `calafly.net/images/…` and change `IMG` in `build-feed.py`.

---

## Fix first (these block or hurt every auction)

1. **Mixed currencies.** Turkey is priced at **£5.00**; every other product is in **US dollars** ($4–$22). For UK shoppers Google wants prices in **GBP that match what calafly.net shows a UK visitor**. Dollar prices either get disapproved or shown converted, which hurts click-through. Set every price in GBP, exactly as on the site.
2. **Turkey shows "Not approved".** Open the product and read the issue. The most likely cause is the £/$ mismatch above, or the price not matching the landing page. Turkey is our biggest UK market, so this comes first.
3. **Dubai is missing.** It's 40% of the planned UK budget from October to March. Upload `calafly_new_product_dubai.csv` once the price and link are filled in.

## Step-by-step (menus as in your Merchant Center)

**Settings → Business info**
- Business name: CalaFly. Website: calafly.net. Verify and claim the site. Since the GTM container is on the site, choose **Google Tag Manager** verification; no developer is needed.
- Logos: upload `logos/calafly-logo-square-1200-white.png` (square) and `calafly-logo-wide-4x1-1200x300-white.png` (rectangular).
- Add a customer service email and the contact page URL. Store Quality checks these.

**Products & store → Shipping and returns**
- *Shipping:* create a UK service called "Email delivery". Cost **£0**, handling **0 days**, transit **0 days**, applying to all products. This shows as **Free delivery** and scores top for speed and cost.
- *Returns:* create a UK policy that matches the refund-if-not-installed terms exactly:
  - Return window: the real number of days. Longer scores better, but it must match the T&Cs.
  - Return fees: free. Return method: online or by email.
  - Return policy URL: the calafly.net refund or terms page.

**Settings → Data sources → Add supplemental source**
- Upload `feed/calafly_supplemental_feed.csv`, or paste it into a Google Sheet and add it as a Sheets source so we can edit it live.
- Link it to the primary source (the products you created manually). It matches on `id`, the G-625892xx Product ID. If Merchant Center says the IDs don't match, open one product, copy its exact ID, and tell me.
- Prices and links are deliberately not overridden. They stay as on the site.

**Settings → Add-ons → Google Customer Reviews**
- Opt in and add the survey opt-in code to the order confirmation page, via GTM on the CHECKOUT_SUCCESS step.
- This is what produces the star rating, and reviews are the slowest part of the Top Quality Store badge to build.

**Products & store → Store quality**
- Check it weekly. The aim is "Exceptional" overall. Changes can take up to 30 days to show.

**Settings → Access and services**
- Link the client's Google Ads account, so Shopping campaigns can use these products and conversions flow both ways.

**Marketing → Promotions** (optional, high impact)
- Run a real promotion, for example "10% off your first eSIM". It earns a "Special offer" label on Shopping listings, which lifts click-through. Only run offers that actually exist at checkout.

**Analytics → Price benchmarks** (after about 2 weeks of data)
- Compare each product's price with the market benchmark. At $4–$6 CalaFly is likely already among the cheapest, so this is a strength to show in the GBP prices.

---

## What the feed changes and why it wins auctions

| Field | Before | After | Why it matters |
|---|---|---|---|
| Title | "Turkey eSIM Plan" | "Turkey eSIM – Travel Mobile Data for Turkey \| Install Before You Fly \| CalaFly" | Matches what people search ("turkey esim", "mobile data turkey"). Titles are the strongest relevance signal in Shopping. |
| Description | – | Factual, about 600 characters: delivery, install, data-only, pay once, refund, compatibility | Relevance and policy clarity |
| Images | Stock city photos | Product main image plus 2 lifestyle images | Product-first images are favoured and avoid "image doesn't show product" problems. Lifestyle images show on browsing surfaces. |
| Category | – | Mobile Phone Pre-Paid Cards & SIM Cards | Correct category, so the right auctions |
| Product type | – | eSIM > Region > Destination | Lets campaigns be organised by region |
| Highlights and details | – | 6 highlights, 4–5 details | Fills the expanded product view and adds trust |
| Custom labels | – | `uk_core` (Turkey, USA, Dubai), `uk_secondary` (Spain, France, Italy), `long_haul`, `global`; region; price band | Bid harder on what UK travellers search for most |

**Shopping campaign setup in Google Ads** (once linked):
- **Campaign:** one Standard Shopping campaign for the UK.
- **Product groups:** split by `custom_label_0`. Bid highest on `uk_core`, lower on `uk_secondary`, lowest on `long_haul` and `global`.
- **Bidding:** start on manual CPC. Move to Maximise conversion value once there are about 30 purchases.
- **Negatives:** apply the shared negative keyword list from the Search plan.

**Check the CPC against the basket size.** Plans are around $4–$6, so a click costing 30p eats much of the margin. Watch cost per purchase closely, and push the global and bigger plans, where the basket is larger.

## Claims used (same sign-off as the ads)
The feed and images use only these claims:
- QR code by email; install at home
- Data-only, so your number and WhatsApp stay the same
- Pay once, no daily charges from us
- Refund if not installed (terms apply)
- Unlocked, eSIM-compatible phone needed
- 200+ countries for the global plans (from Gladstone's 29 Sept email)

The screens on the phones are CalaFly-style mock-ups. Swap in real screenshots when available.

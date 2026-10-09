# CalaFly · Google Search build (UK → USA, Turkey, Dubai)

One Search campaign covers all three destinations. A small brand campaign sits beside it. The whole build is in `editor/` as Google Ads Editor import files: 13 ad groups, 200 keywords, 13 RSAs, negatives, sitelinks, callouts, snippets and image assets. Every line has been checked against Google's character limits.

Rebuild after any copy change: `python3 build-search.py`

---

## 1. Account setup (once, before any campaign)

| Setting | Value | Why |
|---|---|---|
| Account creation | Use **Expert mode**: "Switch to Expert Mode", then "Create an account without a campaign" | Stops Google creating a Smart or PMax campaign |
| Currency | **GBP** | Can't be changed later. Must match Merchant Center. |
| Time zone | **(GMT+00:00) London** | Can't be changed later |
| Billing | Client's card or invoice, under the Cala Travel business name | |
| Advertiser verification | Complete as soon as Google asks, with company documents | Ads stop if it isn't done in time |
| Auto-tagging | **On** (Admin → Account settings) | Needed for GA4 and conversion matching |
| Auto-apply recommendations | **Everything off** (Recommendations → Auto-apply) | Google otherwise adds broad match, new keywords and new ad copy without sign-off. Some of that would breach our CAP-checked claims. |
| Tracking template | Leave empty. Each campaign uses a final URL suffix with UTMs. | |
| Linked accounts | **GA4** (import conversions and audiences), **Merchant Center 5858054381** (Shopping later), **Google Tag Manager** | |
| Customer data terms | Accept (Tools → Conversions → Settings) | Required for Enhanced Conversions |
| Account-level negatives | Attach shared list **CF_UK_NEGATIVES** to both campaigns | |
| Content suitability | Exclude sensitive content and parked domains | Search partners are off anyway |

### Conversion tracking (week 0, blocks launch)
Set these up with GTM. The site already has a container, and calafly.net fires these steps as custom events: INITIATE_JOURNEY, CHECKOUT and CHECKOUT_SUCCESS.

| Conversion action | Fires on | Goal | Value | Count |
|---|---|---|---|---|
| **CF Purchase** | CHECKOUT_SUCCESS (order confirmation) | **Primary**, the only one bidding uses | Real order value in GBP plus transaction_id | One |
| CF Begin checkout | CHECKOUT | Secondary (observation only) | none | One |
| CF Start journey | INITIATE_JOURNEY | Secondary | none | One |
| CF Account created | ACCOUNT_CREATED | Secondary | none | One |

- **Enhanced Conversions:** turn on for CF Purchase. Pass the hashed email from the checkout via GTM's user-provided data variable.
- **Consent Mode v2:** set up in Advanced mode with a UK-compliant cookie banner. Without it, UK conversions go unrecorded and audiences can't be built (UK GDPR / PECR).
- **Attribution:** data-driven, 30-day click window, 1-day engaged-view window.
- **QA before launch:** run a real test purchase, then check CF Purchase in Tag Assistant and in Conversions → Diagnostics. Refund the test order afterwards.

---

## 2. Campaign settings: `CF_UK_SEARCH_DESTINATIONS`

| Setting | Value |
|---|---|
| Objective | Sales, with goal **CF Purchase only**. Use campaign-specific goals and remove the account defaults. |
| Type | Search |
| Networks | **Google Search only.** Search Partners off, Display Network off. |
| Locations | **United Kingdom**. Targeting method: **Presence**, "people in or regularly in". Do not use "interest", which would show ads to people abroad. |
| Languages | English |
| Audience segments | **Observation** only, so bidding isn't limited. Add: in-market *Travel → Air Travel*, *Trips to North America*, *Trips to Middle East*, *Trips to Europe*; affinity *Travel Buffs*; your data *all visitors 30d*, *purchasers 180d*. |
| AI Max for Search | **Off at launch.** It expands to broad-style queries and rewrites ad text and URLs. Test it in month 2. |
| Automatically created assets | **Off** (text and final URL expansion). Every claim must stay in the approved wording. |
| Broad match | Not used. Phrase + exact only, with the 200 keywords in the file. |
| Ad schedule | All day, every day. Add hour-by-day blocks for reporting only. Don't adjust bids yet. |
| Devices | All. No adjustments (Smart Bidding handles device). |
| Ad rotation | Optimise |
| Final URL suffix | `utm_source=google&utm_medium=cpc&utm_campaign=cf_uk_search_destinations&utm_content={adgroupid}&utm_term={keyword}` (already in file 01) |
| Start | Status **Paused** in the import. Enable after tracking QA passes. |

### Bidding: staged, because the basket is small
Plans sell for about £3–£18, so a 70p click can wipe out a sale. Bidding goes in three stages:

| Stage | When | Strategy |
|---|---|---|
| 1 · Learn | Days 1–14, or until about 15 purchases | **Maximise clicks with a £0.60 max CPC cap.** Buys clean data at a controlled price. Purchases are still tracked. |
| 2 · Convert | After 15 purchases | **Maximise conversions**, no target |
| 3 · Efficiency | After 30 purchases in 30 days | **Target CPA** at the actual 14-day CPA, then lower it by 10% every 2 weeks. When value tracking is reliable, switch to **Maximise conversion value with target ROAS** (start at the actual ROAS). |

Never change budget or bidding by more than 20% at once, or more than once every 3–4 days.

### Budget: £1,000 a month to start
The Google Search budget is **£1,000 for the month**, about £33 a day. Google can spend up to 2× the daily budget on a single day but never more than 30.4× it in a month.

| Campaign | Daily budget | Month |
|---|---|---|
| CF_UK_SEARCH_DESTINATIONS | **£30.00** | ~£912 |
| CF_UK_SEARCH_BRAND | **£3.00** | ~£91 (usually underspends) |

Target country split of the £30: Dubai about £12, USA about £10.50, Turkey about £7.50 a day.

**What £1,000 buys.** At the £0.60 cap, that's roughly 1,500+ clicks a month, or about 50 a day across three countries. That's enough to learn which country and intent converts, but not enough to cover every search. Expect "Limited by budget" on the campaign; that's fine at this stage.

**Rules for a small budget:**
- Keep the £0.60 cap for the first 2 weeks. Don't remove it just because impression share is low.
- If an ad group reaches about £40 spent with no purchase while others are converting, pause it. Cities is the likeliest one.
- Scale only once cost per purchase is known. Then add +20% every 3–4 days (for example £30 → £36 → £43) to campaigns under target.

**Country weighting in one campaign.** A single campaign budget can't be split by country, so the 40/35/25 plan (Dubai/USA/Turkey) is steered through ad groups:
- Check spend by country every Thursday. Segment by ad group and filter by the "DUBAI |", "USA |" or "TURKEY |" prefix.
- If one country takes more than 15 points over its share without the purchases to justify it, pause its weakest ad group, which is usually Roaming.
- If that happens two weeks in a row, move that country into its own campaign. It's a 10-minute copy-and-paste in Editor.

---

## 3. Ad groups (12 + brand)

Each country has four ad groups by search intent, all sending traffic to that country's landing page:

| Ad group | Example keywords | Path | First headlines |
|---|---|---|---|
| `{COUNTRY} \| eSIM` | turkey esim, esim for dubai, us esim | /turkey/esim | {Country} eSIM by CalaFly · Get Your {Country} eSIM |
| `{COUNTRY} \| Data SIM` | dubai tourist sim, sim card for usa from uk | /dubai/data | Mobile Data for {Country} · No SIM Card to Collect |
| `{COUNTRY} \| Roaming` | roaming in turkey, ee roaming dubai, vodafone roaming usa | /usa/roaming | Using Your Phone in {Country}? · Holiday Data for {Country} |
| `{COUNTRY} \| Cities` | antalya esim, new york esim, abu dhabi esim | /turkey/cities | eSIM for Antalya · eSIM for Istanbul |
| `Brand` (own campaign) | calafly, cala fly, calafly esim | /esim/official | CalaFly Official Site |

- **Roaming** is the highest-value group. Turkey, the USA and the UAE are all outside UK networks' Europe roaming zones, so these searchers face a daily charge. The ad copy never names a network or makes a comparison: "No daily charges from us" and "Pay once, not per day" are claims about CalaFly only.
- **Brand** has its own campaign because Google reads "calafly" as a misspelling of a bigger competitor. Brand terms are added as negatives in the destinations campaign so the two campaigns don't compete with each other.

## 4. Ads (1 RSA per ad group, ready to add a second in week 3)
- 15 headlines and 4 descriptions per ad group. The first 3–4 headlines change by intent and country; the rest carry the USPs.
- **Compliance pin:** both refund descriptions ("…Refund if your eSIM is never installed. T&Cs apply.") are pinned to **Description position 2**. Every ad that can show "Refund if Not Installed" then also shows the T&Cs line (CAP 3.9–3.10). Nothing else is pinned, so Ad Strength stays at Good or above.
- No dynamic keyword insertion, because it would print searcher words like "best" or "cheapest" into the ad.
- No price in the ads until GBP prices on calafly.net and in Merchant Center match.

## 5. Assets
| Asset | Level | Content |
|---|---|---|
| Sitelinks (8) | Campaign | How It Works · Refund Policy · Compatible Phones · Help and FAQs · USA eSIM · Turkey eSIM · Dubai eSIM · Global eSIM |
| Callouts (8) | Campaign | Set Up in Minutes · Pay Once, Not Per Day · Refund if Not Installed · QR Code by Email · Data-Only eSIM · Keep Your WhatsApp Number · Install Before You Fly · No Daily Charges From Us |
| Structured snippet | Campaign | Destinations: USA, Turkey, Dubai, Spain, France, Italy, Japan, Thailand |
| Images (4 per ad group) | Ad group | `images/` has a 1:1 and a 1.91:1 of the arrival and install-at-home scenes per country. They have no overlaid text, which Google Search image rules require. |
| Business name + logo | Account | "CalaFly" plus `merchant-center/logos/calafly-logo-square-1200-white.png` |
| Price assets | Campaign | **Add when GBP prices are confirmed:** USA / Turkey / Dubai / Global, "From £X", linking to each country page |
| Promotion | Campaign | Only if a real code works at checkout, e.g. 10% off a first eSIM |

**Check before upload:** the sitelink URLs (/how-it-works, /refund-policy, /compatible-devices, /faq, /global) and the country pages (/usa, /turkey, /dubai) are assumed. Open each one on calafly.net and correct `SITELINKS` or `COUNTRIES` in `build-search.py` if a path differs. Ads pointing to a 404 get disapproved.

## 6. Negatives
- **Shared list `CF_UK_NEGATIVES`** (60 terms, phrase match, on both campaigns). It blocks:
  - jobs, logins and support searches ("not working", "transfer esim")
  - contract, SIM-only and broadband searches
  - pocket wifi
  - inbound-tourist searches ("esim for uk")
  - other EU destinations
  - flights, hotels and visas
  - competitor brand names, so the account doesn't pay for other brands' searches at launch. Test removing these in month 2 if non-brand volume runs out.
- **Campaign negatives** on the destinations campaign: calafly, cala fly, cala esim.
- **Search terms review:** every Monday and Thursday for the first 4 weeks, then weekly. Add anything irrelevant to the shared list.

## 7. Importing with Google Ads Editor (about 15 minutes)
1. Download Google Ads Editor, sign in, and download the CalaFly account.
2. Shared library → Negative keyword lists → add `CF_UK_NEGATIVES`, then paste file **06**.
3. Go to Account → **Import → From file**, and import in order: **01 → 02 → 03 → 04 → 05 → 07 → 08 → 09**. Review the changes each time and accept.
4. Upload the images from `images/` to each ad group (file **10** lists which go where).
5. Set the campaign goal (CF Purchase only), audiences (observation), and turn AI Max and auto-assets off. These settings aren't in the import.
6. Fill in each campaign's daily budget, then **Post**. Both campaigns arrive **Paused**.
7. Enable once conversion QA has passed.

## 8. First 8 weeks
| Week | Actions |
|---|---|
| 0 | Account settings, conversions and Consent Mode QA, sitelink URL checks, import, then enable |
| 1–2 | Leave bids alone. Search terms twice a week. Check impression share for "turkey esim", "dubai esim" and "usa esim" exact. |
| 2 | Move to Maximise conversions once there are about 15 purchases. Shift weight between countries if CPA differs by more than 30%. |
| 3–4 | Add RSA #2 per ad group, built from the best headlines in the asset report. Pause keywords that spent 2× target CPA with no purchase. Add a price asset if prices are fixed. |
| 5–8 | Move to target CPA. Scale budget +20% every 3–4 days while under target. Test AI Max in one country. Launch Standard Shopping from the Merchant Center feed. |

**KPIs:** cost per purchase (primary), ROAS, conversion rate by ad group, search impression share on core exact terms (target above 60%), CTR (target above 8% non-brand, above 25% brand), install rate and refund rate (from CalaFly).

# CalaFly UK launch: USA, Turkey and Dubai (October 2026)

Prospecting and retargeting on Google (70% of spend) and Meta (30%) for people travelling from the UK to the USA, Turkey and Dubai. Each destination has its own landing page with the same structure.

## What's in this folder

| Folder | Contents |
|---|---|
| `creatives/<country>/` | 6 concepts per country × 4 sizes: 1:1 (1080×1080), 4:5 (1080×1350), 9:16 (1080×1920), 1.91:1 (1200×628). 72 PNGs in total. |
| `videos/` | 2 × 15s videos, each in 9:16 and 16:9 (H.264, 30fps, silent AAC track) |
| `copy/` | Google RSA copy, Google keywords and negatives, Meta primary text, headlines and descriptions. Every line is checked against platform character limits. |
| `src/` | HTML templates and render scripts. Edit a line and re-render everything in about a minute. |

Re-render: `cd src && node render-creatives.mjs && node render-videos.mjs && python3 build-copy.py`

## Round 2 (realistic set)

See `v2-realistic/README.md`: competitor scan, 60 realistic statics (phone mock-ups, iOS-style screens, rendered scenes), 12 videos with synthesised sound design, and audio stems.

## Message architecture

An intro to CalaFly, followed by three USPs. Every ad is about CalaFly's own product. There are no competitor names and no comparative claims.

| # | Concept | Headline | Role |
|---|---|---|---|
| 01 | Intro | Meet CalaFly. Mobile data for {country}, sorted before you leave the UK. | Prospecting, cold |
| 02 | Easy setup | Set up in minutes. From the sofa. (Pick, Scan, Land connected) | Prospecting |
| 03 | Pay once | Pay once. Not per day. One price for your whole trip. | Prospecting |
| 04 | Refund | Plans changed? Get a refund (if you never install it). | Prospecting + retargeting |
| 05 | All USPs | {Country} data, sorted. (3 ticks) | Prospecting workhorse, Google image assets |
| 06 | Retarget | Still planning {country}? Your data can be sorted tonight. | Retargeting only |
| V1 | Video: Meet CalaFly | Hook, then brand, then 3 USPs, then CTA (15s) | Prospecting (Meta, YouTube, Demand Gen) |
| V2 | Video: How it works | Pick, Scan, Land connected, then one price + refund (15s) | Retargeting + mid-funnel |

## Budget split (share of total spend)

| Channel | Campaign | Share | Per £1,000 |
|---|---|---|---|
| Google | Search, non-brand (3 campaigns, one per country) | 49% | £490 |
| Google | Search, brand + misspellings | 4% | £40 |
| Google | Demand Gen prospecting (video + image) | 10% | £100 |
| Google | Demand Gen remarketing | 7% | £70 |
| Meta | Prospecting (Sales, Advantage+ audience) | 22% | £220 |
| Meta | Retargeting (site visitors, video viewers, engagers) | 8% | £80 |

**Country split to start (Oct–Mar): Dubai 40%, USA 35%, Turkey 25%.** Winter is peak season for UK trips to Dubai. USA demand stays steady (New York at Christmas, Florida over half-term). Turkey is mainly a summer destination for UK travellers, so move Turkey up from April. After two weeks, rebalance on cost per purchase.

## Campaign structure

### Google (70%)
- **CF_UK_SEARCH_USA / _TURKEY / _DUBAI.** One campaign per country so each budget can be controlled separately.
  - Ad groups: eSIM, Data/SIM, Roaming intent, Destinations (cities). Phrase and exact match.
  - Location: UK, "presence" targeting.
  - Assets: 1 RSA (15 headlines, 4 descriptions), sitelinks (How it works, Refund policy, Compatible phones, and one per country), callouts (Set up in minutes, Pay once not per day, Refund if not installed, Data-only eSIM, Keep your WhatsApp number), image assets (1:1 + 1.91:1).
  - Bidding: Maximise conversions, then target CPA once a campaign reaches about 30 purchases in 30 days.
- **CF_UK_SEARCH_BRAND.** Covers calafly, cala fly, calafly esim and calafly.net. Needed because Google treats "calafly" as a misspelling of Holafly, a much bigger competitor.
- **CF_UK_DEMANDGEN_PROSPECTING.**
  - Ad groups per country, using custom segments built from search terms (e.g. "flights to dubai", "dubai holiday", "esim dubai") plus in-market travel audiences.
  - Add lookalikes once there are about 1,000 purchasers to seed them.
  - Assets: statics 01–05 + V1 + V2.
- **CF_UK_DEMANDGEN_REMARKETING.** Site visitors in the last 30 days, split by country page. Assets: 06, 04, V2.
- **No Performance Max at launch.** It would take spend from brand and search terms that the Search campaigns already cover. Revisit in month 2 with brand exclusions.

### Meta (30%)
- **CF_UK_META_PROSPECTING.** Sales objective, Purchase event, campaign budget.
  - Ad sets: USA, TURKEY, DUBAI.
  - Audience: UK residents 18+, Advantage+ audience with destination and airline interests as suggestions, Advantage+ placements. Exclude purchasers from the last 180 days.
  - Ads: 01–05 (placement-customised 1:1, 4:5, 9:16) + V1 + V2.
- **CF_UK_META_RETARGETING.** Ad set per country.
  - Audience: visitors to /usa, /turkey or /dubai in the last 30 days, plus 50% video viewers and page engagers. Exclude purchasers.
  - Ads: 06, 04, V2.
  - Keep frequency under 3 per 7 days.

### Tracking (week 0, before any spend)
- Meta: Pixel + Conversions API with deduplication.
- Google: Ads purchase conversion with Enhanced Conversions, GA4, and **Consent Mode v2 with a compliant cookie banner** (required under UK GDPR and PECR).
- Pass purchase value and country on every purchase.
- Add an install event if CalaFly can send it. Refund rate and install rate are the quality metrics for this account.

## Plan by phase

| Phase | Weeks | What happens |
|---|---|---|
| Set-up | 0 | Tracking QA, claim sign-off (see below), LP message match per country, refund T&Cs page live |
| Learn | 1–2 | Everything live. No edits for the first 72 hours. Thursday competitive review starts. |
| Cut | 3–4 | Pause any ad that has spent twice the target cost per purchase with no purchases. Move Search to target CPA. Rebalance countries. |
| Scale | 5–8 | Raise budget 20% every 3–4 days on campaigns under target. Round 2 creative built from what won (price variant, creator video). |

KPIs: cost per purchase (primary), ROAS, landing-page conversion rate, CTR/CPC, 3-second video view rate, install rate, refund rate.

## UK ad compliance

**Built into every creative:**
- **Comparisons:** no competitors named, and no comparative, "cheapest", "best", "unlimited", "5G" or "free" claims. Every claim is about CalaFly only (CAP Code 3.33–3.44).
- **Material information on every ad:** "Data-only eSIM. Requires an unlocked, eSIM-compatible phone." (CAP 3.3)
- **Refund wording:** the refund claim always carries "Refund if your eSIM is not installed. T&Cs apply, see calafly.net." (CAP 3.9–3.10)
- **Setup time:** "Set up in minutes" rather than a specific minute count.
- **Neutral visuals:** no flags, maps, landmarks, or religious or national symbols. Destinations appear only as airport codes. "Turkey" follows UK English usage.
- **No pressure tactics:** no countdowns or false urgency.
- **Retargeting copy** never says "we saw you" or refers to the person's browsing.
- **Legibility:** small print is at least 24px at 1080 width on a high-contrast background.
- **9:16 safe zones:** key copy stays clear of the Reels/Stories UI (top 250px, bottom 600px).

**CalaFly must confirm before launch (blockers):**
1. **"Pay once, not per day":** no plan for these destinations has a daily charge, auto-renewal or automatic top-up.
2. **Refund terms:** what counts as "not installed", the time window and how to claim. All of it must appear on the landing page and at checkout. If there is a short deadline, it goes into the ad small print.
3. **"Set up in minutes":** needs a typical install time to back it up.
4. **WhatsApp line (Google + video V2):** it works because the eSIM is data-only and the main SIM stays in the phone. The landing page should say so.
5. **Brand name:** the logo reads CALA while the product and CTA say CalaFly. Decide on one.
6. **Price:** add "from £X" only once it matches the landing page exactly.

## Suggestions
1. **Show the price as soon as it's confirmed.** "Pay once" is far stronger with a number next to it. The templates take a price line in minutes.
2. **Match the landing page to the ad.** Use the same headline per country, with refund terms and a phone-compatibility checker above the fold, plus Apple Pay / Google Pay.
3. **Send an install reminder** by email about 48 hours before the flight. This lifts install rate, cuts refunds and reduces support tickets.
4. **Round 2 creative:** creator-style arrival videos (phone connects as the plane lands), using the winning USP as the hook.
5. **Add audio:** the videos ship with a silent track. Add licensed music from Meta's Sound Collection or the YouTube Audio Library when uploading.

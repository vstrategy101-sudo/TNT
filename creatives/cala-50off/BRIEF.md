# Cala eSIM: 50% sitewide off, static creatives (internal draft)

Client: Cala eSIM (calafly.net), UK travellers, GBP. Ad account: "cala".
Built: 11 Nov 2026. 9 creatives × 2 sizes = 18 PNGs in `out/`.
Sizes: 4:5 (1080×1350) for Feed, 9:16 (1080×1920) for Stories and Reels.

## Summary

- 5 prospecting creatives and 4 retargeting creatives. Each one uses a different pattern interrupt: a sliced "50%", a receipt, a one-word "No.", a boarding pass, a postcard, a price tag, a sticky note, a night scene and a big "2 min".
- Every product claim is copied from Cala's own live ads in the account. I made up no prices, plan details or end dates.
- **Clear these 4 things before launch** (see Flags): the logo, the offer terms, the end date, and whether "sitewide" is literally true.

## Source of claims

**FACT** (from Cala's live ad copy in the ad account, pulled 11 Nov 2026):

| Claim used in image | Source (Cala ad copy) |
|---|---|
| One price for the whole trip / no daily roaming | "CALA eSIM: one price for your whole trip, no daily roaming" |
| Pay once for your trip, priced in pounds | "Pay once for your trip, priced in pounds, with no daily roaming charges." |
| Keep your WhatsApp number | "you keep your WhatsApp number" (free-trial retargeting ad) |
| Install at home, switch on when you land | "Install it at home, switch it on when you land." |
| Scan the QR code at home, land connected | "scan the QR code at home, land connected" |
| Sorted in 2 minutes | "Holiday data, sorted in 2 minutes." |
| 50% sitewide | User brief (11 Nov 2026) |

**Not verified:** I couldn't read calafly.net or download the existing ad images because the sandbox network blocks both. So I haven't checked the site's offer page, logo or colours.

## Creatives

The CTA button for all of them is **Shop now**. The link is calafly.net, or the offer landing page if there is one.

### Prospecting (cold UK travellers)

| # | File | Angle | Hook (what stops the scroll) | Primary text | Headline |
|---|---|---|---|---|---|
| P1 | P1-half-cut | Offer | A giant "50%" sliced in half | Holiday data, half price. Every plan on calafly.net is 50% off. One price for the whole trip, no daily roaming. | Half-price holiday data |
| P2 | P2-roaming-receipt | Pain | A receipt listing day-by-day roaming at "£?" | Roaming charges you by the day. Cala charges once for the whole trip, in pounds. And right now every plan is 50% off. | Stop paying by the day |
| P3 | P3-whatsapp-no | Objection | A huge coral "No." | Your WhatsApp number stays the same. Only your data changes. One price for the trip, 50% off every plan. | Keep your number. Half the price. |
| P4 | P4-boarding-pass | Ease | A boarding pass from "Daily roaming" to "One trip price" | Scan the QR code at home, land connected. Sort your data before the gate. 50% off every plan. | Sort your data before the gate |
| P5 | P5-breakup-postcard | Emotion/humour | A break-up postcard to roaming | Dear daily roaming, it's not me, it's you. One price for the whole trip, now 50% off sitewide. | Break up with roaming |

### Retargeting (site visitors 30d, ATC/IC no purchase 14d, free-trial users)

| # | File | Angle | Hook | Primary text | Headline |
|---|---|---|---|---|---|
| R1 | R1-you-looked | Offer to visitors | A price tag with "Full price" crossed out | You had a look at Cala. Now it's half price. Same plans, same data, 50% off sitewide. | You looked. It got cheaper. |
| R2 | R2-packing-list | Reminder | Packing list with eSIM circled as the last item | Passport, chargers, sun cream. Don't leave the eSIM for the airport. Install at home, switch on when you land. 50% off every plan. | Don't leave it for the airport |
| R3 | R3-install-tonight | Ease | Night scene: "Install it tonight." | Scan the QR code tonight. Switch it on when you land. One price for the whole trip, 50% off. | Install tonight. Land connected. |
| R4 | R4-two-minutes | Speed + price | A big "2 min" | Holiday data, sorted in 2 minutes. Choose your destination, pay once. Now half price. | Sorted in 2 minutes. Half price. |

## How to run it (RECOMMENDATION)

- **Prospecting:** run 1 campaign and 1 ad set with broad UK targeting, 18+. Put all 5 creatives in it, with both sizes on each ad (placement asset customisation). Optimise for Purchase.
  - Because the 5 angles are genuinely different, Meta has distinct options to test, which is better than giving it 5 colour variants.
- **Retargeting:** run 1 ad set with site visitors from the last 30 days, plus initiate checkout without purchase in the last 14 days. Exclude purchasers from the last 180 days.
  - Put the 4 R creatives in it.
- **Exclusions:** exclude the retargeting pool from prospecting so the two don't overlap.
- **Naming:**
  - Campaign: `Sales (UK) | Purchase | 2026-11-11 | 50% Sitewide`
  - Ads: `Ad 1 (P1 half cut)`, `Ad 2 (P2 receipt)`, and so on.
- **Budget:** I haven't set one because I don't have the budget or the current CPA.
  - **Check:** each ad set needs about 50 purchases a week to exit learning, so make sure the budget can get there. If it can't, merge the ad sets.
- **Overlap with the free trial:** the live retargeting ads push "free 500 MB". If both offers run to the same people, they compete with each other.
  - Pause the free-trial retargeting during the sale, or decide which offer wins. Owner: Sonal.

## Flags (fix before launch)

| # | Issue | Why it matters | Fix | Owner |
|---|---|---|---|---|
| 1 | **"Sitewide" / "every plan" must be literally true** | ASA upheld complaints against "20% off sitewide" ads where the code excluded items (Antler ruling 2026). | Confirm with Cala that the discount applies to all plans with no exclusions and no minimum spend. If there are exclusions, I'll rewrite as "50% off selected plans". | Vishnu |
| 2 | **Savings must be against the usual price** | The ASA expects "50% off" to be measured against a genuine prior selling price. | Get confirmation that the full prices have been charged recently. | Vishnu |
| 3 | **No end date in the creatives** | I left out "ends soon" and any countdown on purpose, because urgency without a real end date is an ASA/DMCC risk. | If there's a fixed end date, send it and I'll add "Ends [date]" to the fine print and an urgency variant. | Neha |
| 4 | **"T&Cs apply" needs a real T&C page** | Fine print points to calafly.net. | Make sure the offer T&Cs are live on the site. If there's a promo code, tell me and I'll add it. | Satyam |
| 5 | **Logo and colours are placeholders** | I couldn't load the site or the existing ad images, so the "cala eSIM" wordmark and the palette are mine, not Cala's. | Send the logo SVG/PNG and brand hex codes, then I'll re-render in about 5 minutes. | Shruti |
| 6 | **WhatsApp named in the P3 image** | Meta's brand rules limit using its brand names. Cala already uses "WhatsApp" in its ad text. Having it in the image is slightly riskier. Risk: Low–Medium. | If it gets rejected, swap the hook to "Will I lose my number?" | Sonal |
| 7 | **"2 minutes" is Cala's claim** | It needs to be true for a typical customer. | Confirm with the client. | Satyam |
| 8 | **Free-trial offer conflict** | See "Overlap with the free trial" above. | Decide which offer runs to which audience. | Sonal |

Things I deliberately kept out of the images, per Meta policy:
- fake buttons
- play icons
- notification badges
- tick-boxes

The CTA is a plain underlined text line, not a button shape. Source: [Meta: non-existent functionality](https://transparency.meta.com/policies/ad-standards/deceptive-content/non-existent-functionality/).

## How to measure

**Primary metric:** cost per purchase during the sale, compared with the pre-sale CPA.

**Watch AOV.** At 50% off, revenue per order halves. For ROAS to stay flat, conversion rate needs to roughly double.

> INFERRED: ROAS = (orders × AOV × 0.5) ÷ spend. To hold ROAS, orders ÷ spend must rise 2×.

After 7 days:
- Kill the creatives that aren't spending.
- Study the winning angle and make 2 variants of it.

## Re-render

```
node creatives/cala-50off/build.mjs
```

Copy is in `build.mjs`, with one block per creative. Fonts are embedded from `creatives/fonts/`, under the SIL Open Font License.

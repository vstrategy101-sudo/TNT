# CalaFly round 2: realistic creative set + sound design

Round 2 keeps the CalaFly site look (logo, pill tags, heavy Inter Display type, teal offset card, blue CTA). The flat graphics are replaced with product photography-style scenes: a hi-fi phone mock-up, iOS-style screens and rendered sets.

| Folder | Contents |
|---|---|
| `creatives/<country>/` | 5 concepts × 3 countries × 4 sizes (1:1, 4:5, 9:16, 1.91:1) = 60 PNGs |
| `videos/` | 2 films × 3 countries × 2 formats (9:16, 16:9), 15s, H.264 + AAC 256k = 12 MP4s |
| `audio/` | Final mix plus separate music and SFX stems for each film (48 kHz WAV) |
| `src/` | `kit.css`/`kit.js` (phone, screens, props, procedural scenes), `creative.html`, `video.html`, `sound.py`, render scripts |

Re-render: `cd src && node render-creatives.mjs && node render-videos.mjs` (the sound mix is rebuilt when its WAV is deleted).

## Competitor scan (Meta Ad Library, UK, active ads, 9 Oct 2026)

The Ad Library tool returns ad text and volume but not the images or videos, so this scan covers messages and testing behaviour, not visual style.

| Brand | Live ads | Leads with | Example headlines |
|---|---|---|---|
| Holafly | ≈307 | Discounts, anti-roaming, "unlimited" catalogue ads | "Travel with 5% OFF", "Say goodbye to roaming in 2026.", "Roaming? Not my problem" |
| Saily | ≈230 | One promise, many variants | "Get productive from touchdown… 200+ destinations" |
| Airalo | ≈100 | One brand line, ~30 variants | "Go further. Stay connected." |
| Maya Mobile | – | Spec claims | "Connected in under a minute", "No Data Caps. Ever.", "Fast 5G Data Abroad" |
| Breeze eSIM | – | Price anchors | "Travel data from $3.99", "Türkiye eSIM from $3.99" |
| E-Sim | – | Price anchor | "Mobile Data Abroad from £0.99" |
| ESIM App, Trip Sim | – | Arrival moment | "Land Connected. Every Trip.", "Land with Data On!" |
| Jetpac, Simify | – | Promo codes, "unlimited" + flags | "Use Code: ESIM15" |
| TurkSIM | – | Superlatives | "#1 eSIM For Dubai Tourists" |
| Advertorials | – | Story hooks | "My last roaming bill was £340. I haven't paid one since." |

**Patterns**
- **Volume over variety:** the big three run 100–300 live ads on one or two messages.
- **Price and discount first:** "from £0.99", "from $3.99", "5% off", promo codes.
- **Spec claims:** unlimited, 5G, no caps.
- **"Land connected" is crowded,** including our own round 1. Round 2 uses "Wheels down. Data on." and puts proof on screen instead.
- **Turkish noise:** "eşim" means "my spouse" in Turkish, so a plain "esim" search pulls in unrelated Turkish ads.

**Gaps CalaFly can own:** pay once (not per day), refund if not installed, set up from the sofa, and real proof on screen.

## Concepts (per country)

| # | Concept | Scene | Funnel |
|---|---|---|---|
| R1 | Wheels down. Data on. | Plane window with a destination sky; lock screen shows "CalaFly" network and arriving messages | Prospecting, intro |
| R2 | Set up in minutes. From the sofa. | Sofa, laptop showing a real calafly.net QR, phone camera scanning, "Activating eSIM" sheet | Prospecting |
| R3 | Pay once. Not per day. | Wooden table flatlay, boarding pass, order screen: "Payment: One-off ✓, Daily charges: None ✓" | Prospecting |
| R4 | Plans changed? Get a refund. | Studio product shot, "Not installed → Request refund" screen, "Refund request sent" toast | Prospecting + retargeting |
| R5 | Still flying to {country}? | Split-flap departures board (destination row highlighted), plan page on the phone | Retargeting |

Videos:
- **V3 Wheels down:** landing, then the phone wakes, setup, pay once, refund, end card.
- **V4 From the sofa:** QR install, departures board, landing, end card.

## Sound design

Everything is synthesised in `sound.py`: no samples and no licensed music.
- **Mix target:** −14 LUFS integrated, −1 dBTP.
- **Effects:** cabin rumble, seatbelt chime, touchdown thump, whooshes, message pings, camera focus beep, install progress glide, success chime, UI pops and taps, split-flap clatter, riser, closing chord.
- **Music bed:** 112 bpm, plucked arpeggio over a pad with a light kick. It is sidechain-ducked under each effect.
- **Original sounds:** the chimes are written to be generic, not copies of Apple's or any airline's sounds.

## Sign-off before launch
1. **Swap the mock screens for real CalaFly screenshots.** An ad can't show a product flow that differs from the real one (CAP 3.1). Each screen is one function in `kit.js`.
2. **Confirm the network label** "CalaFly" on the lock screen matches what the eSIM shows on a phone.
3. **"One-off" and "Daily charges: None"** on the order screen need the same pay-once sign-off as round 1.
4. **Illustrative messages:** "Mum" and "Holiday group" are invented. The phone is a generic mock-up with no Apple branding.

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

## Sound design (minimal, current)

`sound_min.py` is the current mix: no music, sparse clean cues (cabin chime, touchdown, swishes, glass message pings, focus tick, three-note confirm, departures-board clicks, end-card swell), soft attacks, nothing harsh above ~5 kHz, −16 LUFS / −1 dBTP. Run `python3 src/sound_min.py` to rebuild and remux all 12 films.

## Sound design (first pass, superseded)

Everything is synthesised in `sound.py`: no samples and no licensed music.
- **Mix target:** −14 LUFS integrated, −1 dBTP.
- **Effects:** cabin rumble, seatbelt chime, touchdown thump, whooshes, message pings, camera focus beep, install progress glide, success chime, UI pops and taps, split-flap clatter, riser, closing chord.
- **Music bed:** 112 bpm, plucked arpeggio over a pad with a light kick. It is sidechain-ducked under each effect.
- **Original sounds:** the chimes are written to be generic, not copies of Apple's or any airline's sounds.

## Licensed music drop-in (replaces the synth music)

The synthesised bed is a placeholder. For production, use a licensed track (Artlist, Epidemic Sound, Musicbed, etc.):

```
cd src
python3 music.py --track wheels=/path/trackA.wav --track sofa=/path/trackB.wav \
                 [--sfx-dir /path/licensed_sfx] [--start wheels=24.0] [--dry]
```

- **Cutting:** finds the tempo and beats, starts the body on a strong downbeat after any quiet intro, and keeps the track's real ending. It splices on a beat with an equal-power crossfade, so the final hit lands on the end card (13.0 s on V3, 12.4 s on V4).
- **Effects:** a file in `--sfx-dir` named after a cue (`notif.wav`, `landing.wav`, `whoosh.wav`, `success.wav`, `flaps.wav`…) replaces that sound. Cues without a file stay silent unless `--synth-sfx` is given.
- **Mixing:** music ducks 4 dB under each effect. Two-pass loudness normalisation to −14 LUFS / −1 dBTP, AAC 320k.
- **Output:** all 12 films are remuxed in place with no picture re-render. `--dry` writes only the mixes, to `.tmp/`.

Brief for picking tracks: modern electronic or indie-pop, 110–124 BPM, bright plucks or guitar, an optimistic travel feel, no vocals (the films carry on-screen copy), and a clean "button" ending rather than a fade.

## Sign-off before launch
1. **Swap the mock screens for real CalaFly screenshots.** An ad can't show a product flow that differs from the real one (CAP 3.1). Each screen is one function in `kit.js`.
2. **Confirm the network label** "CalaFly" on the lock screen matches what the eSIM shows on a phone.
3. **"One-off" and "Daily charges: None"** on the order screen need the same pay-once sign-off as round 1.
4. **Illustrative messages:** "Mum" and "Holiday group" are invented. The phone is a generic mock-up with no Apple branding.

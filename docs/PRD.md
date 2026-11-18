# Saphi — Product Requirements Document

> Status: Draft v0.3 · Date: 2026-11-18 · Owner: Auca17
> Languages: English (this file) · [Español](PRD.es.md)
> Prototype: [live artifact](https://claude.ai/artifact/Q6LCHyEBq3khP7uZvdvwQU) · source `prototype/saphi-prototype.html` · Decisions: [`docs/adr/`](adr/README.md) · Validation: [`docs/validation/interview-guide.md`](validation/interview-guide.md)

**Key decisions (grill-me round, 2026-11-18):** primary user = gardening beginners; first market = **Mendoza, Argentina**; UI in **Rioplatense Spanish**; free for users; future revenue from a paid shop map (ADR 0002); validate in Mendoza before building the backend; 8–16 h/week while validation holds.

---

## 1. Summary

Saphi is a **mobile-first web app (PWA)** for planning and caring for **ornamental gardens** and **home harvests**. The user enters the real size of a space, gets a to-scale grid (the **sandbox**), and places plants at their adult size. Saphi flags crowding, shade, soil pH mismatches, and invasive plants, suggests fixes such as moving a plant to a pot, and keeps the space alive with reminders, weather precautions and, later, sensors.

**One-liner:** "See your garden before you plant it, and keep it alive after."

## 2. Problem

People who design or start a garden struggle to:

1. **Imagine the layout:** how many plants fit, how big they get, where they go.
2. **Know which plants get along.** Plants are not "enemies". Some crowd each other as they grow, some need a different soil pH, and some are invasive and spread into their neighbors.
3. **Avoid shade:** tall plants block sun for short ones, and the sun angle changes with the season.
4. **Stay on top of care:** watering, feeding, harvesting at the right time, and reacting to the weather.

Existing tools cover one of these (garden planners, plant ID apps, irrigation controllers), not the whole loop: **plan → plant → care → harvest**, in a friendly mobile UX.

## 3. Target users

| Persona | Description | Main need |
|---|---|---|
| **Gardening beginner with little time** (primary) | Lives in Mendoza, starting out with a yard, balcony, or patio. Low plant knowledge. | "Tell me what fits, where, and how to protect it from hail, Zonda, and frost." |
| **Home harvester** | Grows vegetables and herbs for the household. | Plant interactions, sowing and harvest timing. |
| **Landscaper** (future segment) | Designs gardens for clients. Needs professional software; served later by a Pro plan (share plan with client, many projects). | Not in MVP scope. |

**First market:** Mendoza, Argentina (arid, irrigated gardens, mostly alkaline soil, hail, Zonda wind, late frost). Then the rest of Argentina, then other countries.

Non-target: commercial farms and professional agronomists (they already know this).

## 4. Goals and non-goals

### Goals
- G1. A new user creates a to-scale space and places plants in **under 5 minutes**, guided by the tutorial.
- G2. The sandbox flags **crowding, shade, soil pH, and invasive spread** in real time, with a fix where one exists.
- G3. Users come back weekly through **reminders, weather precautions, and gamification**.
- G4. Paying users stay subscribed because good habits lower their bill (see [ADR 0001](adr/0001-plus-achievement-discounts.md)).
- G5. The architecture is ready for **AI** (advisor, renders, photo analysis) and **sensors** without rewrites.

### Non-goals
- No social network or feed (high data cost, low value).
- No native iOS/Android app in v1 (PWA only).
- No professional agronomy (lab soil analysis, commercial yield models).
- No hardware sales in the MVP.

## 5. Product principles

1. **Mobile-first, thumb-first.** Every core action works one-handed on a ~375 px screen.
2. **Real units.** The grid is real centimeters. A plant's footprint comes from its adult size.
3. **Sensible defaults, full control.** Every plant has default sizes; the user can override them.
4. **Honest guidance.** Every warning says how sure it is: *measured*, *documented*, *traditional*, or *estimated*. The AI never invents data.
5. **Calm UI.** Glassmorphism, minimal, mostly white with dark green and brown; soft motion; no dark patterns in gamification; no data exploitation.

## 6. Information architecture

Bottom navigation bar, 4 tabs, always visible:

| Tab | Purpose |
|---|---|
| **Home** | Today's tasks, care streak, your spaces, what to sow this month, 5-day weather with precautions. |
| **Garden** | Ornamental spaces (sandbox). |
| **Harvest** | Edible spaces (sandbox + harvest timeline). |
| **Profile** | Level, Saphi Plus, tiered achievements, plant collection, settings (theme, location, hemisphere, tutorial). |

Garden and Harvest share the **same sandbox engine**. They differ in catalog, goals (bloom vs yield), and the Harvest timeline.

### Screen layout (Garden / Harvest)

```
┌──────────────────────────────────┐
│ Garden  [Front yard ▾]           │  title + space switcher
│ 4.0 × 6.0 m · 24 m² · grid 10 cm │  real dimensions
├──────────────────────────────┬───┤
│                              │ + │  add plant
│      SANDBOX (to scale)      │ ☀ │  sun and shadows
│                              │ 👁 │  show issues
│                              │ ↶ │  undo
├──────────────────────────────┴───┤
│ ◯ In a pot  ! Needs attention  ⋯ Good pair  ○ Selected │  map key
│ Free soil 82% · Water – – – · Issues 3                  │  stats strip
│ 🔔 Next reminder                                         │
├──────────────────────────────────┤
│  Home   Garden   Harvest  Profile│  bottom nav (glass)
└──────────────────────────────────┘
```

## 7. Functional requirements

Priority: **P0** = MVP · **P1** = right after MVP · **P2** = AI phase · **P3** = hardware phase.

### 7.1 Onboarding

| ID | Requirement | Priority |
|---|---|---|
| ON-1 | **First-run tutorial** of 6 short steps: welcome; draw your space; add and move plants; read the map (attention badge, pots, good pairs); sun and weather (pick a city or share location); achievements and Plus discounts. | P0 |
| ON-2 | Each step has a visual, a skip option, back/next, and progress dots. The location step is actionable inside the tutorial. | P0 |
| ON-3 | The tutorial can be replayed from Profile → Settings. | P0 |
| ON-4 | The real app starts with an empty, guided first space, not with example data. | P0 |

### 7.2 Spaces

| ID | Requirement | Priority |
|---|---|---|
| SP-1 | Create a space with **name**, **type** (garden / harvest), **width** and **length** in meters. | P0 |
| SP-2 | Optional **soil depth** in cm (raised beds, planters). | P0 |
| SP-3 | Several spaces per user, switched from the title chip (limits per plan in 7.10). | P0 |
| SP-4 | Edit dimensions after creation; plants outside the new bounds are flagged, never silently deleted. | P0 |
| SP-5 | Fixed obstacles on the grid (walls, trees, paths, paving). | P1 |
| SP-6 | Non-rectangular shapes (L-shape, polygon). | P1 |

### 7.3 Sandbox

**Model:** a grid in real units. Default cell = **10 cm** (25 cm for very large spaces). The sandbox keeps the **exact aspect ratio** of the space. Positions are stored in centimeters, so changing the grid never corrupts a layout.

**Plants are footprints**, drawn as ellipses sized by their **adult width and length**, filled with the plant's own color.

| ID | Requirement | Priority |
|---|---|---|
| SB-1 | Render to scale with grid, meter rulers, and a north marker. | P0 |
| SB-2 | Add a plant from a searchable catalog (bottom sheet); it lands on the first free spot. | P0 |
| SB-3 | Default adult width, length, and height per plant; the user can override all three. | P0 |
| SB-4 | Drag to move (snaps to the grid), keyboard arrows to nudge, duplicate, remove, undo. | P0 |
| SB-5 | **Plant interaction checks** within an influence radius: **crowding** (canopies overlap at maturity), **soil pH mismatch**, **invasive spread** (runners), **competition** (e.g. fennel), and **good pairs**. Each shows its reason and confidence. | P0 |
| SB-6 | **Clear markers:** a plant with an issue gets an **attention badge (!)** on its edge; good pairs are joined by a dotted green line; the selected plant gets a solid ring. A map key under the sandbox explains every marker. | P0 |
| SB-7 | **Pots:** any plant can be "in the ground" or "in a pot" with its own diameter. Drawn as a pot rim seen from above. A pot keeps roots and soil apart, so invasive, soil-pH, and root-competition warnings do not apply; crowding and shade still do. Root-level warnings offer a one-tap **"Put it in a pot"** fix. Warns if the pot looks too small for the plant. | P0 |
| SB-8 | **Free soil** metric (% and m²) and issue count under the sandbox. | P0 |
| SB-9 | Works offline; syncs when back online. | P1 |

### 7.4 Sun and shade

| ID | Requirement | Priority |
|---|---|---|
| SU-1 | **Location:** the user shares GPS location or picks a city. Saphi derives hemisphere, latitude, sun angle, local weather, and likely soil. | P0 |
| SU-2 | **Manual hemisphere** (Southern / Northern) stays available for users who do not share location. | P0 |
| SU-3 | **Shade check:** shadow length at solar noon = plant height ÷ tan(sun elevation), for today, midwinter, or midsummer. Warn when a tall plant shades one that needs full sun. | P1 |
| SU-4 | **Noon shadow layer:** toggle that draws every plant's noon shadow for the selected season. | P1 |
| SU-5 | **Sun study:** photos of the space from the same spot at 08:00, 13:00, and 19:00 (13:00 alone is enough to start). The MVP stores them; analysis that maps light and shade onto the grid is P2. | P1 / P2 |

### 7.5 Plant catalog

| ID | Requirement | Priority |
|---|---|---|
| PC-1 | Curated catalog of ornamental and edible plants (target: 150 species for MVP). | P0 |
| PC-2 | Per plant: common names (es/en), scientific name, family, adult height and spread (as ranges), spacing, sun, water, soil pH range, lifecycle, sowing months per hemisphere, days to harvest, rarity, color, weather traits (`lowFruit`, `heatBolt`, `frostTender`), flags (`invasive`, `allelopathic`, `pollinator`). | P0 |
| PC-3 | Pair relations: plant A ↔ plant B, good or bad, reason, confidence, source. | P0 |
| PC-4 | User-created custom plants (private). | P1 |
| PC-5 | Import pipeline from external sources with normalization and per-field source. | P1 |
| PC-6 | **MVP catalog for Mendoza:** about 60 species taken from what local nurseries sell most (list collected during validation), each with pros, cons, and full data. | P0 |
| PC-7 | **Native label** ("Nativa") and **water use 1–10** per species; average water use shown per space. Natives earn extra collection points. Wild natives are not pushed as garden picks. | P0 |
| PC-8 | **Invasive in Argentina** flag (e.g. *Gleditsia triacanthos* "acacia negra", *Robinia pseudoacacia* "acacia blanca"): placing one always shows a critical warning with a non-invasive alternative. | P0 |

Candidate sources (licenses to verify): USDA PLANTS, Perenual, Permapeople, Trefle, Wikidata, regional extension guides. Pair relations need **manual curation**; there is no single trustworthy dataset. Store ranges (min/max), not single numbers.

### 7.6 Care, weather, and sowing

| ID | Requirement | Priority |
|---|---|---|
| CR-1 | Auto-generated care tasks per plant (water, feed, prune, harvest) from catalog data and season. | P1 |
| CR-2 | Tasks on Home and the next reminder under the sandbox; web push notifications. | P1 |
| CR-3 | Mark a task done → feeds the weekly streak. | P1 |
| CR-4 | **5-day forecast** on Home: day, icon, high/low, rain in mm or "Dry". Nothing else on the strip. | **P0** |
| CR-5 | **Every day is tappable** and opens a detail sheet: summary, high, low, rain and chance, the alert explained, and what to do for your plants that day. | **P0** |
| CR-6 | **Alert days** are marked in amber **and** labeled with the alert ("Granizo", "Zonda", "Helada", "Lluvia", "Calor"), so the color is never the only signal. The detail sheet explains why. | **P0** |
| CR-7 | **Weather precautions** per plant: hail → cover crops and soft-leaved plants with hail net or shade cloth; Zonda → water early and shelter young and potted plants; frost → cover tender crops; heavy rain → lift low fruit off wet soil; heat → shade cloth for lettuce and hydrangea. Weather alerts are **P0** for Mendoza. | **P0** |
| CR-7a | **Irrigation type** per space: hose ("Manguera") or drip ("Goteo"); watering tasks use it. Turn-based irrigation ("por turno") is added if interviews show it is common. | P0 |
| CR-8 | Rain lowers watering advice ("Water less this week: about 44 mm of rain is coming"). Saphi only says **skip watering** when a soil sensor confirms the soil is wet (P3). | P1 |
| CR-9 | Forecasts change often (e.g. El Niño years). Precautions are re-checked every morning; days 4–5 say they are less certain. | P1 |
| CR-10 | **Sow this month:** crops to sow now for the user's hemisphere. Tapping one opens the catalog with it selected. | P1 |
| CR-11 | **Harvest timeline:** per crop, days since sowing, expected window, progress bar, "Ready". Emojis appear here and in harvest plant sheets only. | P1 |
| CR-12 | Crop rotation hints for the next season. | P2 |

### 7.7 AI planting advisor

The advisor answers questions like "With what I already have, what should I plant here?" It is **limited by design**: it never invents facts.

| ID | Requirement | Priority |
|---|---|---|
| AD-1 | Chat inside each space. Answers use the space's real data: size, free soil, plants, pots, sun and shade, location, soil, season, and forecast. | P1 |
| AD-2 | **Pipeline:** (1) gather context from the database and APIs; (2) the model proposes candidates **only from the catalog**; (3) each candidate is placed on a free spot and checked by the **same rule engine** as manual placements; (4) only candidates with no issues (or with a stated fix, like a pot) reach the user. | P1 |
| AD-3 | Every claim cites its source (catalog, soil map, forecast, rule) and says when it is estimating. Questions outside gardening are declined. | P1 |
| AD-4 | Each suggestion has an "Add to my space" button that places it on the grid. | P1 |
| AD-5 | Usage limits per plan; the model provider stays swappable. | P1 |

### 7.8 Soil data

| ID | Requirement | Priority |
|---|---|---|
| SO-1 | Likely soil pH, texture, and organic carbon for the user's coordinates. Sources: **INTA** soil maps (Argentina) and **ISRIC SoilGrids** (global, ~250 m grid). Licenses and API terms to verify. | P1 |
| SO-2 | Soil maps are regional estimates, not the user's yard: shown as "likely pH". A home test-kit reading entered by the user overrides them. | P1 |
| SO-3 | Soil pH feeds the pH checks and the advisor. In Mendoza (mostly alkaline), acid-loving plants in the ground get a "Suelo alcalino" warning with a one-tap pot fix. | P1 |

### 7.9 Profile and gamification

| ID | Requirement | Priority |
|---|---|---|
| GM-1 | **Level** from biodiversity points (Seedling → Sprout → Grower → Gardener → Landscaper → Master gardener). | P1 |
| GM-2 | **Plant collection:** every species planted is "discovered"; undiscovered ones show their point value. | P0 |
| GM-3 | **Weekly care streak** (weekly, so normal life is not punished). | P1 |
| GM-4 | **Biodiversity score:** points per species weighted by rarity, plus a bonus per plant family. | P1 |
| GM-5 | **Tiered achievements (I / II / III)** with progress bars: Collector (5/15/30 species), Steady hands (4/12/26 weeks), Good neighbors (1/3/5 spaces with zero issues), Pollinator friend (3/5/8 species in one space), Sun reader (1/3/9 photos), Weather-ready (1/10/25 precautions), Harvester (1/10/50 harvests). | P1 |
| GM-6 | **Plus achievements** (Good neighbors, Sun reader, Weather-ready): each new tier gives **20% off the next month of Plus**, applied automatically, one discount per month. See [ADR 0001](adr/0001-plus-achievement-discounts.md). | P2 |
| GM-7 | Free achievements give tier III rewards: discount on a soil sensor or the irrigation kit, one month of Plus. | P3 |
| GM-8 | No leaderboards or social features. | — |

### 7.10 Plans and limits

| ID | Requirement | Priority |
|---|---|---|
| PL-1 | **Beta / MVP:** everything free, unlimited spaces. | P0 |
| PL-2 | **Free plan (after beta):** one space per verified account (email, optional phone). Not per IP: IPs are shared by households, offices, and mobile carriers, and change often. | P2 |
| PL-3 | **Saphi Plus** (optional, later; planned US$5/month): unlimited spaces, AI advisor, sun-study analysis, AI renders, Plus achievements. The core app stays free. | P2 |
| PL-4 | **Shop map (next big feature after MVP):** nurseries and flower shops in Mendoza, curated by hand and stored long-term. Shops pay to rank higher **only when the user searches for a plant type they sell**, always weighted by distance and labeled "Destacado". Payment never changes plant advice ([ADR 0002](adr/0002-paid-placement-only-in-shop-map.md)). | P2 |
| PL-5 | **Nursery QR:** a counter QR that opens Saphi, first as a validation channel. | P1 |

### 7.11 Theming

| ID | Requirement | Priority |
|---|---|---|
| TH-1 | Glassmorphism: translucent panels with blur over a soft "dappled light" background. | P0 |
| TH-2 | **Day / night themes** switched by local time (sunrise/sunset when location is known). Manual Auto / Day / Night in settings. | P0 |
| TH-3 | **Night theme is designed, not inverted:** deep green-black ground, cool moonlit tints, brighter plant fills, and neutral pot rims (no terracotta brown at night). | P0 |
| TH-4 | WCAG AA contrast in both themes; respect `prefers-reduced-motion`. | P0 |

### 7.12 AI garden visualization (P2)

| ID | Requirement | Priority |
|---|---|---|
| AI-1 | The user photographs the real space and marks its 4 corners. | P2 |
| AI-2 | Generate a realistic render of the plan over the photo, labeled "illustrative". | P2 |
| AI-3 | Optional time slider: at planting, 3 months, adult. | P2 |
| AI-4 | Optional plant identification from a photo. | P2 |

### 7.13 Sensors and irrigation (P3)

| ID | Requirement | Priority |
|---|---|---|
| HW-1 | Saphi soil sensor: moisture, temperature, light; later EC/nutrients. | P3 |
| HW-2 | Assign a sensor to a zone; "Water – – –" becomes live data. | P3 |
| HW-3 | Device ingestion API (MQTT or HTTPS) with per-device tokens. | P3 |
| HW-4 | Integrations with existing irrigation controllers (candidates: Home Assistant, OpenSprinkler; to research). | P3 |
| HW-5 | Watering rules ("water zone B when moisture < 30%") and "skip watering" advice backed by sensor data. | P3 |
| HW-6 | In-app store for sensors and kits. | P3 |

## 8. Non-functional requirements

| Area | Requirement |
|---|---|
| Platform | Installable PWA; mobile Safari and Chrome Android. |
| Performance | Sandbox at 60 fps with 200 plants on a mid-range phone; first load < 3 s on 4G. |
| Offline | Sandbox editing offline (P1); last-write-wins sync with a conflict notice. |
| i18n | **Rioplatense Spanish first** (voseo), strings ready for translation; English later; metric units. |
| Accessibility | WCAG 2.2 AA. Plants are keyboard-focusable; every marker has a text equivalent; color is never the only signal. |
| Privacy | Store the minimum: email, city (not exact GPS), and the user's spaces. Usage analytics limited to whether people genuinely use the app (sessions, returning weeks, spaces created), privacy-friendly and ad-free. Photos deleted after analysis unless the user keeps them. No selling or sharing of user data. |
| Security | **Passwordless sign-in:** a one-time code sent by email, then a secure, HTTP-only session cookie. No passwords. Achievement progress computed on the server. Per-device sensor tokens. |

## 9. Technical architecture (proposal)

### 9.1 Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | React + TypeScript + Vite, PWA | Highly interactive client. |
| Sandbox | SVG first; Canvas if needed | Simple, accessible, easy hit-testing. |
| Styling | Tailwind + design tokens (day/night) | Token-based theming. |
| Backend | Django + Django REST Framework (or Django Ninja) | Founder wants to learn Django; the admin is ideal for curating the catalog. |
| Database | PostgreSQL (Supabase or Neon) + JSONB | See 9.2. |
| Jobs | Celery or Django-Q + Redis | Reminders, imports, forecasts, AI. |
| Storage | S3-compatible (Supabase Storage / Cloudflare R2) | Images and photos. |
| Weather | Open-Meteo | Free, no key, global. |
| Soil | INTA maps, ISRIC SoilGrids | See 7.8. |
| AI | LLM behind a backend service with tool calls into the rule engine | See 7.7. |

### 9.2 PostgreSQL over MongoDB Atlas

- Django's ORM, migrations, admin, and auth are built for relational databases; MongoDB's Django backend is younger and works with fewer third-party apps.
- The data is relational: users → spaces → placements → plants → pair relations.
- Flexible attributes fit in JSONB.
- Only sensor time-series (P3) is high-volume; TimescaleDB (a Postgres extension) covers it.

### 9.3 Core data model (draft)

```
User(id, email, locale, units, theme_mode, city, lat?, lon?, hemisphere, timezone, tutorial_done)

Space(id, user_id, name, kind[garden|harvest], width_cm, length_cm, depth_cm?,
      north_angle_deg?, cell_size_cm)

Placement(id, space_id, plant_id, x_cm, y_cm, spread_x_cm, spread_y_cm, height_cm,
          pot_diameter_cm?, count?, planted_at?, notes)

Plant(id, scientific_name, common_names{es,en}, family, height_cm_min/max,
      spread_cm_min/max, spacing_cm, sun, water, ph_min, ph_max, lifecycle,
      sowing_months_south[], days_to_harvest_min/max, rarity, color,
      traits[], flags[], sources{})

PairRelation(plant_a_id, plant_b_id, kind[good|bad], reason, confidence, source)

SoilEstimate(lat_round, lon_round, ph, texture, organic_carbon, source, fetched_at)
SoilReading(space_id, ph, measured_at)                          -- user test kit

CareTask(id, placement_id, kind, due_at, done_at?)
Forecast(location_key, day, hi, lo, rain_mm, chance, fetched_at)
Precaution(id, user_id, day, kind, plant_ids[], done_at?)

AchievementTier(user_id, chain, tier, earned_at)
PendingDiscount(subscription_id, percent, source_tier, applies_to_period)

SunStudyPhoto(space_id, slot[08|13|19], url, taken_at)          -- P1/P2
AdvisorMessage(space_id, role, content, citations[], created_at) -- P1
Device / Reading                                                 -- P3
```

### 9.4 Repo layout

```
saphi/
├── apps/web/          # React PWA
├── apps/api/          # Django
│   ├── accounts/  spaces/  catalog/  care/  weather/  soil/
│   ├── advisor/       # AI pipeline (tools call the rule engine)
│   └── gamification/  billing/
├── packages/rules/    # pure rule engine (crowding, pH, invasive, shade, pots), mirrored in TS
├── prototype/
└── docs/  (PRD, ADRs)
```

The **rule engine is pure code** with no framework imports: the sandbox, the advisor, and the tests all use the same functions.

## 10. Roadmap

| Phase | Content | Exit criteria |
|---|---|---|
| **0 — Prototype** ✅ | Clickable prototype in Rioplatense Spanish, adapted to Mendoza. | — |
| **0b — Validation (2 weeks)** | Interviews in Mendoza with the prototype: 10 beginners, 5 nurseries ([guide](validation/interview-guide.md)); collect the nursery plant list. | Go if ≥ 6/10 beginners would use it for their own space **and** ≥ 2 nurseries accept a counter QR. Otherwise it stays a learning project. |
| **1 — MVP (P0)** | Passwordless auth, spaces, sandbox with pots and checks, Mendoza catalog (~60), location/hemisphere, irrigation type, weather alerts (hail, Zonda, frost), sow this month, tutorial, collection, themes, PWA. Start with ~5–10 accounts. | **5–10 people who do not know us** use it and come back on their own at least 3 of 4 weeks. |
| **2 — Retention (P1)** | Tasks + push, harvest timeline, streak, achievements, shade, soil data, nursery QR, AI advisor. | Week-4 retention ≥ 25%. |
| **3 — Shop map + Plus (P2)** | Paid shop map (ADR 0002), optional Saphi Plus with automatic discounts (ADR 0001), sun-study analysis, renders. | First paying shops. |
| **4 — Hardware (P3)** | Sensor pilot, ingestion API, irrigation integrations, store. | 10 pilot sensors running for one month. |

## 11. Success metrics

- **Activation:** % who create a space and place ≥ 5 plants in the first session.
- **Tutorial completion** and time to first layout (target < 5 min).
- **Retention:** week-1 and week-4.
- **Fix rate:** % of warnings resolved (moved, resized, potted) vs dismissed.
- **Precaution follow-through:** % of weather precautions marked done.
- **Advisor acceptance:** % of advisor suggestions added to a space.
- **Plus conversion and churn**, and average discount per paying user.

## 12. Risks

| Risk | Mitigation |
|---|---|
| Plant and pair data quality and licensing. | Manual curation for the MVP; sources per field; confidence labels. |
| The AI advisor states wrong facts. | Catalog-only candidates, rule-engine validation, citations, refusal outside scope. |
| Soil maps differ from the real yard. | "Likely pH" wording; user test-kit override. |
| Sandbox too complex on a small screen. | Tutorial, map key, user testing with landscapers. |
| Discounts erode revenue. | One 20% discount per month, server-side achievements (ADR 0001). |
| Scope creep. | Phase gates; P2/P3 only after MVP metrics. |
| Hardware is a separate business. | Validate with off-the-shelf sensors and integrations first. |
| Founder bandwidth. | Small MVP; validate with real users early. |

## 13. Open questions

1. Final brand name: **Saphi**?
2. Which ~60 species for the Mendoza catalog (pending the nursery list).
3. Is turn-based irrigation ("riego por turno") common enough among beginners to support in the MVP?
4. Shop map pricing for nurseries (after validation).
5. Plus price in pesos, if Plus is launched at all.

## 14. Glossary

- **Space:** a garden or harvest area with real dimensions.
- **Sandbox:** the to-scale interactive grid of a space.
- **Placement:** a plant at a position in a space, with its own size, optionally in a pot.
- **Footprint:** the area a plant covers at adult size.
- **Pair relation:** a known good or bad interaction between two species.
- **Rule engine:** the shared code that checks crowding, pH, invasive spread, competition, and shade.
- **Plus achievement:** an achievement that takes 20% off the next month of Saphi Plus.

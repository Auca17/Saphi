# Saphi — Build Guide for Coding Agents

> Audience: an AI coding agent (e.g. Devin) or a developer building Saphi from this repository.
> Roles: **the founder decides product**, **Claude orchestrates and reviews PRs**, **the coding agent implements one milestone per PR**.
> Read this whole file before writing code. When something here conflicts with the PRD, this file wins for implementation details and the PRD wins for product intent. When something is unclear, stop and ask in the PR; do not guess product decisions.

---

## 0. Read first (in this order)

1. `docs/PRD.md` — product requirements (English). `docs/PRD.es.md` is the same in Spanish.
2. `docs/adr/0001-plus-achievement-discounts.md` and `docs/adr/0002-paid-placement-only-in-shop-map.md` — accepted decisions.
3. `prototype/saphi-prototype.html` — **the visual and interaction source of truth.** Single-file HTML/CSS/JS. Its CSS tokens, components, copy (Rioplatense Spanish), rule engine (`computeIssues`), sandbox renderer (`sandboxSVG`) and catalog data (`CATALOG`, `RELATIONS`, `SOW_SOUTH`) are what you port.
4. `saphi-startup/README.md` and `saphi-startup/06-validation/experiment-design.md` — why Milestone 1 is a waitlist with nursery QR codes.
5. `docs/validation/interview-guide.md` — context on the users.

Live prototype: https://claude.ai/artifact/Q6LCHyEBq3khP7uZvdvwQU

## 1. What Saphi is (one paragraph)

A free, mobile-first web app (PWA) for gardening beginners in **Mendoza, Argentina**. Users draw their garden or vegetable patch to scale, place plants at adult size, and get warnings (crowding, soil pH, invasive species, shade) with fixes such as "put it in a pot". They get weather precautions per plant for hail (granizo), Zonda wind and frost. Nurseries ("viveros") pay for their catalog and a counter QR inside Saphi. The UI is in **Rioplatense Spanish** (voseo: "plantá", "regá", "tocá").

## 2. Non-negotiable rules

- **Stack:** Django monolith (server-rendered templates + HTMX). No React, no Next.js, no separate SPA.
- **Language:** code, identifiers, comments, commit messages, docs → **English**. User-facing UI copy → **Rioplatense Spanish**, wrapped for translation (`{% translate %}` / `gettext`).
- **Privacy:** store the minimum (Ley 25.326, Argentina). No ads, no selling data, no third-party trackers. Usage analytics are first-party counters only.
- **Honest guidance:** plant advice and warnings never depend on who pays (ADR 0002). Code that ranks nurseries must not be imported by the rule engine or plant recommendations.
- **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`). **Never add "Co-Authored-By" or any AI attribution.** Keep each commit around 400 changed lines or less; tests and docs go in the same commit as the behavior.
- **Branches and PRs:** one branch and one PR per milestone (`feat/m1-waitlist`, `feat/m2-catalog`, …). Never commit directly to `main`. Never force-push `main`.
- **Tests first:** for every rule or behavior, write a failing test, then the code. Tests go through public interfaces (views via the Django test client, rule engine via its functions).
- **Secrets:** never commit `.env`, keys, or tokens. Use `.env.example` with placeholder values.
- **Do not edit** `prototype/`, `docs/PRD*.md`, `docs/adr/`, or `saphi-startup/` unless the milestone says so.

## 3. Stack and versions

| Layer | Choice | Notes |
|---|---|---|
| Language | Python 3.12 | |
| Package manager | `uv` | `uv init`, `uv add`, `uv run`. Commit `pyproject.toml` and `uv.lock`. |
| Framework | Django 5.2 LTS | |
| Interactivity | HTMX 2.x | Vendored as a static file (`static/vendor/htmx.min.js`), pinned version, no CDN at runtime. |
| Sandbox | Vanilla JS module ported from the prototype | `static/js/sandbox.js`, talks to JSON endpoints. |
| Database | PostgreSQL in production (Neon free tier), SQLite allowed for local dev | Configure with `DATABASE_URL` via `dj-database-url`. Use only features that work on both, or gate them. |
| Settings | `django-environ` | Reads `.env`. |
| Static files | WhiteNoise | Compressed manifest storage in production. |
| Phone numbers | `phonenumbers` | Normalize to E.164, default region `AR`. |
| QR codes | `segno` | Pure Python, generates SVG/PNG. |
| Weather | Open-Meteo forecast API (no key) | Milestone 4. |
| Tests | `pytest`, `pytest-django`, `factory-boy` | |
| Lint/format | `ruff` (lint + format) | Run before every commit. |
| Hosting | Render (web service, HTTPS) + Neon (Postgres) | HTTPS is required for the PWA and for phones to install it. |
| Email (Milestone 3) | Django email backend; console backend in dev; SMTP provider in prod (to decide) | |

## 4. Repository layout (target)

```
saphi/
├── manage.py
├── pyproject.toml / uv.lock
├── .env.example
├── config/                 # Django project: settings.py, urls.py, wsgi.py, asgi.py
├── apps/
│   ├── core/               # base templates, home, PWA manifest + service worker, health check
│   ├── waitlist/           # M1: nurseries, QR codes, signups
│   ├── catalog/            # M2: plants, pair relations, sowing months
│   ├── accounts/           # M3: passwordless email-code login
│   ├── spaces/             # M3: spaces, placements, sandbox views + JSON API
│   └── weather/            # M4: forecasts, alerts, precautions
├── saphi_rules/            # pure Python rule engine, NO Django imports (M3)
├── templates/              # base.html, partials/
├── static/
│   ├── css/tokens.css      # copied from the prototype's :root token blocks
│   ├── css/app.css
│   ├── js/sandbox.js       # M3
│   ├── vendor/htmx.min.js
│   └── icons/              # PWA icons
├── tests/                  # or apps/*/tests/
├── docs/                   # PRD, ADRs, this file
├── prototype/              # read-only reference
└── saphi-startup/          # read-only business docs
```

## 5. Design system (port, don't reinvent)

- Copy the four token blocks from the prototype `<style>` (`:root`, the dark `@media` block, `:root[data-theme="dark"], :root[data-mode="night"]`, `:root[data-mode="day"]`) into `static/css/tokens.css` unchanged.
- Fonts: Bricolage Grotesque (display), Figtree (body), IBM Plex Mono (measurements); Noto Color Emoji only for the harvest timeline. Self-host them in `static/fonts/` (download once, commit) so the app works offline.
- Reuse the prototype's component classes (`.glass`, `.panel`, `.row`, `.btn`, `.pill`, `.sheet`, `.nav`, `.seg`, `.check`, …) and SVG icon sprite.
- Day/night mode: auto by local time (07:00–19:00 = day), overridable in settings; stored on the user (anonymous users: `localStorage`).
- Motion rules: follow the prototype (sheets open 280 ms ease-out, close 150 ms ease-in; press scale .96; `prefers-reduced-motion` disables movement).
- Accessibility: WCAG 2.2 AA, touch targets ≥ 44 px, color never the only signal.
- Mobile first: design at 375 px wide; the layout is a single column max 460 px.

## 6. Milestones

Each milestone = one branch + one PR. Do them in order. Do not start the next milestone until the founder merges the PR.

### M1 — Waitlist with nursery QR codes + deploy (validation experiment 2)

**Goal:** real people scan a QR at a nursery counter (or open a link from a Facebook/Instagram group) and leave their WhatsApp to be told when Saphi is ready and to receive hail/Zonda/frost tips by hand. The founder sees how many people came from each nursery.

**Models (`apps/waitlist`):**
- `Nursery`: `name`, `slug` (unique, used in URLs), `zone` (choices: Capital, Godoy Cruz, Guaymallén, Las Heras, Luján de Cuyo, Maipú, San Martín, Tunuyán, San Rafael, Otra), `contact_name`, `contact_phone`, `notes`, `is_active`, `created_at`.
- `Visit`: `nursery` (FK, nullable for direct traffic), `source` (choices: qr, link, direct), `created_at`. No IP address, no user agent, no cookies beyond the session.
- `Signup`: `name`, `whatsapp` (E.164, unique), `zone` (same choices), `space_type` (patio, balcón, terraza, huerta, sin espacio todavía), `irrigation` (manguera, goteo, por turno, otro, no sé), `interests` (multiple: planificar mi espacio, alertas de clima, qué sembrar, dónde comprar), `nursery` (FK nullable, from the QR), `source`, `consent_at` (required), `created_at`.

**Views and URLs:**
- `/` → landing page (Spanish copy below) with the signup form (HTMX submit, inline validation, success state without page reload).
- `/v/<slug>/` → records a `Visit(source=qr)` and renders the same landing personalized: "Te lo recomienda Vivero X".
- `/l/<slug>/` → same, with `source=link` (for social posts).
- `/healthz` → 200 OK, for Render.
- Admin: `Nursery` with a "Download QR" action (PNG and SVG via `segno`, encoding the absolute `https://<host>/v/<slug>/` URL, with the nursery name printed below for a counter card), `Signup` list with filters (zone, nursery, interests, date) and a CSV export action, and a simple stats view: visits and signups per nursery, conversion %.

**Landing copy (Rioplatense Spanish, keep it short):**
- Title: "Planificá tu patio y enterate qué hacer cuando viene granizo"
- Subtitle: "Saphi te ayuda a elegir qué plantar, dónde, y cómo cuidarlo con el clima de Mendoza. Es gratis."
- 3 benefits with icons: "Tu espacio a escala", "Avisos de granizo, Zonda y helada", "Qué sembrar cada mes".
- Form button: "Avisame por WhatsApp".
- Consent checkbox (required): "Acepto que Saphi me escriba por WhatsApp sobre la app y el clima. Puedo darme de baja cuando quiera."
- Success: "¡Listo! Te escribimos cuando haya novedades. Mientras tanto, tapá tus plantas si viene granizo."
- Link to a short privacy page (`/privacidad/`) in plain Spanish: what is stored, why, how to delete it (write to the founder's contact address from settings).

**Validation rules (each needs a test):**
- WhatsApp numbers are normalized to E.164 with default region AR; invalid numbers show "Revisá el número: tiene que ser un celular de Argentina, por ejemplo 261 555 1234."
- A duplicate number does not create a second row; it shows "Ya estás anotado con ese número."
- Missing consent shows "Necesitamos tu permiso para escribirte."
- Unknown or inactive nursery slug → 404.
- Visits are counted once per session per nursery.

**PWA (M1 already installable):** `manifest.webmanifest` (name "Saphi", short_name "Saphi", start_url "/", display "standalone", theme/background colors from tokens, 192/512 px icons + maskable icon) and a minimal service worker that caches the landing shell and static assets (network-first for HTML). Served from the site root.

**Deploy:** Render web service from `main` (build: `uv sync --frozen && uv run python manage.py collectstatic --noinput && uv run python manage.py migrate`; start: `uv run gunicorn config.wsgi`), Neon Postgres via `DATABASE_URL`, `DEBUG=False`, `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` from env, `SECURE_*` settings on. Write `render.yaml` and a `docs/DEPLOY.md` with step-by-step instructions for the founder (who creates the accounts and sets the secrets; the agent never creates accounts).

**Acceptance criteria:**
- `uv run pytest` green; `uv run ruff check .` and `uv run ruff format --check .` clean.
- On a 375 px phone: the landing matches the prototype's look (glass panel, tokens, fonts), the form works with HTMX, and the success state shows.
- Admin can create a nursery, download its QR, scan it with a phone and land on `/v/<slug>/` with the nursery name shown.
- Stats view shows visits, signups and conversion per nursery.
- Lighthouse on mobile: PWA installable, accessibility ≥ 95.

### M2 — Plant catalog in the admin

**Goal:** the founder loads the ~60 Mendoza species from the nursery list.

- Models (`apps/catalog`): `Plant` (fields from PRD §7.5 PC-2: names es/en, scientific name, family, kind garden/harvest, height and spread **min/max**, spacing, sun, water 1–10, pH min/max, lifecycle, sowing months (southern hemisphere, list of ints), days to harvest min/max, rarity, color hex, traits list, flags: invasive, invasive_ar, allelopathic, pollinator, native, grammatical gender `g` for Spanish copy, sources JSON), `PairRelation` (plant_a, plant_b, kind good/bad, reason, confidence documented/traditional, source; unique unordered pair).
- Data migration seeding the 23 species and 6 relations from the prototype `CATALOG` and `RELATIONS` (convert single values to min=max).
- Management command `import_plants <csv>` with a documented CSV format (`docs/catalog-csv.md`), idempotent by scientific name, dry-run flag, row-level error report.
- Admin with search, filters (kind, native, invasive), and inline pair relations.
- Read-only catalog page `/catalogo/` with search (HTMX) and a plant detail sheet styled like the prototype.

### M3 — Accounts, spaces and the sandbox

- **Passwordless login** (`apps/accounts`): email → 6-digit code (expires in 10 minutes, max 5 attempts, rate-limited per email and per IP) → Django session cookie (HTTP-only, Secure, SameSite=Lax, 60-day expiry). Custom user model with email as username; created in M3 before any user data exists.
- **Rule engine** (`saphi_rules/`): pure Python port of the prototype's `computeIssues`, `gapBetween`, `rAt`, `shade`, `noonElevation`, `shadowLen`, `freeSoil`, `findFreeSpot`, including pots (root-level warnings skipped), invasive in Argentina, alkaline soil (only pH max < 6.6, in ground), allelopathy, pairs. Input/output are plain dataclasses. **Write the tests from the prototype's behavior first** (the seeded example spaces in the prototype are good fixtures: e.g. "Frente de casa" must produce the same issues).
- **Spaces** (`apps/spaces`): `Space` and `Placement` as in PRD §9.3 (positions in cm, `pot_diameter_cm` nullable, `count`, `planted_at`). JSON endpoints (`GET/POST/PATCH/DELETE`) used by `static/js/sandbox.js`; the server re-runs the rule engine on every change and returns issues.
- **Sandbox page:** port `sandboxSVG`, drag, keyboard move, undo, plant sheet, pots, legend, Detalles sheet from the prototype into `sandbox.js` + templates.
- Tabs: Inicio, Jardín, Cosecha, Perfil with the bottom nav from the prototype.

### M4 — Weather alerts and precautions

- `apps/weather`: daily management command `fetch_forecast` (Render cron) calling Open-Meteo for each user zone (round coordinates): `daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_gusts_10m_max,relative_humidity_2m_min,weather_code`, timezone `America/Argentina/Mendoza`, 5 days.
- Alerts: **Granizo** when `weather_code` is 96 or 99 (thunderstorm with hail); **Helada** when min ≤ 2 °C; **Zonda** heuristic when max ≥ 32 °C, gusts ≥ 45 km/h and min humidity ≤ 20% (document it as a heuristic, tune later); **Calor** when max ≥ 32 °C and not Zonda; **Lluvia** when precipitation ≥ 20 mm.
- Precautions per plant trait as in the prototype (`lowFruit`, `heatBolt`, `frostTender`, potted plants for Zonda). Never say "skip watering" without a sensor.
- Home ("Inicio"): today's tasks + precautions (max 3 + "Ver todas"), 5-day strip with tappable days, "Sembrá en <mes>".
- Web push notifications (Android; iOS only when installed) for alerts, opt-in.

### M5 — Profile, collection, achievements (later)

Port Profile from the prototype: level, collection, tiered achievements behind a trophy entry (the founder wants achievements hidden behind a trophy icon that opens the full list), settings. Plus billing is out of scope until validation passes.

## 7. Running locally and on a phone

```bash
uv sync
cp .env.example .env            # fill DJANGO_SECRET_KEY, DEBUG=True
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver 0.0.0.0:8000
```

- Phone on the same Wi-Fi: open `http://<computer-LAN-IP>:8000` (add the IP to `ALLOWED_HOSTS` in `.env`). Pages work, but **the service worker and "install app" need HTTPS**, so test installation on the Render URL (or a temporary HTTPS tunnel the founder starts).
- Document every command in `README.md` under "Development".

## 8. Definition of done (every PR)

- Tests written first and green; ruff clean; migrations committed and reversible where possible.
- Screenshots or a short screen recording at 375 px in the PR description (light and dark mode).
- PR description: what changed, how to test it, what is out of scope, known gaps.
- No secrets, no AI attribution, Conventional Commit messages.
- Update `README.md` / `docs/` when commands or behavior change.

## 9. Out of scope until the founder says otherwise

Saphi Plus billing, paid nursery map ranking (ADR 0002 is the contract when it comes), AI advisor, sun-study photo analysis, sensors and irrigation integrations, native apps, social features.

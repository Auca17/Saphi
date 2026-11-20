# Deploy Saphi to Render + Neon

Step-by-step for the founder. You create the accounts; the repo already has
everything else. Total time: ~15 minutes.

**What gets created:** a Render **Web Service** (runs Django + gunicorn,
serves HTTPS at `https://<name>.onrender.com`) connected to a **Neon**
Postgres database. Render redeploys automatically on every push to `main`.

## 1. Create the Neon database

1. Sign up at [neon.tech](https://neon.tech) → **New project** → name it
   `saphi`, region closest to your users, Postgres 16+.
2. After it is created, copy the **connection string** on the dashboard
   (the one starting with `postgresql://`, including `?sslmode=require`).
   Keep it — it is your `DATABASE_URL`.

## 2. Deploy the Render web service

1. Sign up at [render.com](https://render.com) with your GitHub account.
2. Dashboard → **New +** → **Blueprint** → pick the `Saphi` repository.
   Render reads `render.yaml` automatically.
3. When asked, fill in the environment variables marked `sync: false`:

   | Variable | Value |
   |---|---|
   | `ALLOWED_HOSTS` | `<your-service>.onrender.com` (no `https://`, no trailing `/`) |
   | `CSRF_TRUSTED_ORIGINS` | `https://<your-service>.onrender.com` |
   | `DATABASE_URL` | the Neon connection string from step 1 |
   | `FOUNDER_CONTACT_EMAIL` | the email shown on `/privacidad/` for data requests |

   `DJANGO_SECRET_KEY` is generated for you. `DEBUG=false` is already set —
   leave it.
4. **Deploy**. The build installs dependencies with `uv`, collects static
   files and runs migrations. Watch the logs until you see
   `Listening at: http://0.0.0.0:...`.

## 3. Create your admin user

In the Render dashboard: service → **Shell** tab → run:

```bash
uv run python manage.py createsuperuser
```

## 4. Create nurseries and QR cards

1. Open `https://<your-service>.onrender.com/admin/` and log in.
2. **Waitlist → Nurseries → Add**: name, zone, contact. The `slug` field
   fills itself from the name.
3. Back in the list, select the nursery → action **Download QR card (PNG)**
   (SVG also available). Each QR encodes
   `https://<your-service>.onrender.com/v/<slug>/` with the nursery name
   printed below — print it for the counter.
4. For social posts use `https://<your-service>.onrender.com/l/<slug>/`.

## 5. Verify it works

- `https://<your-service>.onrender.com/healthz` → `ok`.
- `/` shows the landing; submit your own number, check it appears in
  **Waitlist → Signups**.
- Scan the QR with a phone → the landing shows
  "Te lo recomienda <nursery>"; **Waitlist → Nurseries → Estadísticas**
  counts the visit.
- On Android Chrome, the browser offers **"Install app"** (PWA needs HTTPS,
  which Render provides).

## 6. Optional hardening

Once the site is confirmed working over HTTPS, set in the dashboard:

```bash
SECURE_HSTS_SECONDS=31536000
```

This tells browsers to only ever use HTTPS. Enable it *after* verification —
if something is wrong, the lock-in lasts a year.

## Notes

- **No real-time:** the free Render plan sleeps after inactivity; the first
  hit after sleep takes ~30 s. Upgrade later if it matters.
- **Phone on the same Wi-Fi** (local dev): pages work over `http://`, but the
  service worker and "install app" need HTTPS — test installation on the
  Render URL.
- **Custom domain later:** add it in Render → Settings → Custom Domains, then
  add the domain to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`. Existing QR
  cards keep working.

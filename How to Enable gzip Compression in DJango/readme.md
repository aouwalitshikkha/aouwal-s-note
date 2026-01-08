# Static Files in Production  
## Django + WhiteNoise + Nginx + Cloudflare (Free)

This repository uses a **build-time static file pipeline**.
Static assets are finalized before the application runs and are never processed by Django at runtime.

This document describes **what is actually configured and used**, not a generic tutorial.

---

## Architecture Used

```
Client
  ↓
Cloudflare CDN (Free plan)
  ↓
Nginx (reverse proxy + file server)
  ↓
Django (Gunicorn)
  ↓
WhiteNoise (build-time static preparation)
```

Each layer has a single, non-overlapping responsibility.

---

## Static File Philosophy

Static files in this project are treated as **immutable build artifacts**.

Once built:

- They are compressed
- They are versioned
- They are cache-safe
- They never touch Python
- They never enter Django views
- They are not modified by Nginx

---

## Step 1 — Static files are finalized by WhiteNoise

Static files are generated during deployment:

```bash
python manage.py collectstatic
```

This step is mandatory.  
The application is not considered deployable unless this succeeds.

After `collectstatic`, every static file is:

- **Already compressed**
  - Brotli (`.br`)
  - Gzip (`.gz`)
- **Already cache-safe**
  - Long-lived cache headers
- **Already versioned**
  - Content-hashed filenames

Example output:

```
staticfiles/
├── css/
│   ├── output.bd961c615b3e.css
│   ├── output.bd961c615b3e.css.gz
│   └── output.bd961c615b3e.css.br
├── js/
│   ├── backtotop.a8c1f2.js
│   └── backtotop.a8c1f2.js.br
└── fonts/
```

From this point onward:

- Django views are not involved
- Python does not touch static requests

---

## Step 2 — Django configuration used in production

Django does not compress or serve static files dynamically.
It only exposes URLs to finalized assets.

```python
# settings.py

DEBUG = False

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

WHITENOISE_MAX_AGE = 31536000  # 1 year
```

Notes:

- `CompressedManifestStaticFilesStorage` is required
- Hashed filenames are mandatory for CDN safety
- `DEBUG=True` disables this pipeline and is never used in production

---

## Step 3 — WhiteNoise middleware configuration (CRITICAL)

WhiteNoise must be inserted **immediately after** Django’s `SecurityMiddleware`.

This is not optional.  
Incorrect ordering will break static file serving.

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # MUST be here
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
```

What this achieves:

- Static requests are intercepted early
- Django views are bypassed
- Python execution is avoided for static assets

---

## Step 4 — Django does not serve static requests

At runtime:

- Requests to `/static/*` never enter Django views
- No middleware beyond WhiteNoise is executed
- No Python code runs
- No templates are rendered

Django only handles:
- HTML pages
- Forms
- API responses

Static delivery is fully offloaded.

---

## Step 5 — Nginx serves static files exactly as built

Nginx serves files **byte-for-byte** as produced by WhiteNoise.

It does NOT:
- Compress
- Rename
- Re-cache
- Rewrite paths

```nginx
location /static/ {
    alias /var/www/project/staticfiles/;
    access_log off;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

Important details:

- `alias` points directly to `STATIC_ROOT`
- `root` is not used
- Nginx does not modify content
- Headers match WhiteNoise behavior

---

## Step 6 — Compression responsibility

Compression occurs exactly once.

| Layer       | Compression |
|------------|-------------|
| WhiteNoise | Yes         |
| Nginx      | No          |
| Cloudflare | Pass-through |

Nginx compression is explicitly disabled:

```nginx
gzip off;
```

This avoids:
- Double compression
- CPU waste
- Inconsistent `Content-Encoding`

---

## Step 7 — Cloudflare (Free plan) caching

Cloudflare caches static files exactly as received.

Cache rule used:

```
URL: example.com/static/*
Action: Cache everything
Edge TTL: 1 month
Browser TTL: 1 year
```

Cloudflare automatically serves:
- Brotli when supported
- Gzip otherwise

No paid features are required.

---

## Runtime Request Flow

### First request

```
Client → Cloudflare → Nginx → staticfiles → Response
```

### Subsequent requests

```
Client → Cloudflare cache → Response
```

Result:
- Django is not hit
- Nginx is usually not hit
- Server CPU usage is minimal

---

## Verification Used

### Browser DevTools

Check a static file response:

```
content-encoding: br
cache-control: max-age=31536000, immutable
cf-cache-status: HIT
```

### Manual test

```bash
curl -H "Accept-Encoding: br" -I https://example.com/static/css/output.css
```

Expected:

```
Content-Encoding: br
```

---

## Explicit Non-Goals

This setup intentionally avoids:

- Serving static files via Django views
- Runtime compression
- Nginx-level optimization logic
- Dynamic static file handling
- MEDIA file handling (uploads are separate)

---

## Summary

- WhiteNoise finalizes static files at build time
- WhiteNoise middleware intercepts static requests
- Nginx serves files without modification
- Cloudflare caches them globally
- Django never processes static requests

Static files are **immutable build artifacts**, not application logic.

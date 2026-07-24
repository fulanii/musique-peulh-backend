# MusiquePeulh (Backend)

Backend for **MusiquePeulh** — a free, open-source music streaming service for
discovering and listening to Fulani music across West Africa and the Sahel.
Built with **Django REST Framework**, this project was developed entirely by me
without ai, to demonstrate my backend engineering skills and showcase a production-style
implementation with JWT authentication, user and role management, secure media
upload/streaming, and playlist APIs that power the
[frontend client](https://github.com/fulanii/musique-peulh-frontend).

**Live API:** https://api.musiquepeulh.com · Interactive docs at `/api/docs/` (Swagger) — schema via drf-spectacular.

---

## ✨ What this project demonstrates (backend focus)

- **Secure JWT auth** with access/refresh rotation, token blacklisting on logout, and custom token claims.
- **Private media pipeline** — files are uploaded to object storage and served only through **short-lived pre-signed URLs**, never from a public bucket.
- **Ownership-scoped authorization** on every user-owned resource (a resource you don't own returns `404`, so existence isn't leaked).
- **Per-endpoint rate limiting** with scoped throttle classes.
- **Modular, scalable app layout** — views and serializers split one-per-endpoint instead of monolithic files.
- **Environment-separated, security-hardened production config** and full OpenAPI documentation.

---

## 🚀 Features

### 🔐 Authentication & Users

- Custom user model (email as the login identifier), login by email **or** username
- JWT auth via **SimpleJWT** — access/refresh tokens, refresh rotation, and token **blacklisting** on logout
- Custom `TokenObtainPair` serializer embedding `username`/`email` claims
- Email verification with 6-digit codes, resend flow, and password reset — delivered via **Brevo**
- Admin user management: list users, promote to admin, delete
- Input validation with clean, field-name-free error messages

### 🎵 Songs & Streaming

- Upload songs (`.mp3`) + cover art to **Cloudflare R2** (S3-compatible, private bucket)
- Automatic audio-duration extraction with **mutagen**
- **Secure streaming via short-lived pre-signed URLs** — audio is never publicly accessible
- Duplicate-title-per-artist prevention and automatic Title-Case metadata normalization (custom model manager/queryset)
- Browse endpoints: all songs, by artist, by title, by uploader; admin song metadata editing

### 📂 Playlists

- Full CRUD — create, list, rename, delete
- Add / remove songs (many-to-many), all **scoped to the owner**
- Efficient reads with `prefetch_related` to avoid N+1 queries

### 🧩 API & Docs

- RESTful design following DRF best practices; class-based views organized per endpoint
- Auto-generated **OpenAPI 3** schema with **drf-spectacular** (Swagger + Redoc), tagged by domain
- Serializer-based validation with consistent JSON error responses
- Per-scope throttling (`AnonRateThrottle` / `UserRateThrottle`) on auth and media endpoints

### ⚙️ Production-Ready

- Split settings (`base` / `local` / `prod`) with `.env` config via **python-dotenv**
- Deployed on **Railway** with **Gunicorn** + **PostgreSQL**
- Security hardening: HSTS, SSL redirect, secure/CSRF cookies, `X-Frame-Options`, proxy SSL header, CORS allow-list
- Test suite with **pytest** + the DRF test framework (models, serializers, views) and shared fixtures

---

## 🗺️ Roadmap

- **YouTube upload via background tasks** — ingest audio directly from a YouTube URL. Because downloading/processing is long-running, it will run **asynchronously on a background task queue** (e.g. Celery/RQ) so the request returns immediately and the track is added once processing completes.

---

## 🛠 Tech Stack

- **Python 3 / Django 5 / Django REST Framework**
- **SimpleJWT** — authentication (+ token blacklist)
- **drf-spectacular** — OpenAPI 3 schema & docs
- **django-storages + boto3** — Cloudflare R2 (S3-compatible) media
- **mutagen** — audio metadata
- **Brevo** — transactional email
- **PostgreSQL** (prod) / **SQLite** (dev)
- **Gunicorn** on **Railway**
- **pytest** — testing

---

## 🌍 Deployment

| Layer          | Service                          |
| -------------- | -------------------------------- |
| Backend / WSGI | Django REST Framework + Gunicorn |
| Hosting        | Railway                          |
| Database       | PostgreSQL                       |
| Object storage | Cloudflare R2 (S3-compatible)    |
| Email          | Brevo                            |

- **Production URL:** https://api.musiquepeulh.com
- **Frontend Repo:** https://github.com/fulanii/musique-peulh-frontend

---

## 🏗️ Project Structure

Apps use a modular layout — each endpoint gets its own view and serializer
module, plus dedicated `throttles` and `utils`:

```
musique_peulh/
├── accounts/                     # auth, users, roles
│   ├── models.py                 # custom user model
│   ├── throttles.py              # scoped auth throttles
│   ├── utils.py                  # code generation, email sending
│   ├── views/                    # register, login, verify, resend,
│   │   └── ...                   #   password reset, user CRUD, roles
│   ├── serializer/               # one serializer per action (+ token.py)
│   └── test/                     # model / serializer / view tests
│
├── songs/                        # songs, streaming, playlists
│   ├── models.py                 # Song, Playlist (+ custom manager/queryset)
│   ├── throttles.py              # scoped media throttles
│   ├── utils.py                  # r2_client, upload_r2, get_audio_duration
│   ├── views/                    # all_songs, artist_songs, song_data,
│   │   └── ...                   #   song_upload, songs_edit, stream, playlists
│   ├── serializers/              # song, song_upload, songs_edit, playlists
│   └── test/
│
├── musique_peulh/
│   ├── settings/                 # base.py / local.py / prod.py
│   ├── urls.py
│   └── wsgi.py · asgi.py
│
├── manage.py · requirements.txt · pytest.ini
```

---

## 🧑‍💻 Getting Started (local)

```bash
# 1. Clone & enter
git clone https://github.com/fulanii/musique-peulh-backend.git
cd musique-peulh-backend

# 2. Virtual env + deps
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Configure environment (.env) — e.g.
#    SECRET_KEY, DJANGO_SETTINGS_MODULE=musique_peulh.settings.local
#    R2_* credentials, BREVO_API_KEY / BREVO_BASE_URL, DB_* (prod)

# 4. Migrate & run
python manage.py migrate
python manage.py runserver
```

Run the tests:

```bash
pytest
```

API docs are available at `/api/docs/` (Swagger) and `/api/schema/` (raw OpenAPI) when `DEBUG` is on.

---

## 🧑‍💻 Author

[Yassine](https://yassinecodes.dev) · [LinkedIn](https://www.linkedin.com/in/yassinecodes/) · [Twitter / X](https://x.com/yassinecodes)

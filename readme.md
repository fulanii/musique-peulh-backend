# MusiquePeulh (Backend)

This repo is the backend for MusiquePeulh a free and open source music streaming app, where users can discover and 
listen to Fulani music across West Africa and the Sahel region. Built with **Django Rest Framework (DRF)**, 
this backend provides secure authentication, user management, and music data APIs that power the frontend client.


## 🚀 Features

### 🔐 Authentication & Users
- Custom user model using email as the username
- JWT-based authentication (via SimpleJWT)
- Email verification with 6-digit codes
- Case-insensitive username handling
- Full input validation (regex, unique checks, etc.)

### Song Management
- Upload songs (.mp3 only) and cover images
- Auto-extract audio duration using mutagen
- Prevent duplicate song titles for the same artist
- Automatically formatted (Title Case) metadata
- Uploads stored securely in DigitalOcean Spaces

### 🧩 API & Docs
- RESTful API architecture following DRF best practices
- Auto-generated OpenAPI 3.0 schema with drf-spectacular
- Interactive API docs (Swagger & Redoc)
- Serializer-based data validation and clean error responses

### ⚙️ Production-Ready
- Separate settings for local and production
- Deployed on Railway using Gunicorn + Neon PostgreSQL
- .env-based configuration with python-dotenv
- Security hardened (HSTS, CSRF, SSL, secure cookies, etc.)
- Full test coverage with DRF test framework


## 🛠 Tech Stack
- **Python 3**
- **Django 5**
- **Django Rest Framework**
- **SimpleJWT** for authentication
- **SQLite3** (dev) / **Postgres** (prod)

## 🌍 Deployment

#### Current stack:
- 🧠 Backend: Django REST Framework + Gunicorn
- 🛠️ Hosting: Railway
- 🧰 Database: Neon PostgreSQL
- ☁️ File Storage: DigitalOcean Spaces (s3 compatible)
- 📧 Email Service: Resend
- Production URL: https://api.musiquepeulh.com
- Frontend Repo: https://github.com/fulanii/musique-peulh-frontend


## 🏗️ Project Structure
```
├── accounts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_customuser_is_verified.py
│   │   └── 0003_customuser_verification_code.py
│   ├── models.py
│   ├── serializer.py
│   ├── test
│   │   ├── test_models.py
│   │   ├── test_serializers.py
│   │   └── test_views.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── db.sqlite3
├── docs
│   ├── api-spec.md
│   └── MVP Architecture.drawio
├── manage.py
├── musique_peulh
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── local.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── pytest.ini
├── readme.md
├── requirements.txt
└── songs
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   ├── __init__.py
    │   ├── 0001_initial.py
    │   ├── 0002_alter_song_upload_date.py
    │   ├── 0003_alter_song_audio_file_alter_song_cover_image.py
    │   ├── 0004_alter_song_audio_file_alter_song_cover_image.py
    │   └── 0005_alter_song_title.py
    ├── models.py
    ├── serializer.py
    ├── test
    │   ├── __init__.py
    │   ├── assets
    │   │   ├── main.html
    │   │   ├── test_audio.mp3
    │   │   └── test_cover.avif
    │   ├── test_models.py
    │   ├── test_serializers.py
    │   └── test_views.py
    ├── urls.py
    ├── utils.py
    └── views.py
```


## 🧑‍💻 Author

[Yassine](https://yassinecodes.dev) | [LinkedIn](https://www.linkedin.com/in/yassinecodes/) | [Twitter X](https://x.com/yassinecodes) 
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


## 🏗️ Project Structure
```
  musique-peulh-backend/
  ├── accounts/              # Authentication app
  │   ├── models.py          # CustomUser model
  │   ├── serializers.py     # Register, Login serializers
  │   ├── views.py           # Auth endpoints (register, verify, login)
  │   └── urls.py
  │
  ├── songs/                 # Song management app
  │   ├── models.py          # Song model
  │   ├── serializers.py     # Song serializers
  │   ├── views.py           # Upload, list, detail views
  │   └── urls.py
  │
  ├── musique_peulh/
  │   ├── settings/
  │   │   ├── base.py
  │   │   ├── local.py
  │   │   └── prod.py
  │   ├── urls.py
  │   ├── wsgi.py
  │   └── asgi.py
  │
  ├── utils/
  │   ├── audio_utils.py     # Extract audio duration, sanitize filenames
  │   └── upload_do.py       # Upload files to DigitalOcean Spaces
  │
  ├── manage.py
  └── requirements.txt
```


## 🧑‍💻 Author

[Yassine](https://yassinecodes.dev) | [LinkedIn](https://www.linkedin.com/in/yassinecodes/) | [Twitter X](https://x.com/yassinecodes) 
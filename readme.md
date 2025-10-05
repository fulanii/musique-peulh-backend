# MusiquePeulh (Backend)

This repo is the backend for MusiquePeulh a free and open source music streaming app, where users can discover and 
listen to Fulani music across West Africa and the Sahel region. Built with **Django Rest Framework (DRF)**, 
this backend provides secure authentication, user management, and music data APIs that power the frontend client.

---

## 🚀 Features

- User registration and login with **JWT authentication**  
- Account management (sign up, log in, log out, refresh tokens)  
- Music catalog endpoints (artists, playlists)  
- Music upload to  s3 compatible DigitalOcean storage spaces
- Secure API design with DRF best practices  
- Environment-based settings (local, production)  
- SQLite for development (switchable to Postgres in production)  

---

## 🛠 Tech Stack

- **Python 3**
- **Django 5**
- **Django Rest Framework**
- **SimpleJWT** for authentication
- **SQLite3** (dev) / **Postgres** (prod)

---

## ⚙️ Setup & Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/fulanii/musique-peulh-backend
cd musique-peulh-backend

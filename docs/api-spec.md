# Musique Peulh API Specification

This document describes the REST API endpoints for **Musique Peulh**, a music streaming platform focused on Fulani music.

---

## Authentication

### Register
- **POST** `/api/auth/register/`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "username": "JohnDoe",
    "password": "securepass123"
  }
  ```
Responses:
- 201 Created → user registered
- 400 Bad Request → validation errors

### Login
- **POST** `/api/auth/login/`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepass123"
  }
  ```
Responses:
- 200 OK → returns JWT access + refresh tokens
- 401 Unauthorized → invalid credentials

---

## Songs

### Upload Songs
- **POST** `/api/songs/upload`
- **Request Body**: `(multipart/form-data)`
  ```json
  {
    "title": "Denke Denke",
    "artist_name": "Disco Fils",
    "duration": 3.15,
    "upload_by": "YassineCodes",
    "audio_file" file
    "cover_file": file
  }
  ```
Responses:
- 201 Created → song uploaded
- 400 Bad Request → missing/invalid fields

### Get Song (using Title)
- **GET** `/api/songs/title/<title>`
Response:
- 200 OK -> return song
- 404 -> Not Found

### Get Song (using Artist Name)
- **GET** `/api/songs/title/<artist_name>`
Response:
- 200 OK -> return song
- 404 -> Not Found

### Get Song (using Uploaded By)
- **GET** `/api/songs/title/<uploaded_by>`
Response:
- 200 OK -> return song
- 404 -> Not Found
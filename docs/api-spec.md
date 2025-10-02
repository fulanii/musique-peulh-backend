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
Responses:
- 201 Created → user registered
- 400 Bad Request → validation errors

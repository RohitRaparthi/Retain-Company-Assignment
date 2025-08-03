# ✅ Changes.md — URL Shortener Project

This document outlines all the key changes made during the development and debugging of the URL Shortener Flask application.

---

## ✅ Folder Structure Finalized

```
url-shortener/
├── app/
│ ├── init.py # 🔹 Made app a Python package
│ ├── main.py # 🔹 Flask app entry point
│ ├── routes.py # 🔹 API route handlers
│ ├── utils.py # 🔹 Utility functions (short code gen, URL validation)
│ ├── test_basic.py # 🔹 Pytest unit tests for endpoints
│ └── models.py # 🔹 In-memory database (dictionary-based)
├── requirements.txt
├── Readme.md 
└── changes.md # 📄 This changelog
```

## 🔨 Implemented Core Files

### `main.py`
- Created Flask app instance.
- Added `/` and `/api/health` endpoints for health checks.
- Registered API blueprint from `routes.py`.

### `routes.py`
- Implemented the following endpoints:
  - `POST /api/shorten-url` → accepts long URL, returns short code.
  - `GET /<short_code>` → redirects to the original URL.

### `models.py`
- Created an in-memory storage dictionary:
  - Maps short codes to long URLs.

### `utils.py`
- ✅ `generate_short_code()` – generates unique 6-character alphanumeric short code.
- ✅ `is_valid_url(url)` – validates URLs using regex.

---

## ✅ Testing with `pytest`

### `test_basic.py`
- Wrote unit tests for:
  - Health check endpoints.
  - URL shortening with valid/invalid input.
  - Redirect functionality with valid/invalid short codes.

---

## ✅ Summary

- All endpoints and test cases now work correctly.
- Project is fully modular and testable.
- No ModuleNotFoundError or import issues remain.

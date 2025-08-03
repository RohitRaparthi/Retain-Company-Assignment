# CHANGES.md

## ✅ Overview

This document outlines the major issues identified in the original codebase, the refactoring decisions made, and justifications for each change.

---

## 🔍 Major Issues Identified

1. **Poor Code Organization**
   - All logic was in a single `app.py` file, leading to a monolithic structure.
   - No separation of concerns between routing, business logic, models, and utilities.

2. **Security Vulnerabilities**
   - Raw input data used directly without validation.
   - Passwords were stored in plaintext.
   - SQL queries susceptible to injection attacks.

3. **Missing Best Practices**
   - Improper or missing HTTP status codes.
   - Unhandled exceptions could crash the server.
   - No use of reusable helper functions.

4. **Testing Absence**
   - No test cases were written.
   - No validation that core functionalities work as expected.

---

## ✅ Changes Made

### 1. **Code Reorganization**
- Created a modular folder structure:

```
messy-migration/
├── routes/
│ └── user_routes.py
├── utils/
│ ├── auth.py
│ └── db.py 
├── app.py
├── init_db.py
├── test_app.py
├── requirements.txt
├── Readme.md 
└── changes.md 
```

- `app.py` now only initializes the app and routes.
- Business logic and DB operations moved to `routes.py` and `models.py`.

### 2. **Security Improvements**
- Added password hashing using `werkzeug.security`.
- Introduced input validation for fields like email and name.
- Parameterized all SQL queries to prevent injection.

### 3. **Best Practices**
- Consistent and correct use of HTTP status codes (`200`, `201`, `400`, `404`, `500`).
- Centralized error handling using `try-except`.
- Created utility functions in `utils.py` for:
- Password hashing/verification
- Input validation

### 4. **Testing**
- Added test cases in `test_app.py` for:
- Creating a user
- Retrieving a user
- Logging in
- Deleting a user
- Used `unittest` framework and Flask test client.

---

## 🔁 Trade-offs / Assumptions

- Assumed SQLite remains the database (no ORM used).
- Retained basic login without session management (no JWT or cookies).
- Did not implement full coverage testing due to time limits.
- Did not add input schemas (e.g., with Marshmallow or Pydantic) to avoid adding new dependencies.


## 📝 Summary

- Refactored the project for modularity, security, and reliability. Introduced proper folder structure, separated concerns (routes, utils, models), secured input handling and password storage, and implemented unit tests for key functionalities.

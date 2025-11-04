# ekyc-41822-41867

This repository contains the BackendAPIService for the EKYC application.

- FastAPI app with JWT auth + RBAC
- SQLAlchemy models and SQLite/Postgres support
- Endpoints for auth, users, kyc cases, admin stats
- OpenAPI generation script at src/api/generate_openapi.py

Environment:
- A starter .env is included at BackendAPIService/.env with example values (DATABASE_URL on port 5000, JWT secret, storage, CORS to http://localhost:3000, and healthcheck path).
- The WebFrontend container should define REACT_APP_API_BASE (and optionally REACT_APP_BACKEND_URL) in its own .env to point to this backend (e.g., http://localhost:8000).
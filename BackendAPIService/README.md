# EKYC BackendAPIService

FastAPI backend providing EKYC features: auth with JWT, RBAC, users management, KYC case submission and review, local file storage, and audit logging.

## Quickstart

1. Create a virtual environment and install requirements:

   pip install -r requirements.txt

2. Copy .env.example to .env and set variables (JWT_SECRET_KEY, DATABASE_URL, etc.). The orchestrator will inject env automatically in deployed environments.

3. Run the API:

   uvicorn src.api.main:app --host 0.0.0.0 --port ${PGPORT:-8000} --reload

4. Generate OpenAPI spec (optional):

   python -m src.api.generate_openapi

## Notes

- Default admin user "admin" with password "admin123" is created on first start. Change the password immediately using the admin endpoints.
- Local storage for uploads is under STORAGE_DIR (default ./storage).
- Health check path is configurable via PGHEALTHCHECK_PATH (default "/").

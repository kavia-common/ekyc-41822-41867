# EKYC BackendAPIService

FastAPI backend providing EKYC features: auth with JWT, RBAC, users management, KYC case submission and review, local file storage, and audit logging.

## Quickstart

1. Create a virtual environment and install requirements:

   pip install -r requirements.txt

2. Create a .env file (one is provided at BackendAPIService/.env in this repo as a starter) and set variables:
   - DATABASE_URL (e.g., postgresql+psycopg2://appuser:dbuser123@localhost:5000/myapp)
   - JWT_SECRET_KEY (e.g., change-me)
   - PGFRONTEND_URL (e.g., http://localhost:3000) for CORS
   - STORAGE_DIR (e.g., ./storage)
   - PGHEALTHCHECK_PATH (e.g., /health)
   The orchestrator will inject env automatically in deployed environments.

3. Run the API:

   uvicorn src.api.main:app --host 0.0.0.0 --port ${PGPORT:-8000} --reload

4. Generate OpenAPI spec (optional):

   python -m src.api.generate_openapi

## Notes

- Default admin user "admin" with password "admin123" is created on first start. Change the password immediately using the admin endpoints.
- Local storage for uploads is under STORAGE_DIR (default ./storage).
- Health check path is configurable via PGHEALTHCHECK_PATH (default "/health" as set in the provided .env).
- CORS is controlled via PGFRONTEND_URL; set it to your WebFrontend origin (e.g., http://localhost:3000).

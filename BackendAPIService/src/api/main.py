from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.core.config import settings
from src.core.db import init_db
from src.core.security import create_default_admin_if_missing
from src.routers import auth as auth_router
from src.routers import users as users_router
from src.routers import kyc as kyc_router
from src.routers import admin as admin_router
from src.utils.docs import openapi_tags, websocket_usage_help_route


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application with:
    - CORS
    - Routers (auth, users, kyc, admin)
    - OpenAPI metadata and tags
    - Startup tasks (DB init, default admin)
    """
    app = FastAPI(
        title="EKYC Backend API",
        description="Secure backend for EKYC workflows, authentication, RBAC, KYC case management, and document handling.",
        version="1.0.0",
        contact={"name": "EKYC Team"},
        license_info={"name": "Proprietary"},
        openapi_tags=openapi_tags,
    )

    # CORS
    allow_origins: List[str] = []
    # If frontend URL is provided, prioritize it; otherwise allow all during development
    if settings.PGFRONTEND_URL:
        allow_origins = [settings.PGFRONTEND_URL]
    else:
        allow_origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth_router.router, prefix="/api/auth", tags=["Auth"])
    app.include_router(users_router.router, prefix="/api/users", tags=["Users"])
    app.include_router(kyc_router.router, prefix="/api/kyc", tags=["KYC"])
    app.include_router(admin_router.router, prefix="/api/admin", tags=["Admin"])

    # Health check
    @app.get(settings.PGHEALTHCHECK_PATH, summary="Health Check", tags=["System"])
    def health_check():
        """
        Simple health-check endpoint.
        Returns basic information on service status.
        """
        return {"status": "ok", "service": "ekyc-backend", "environment": settings.PGNODE_ENV}

    # WebSocket usage help (even if we don't define a WS endpoint now, document placeholder)
    websocket_usage_help_route(app)

    # Startup events
    @app.on_event("startup")
    async def on_startup():
        # initialize database and create tables
        init_db()
        # ensure default admin user exists (for initial access)
        create_default_admin_if_missing()

    # Custom OpenAPI generation hook to include metadata consistently
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
            tags=openapi_tags,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore

    return app


app = create_app()

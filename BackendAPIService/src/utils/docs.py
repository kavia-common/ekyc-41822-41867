from fastapi import FastAPI

openapi_tags = [
    {"name": "Auth", "description": "Authentication and authorization endpoints"},
    {"name": "Users", "description": "User management endpoints"},
    {"name": "KYC", "description": "KYC case management endpoints"},
    {"name": "Admin", "description": "Administrative operations"},
    {"name": "System", "description": "System-level endpoints"},
    {"name": "WebSocket", "description": "Real-time communication (documentation)"},
]


def websocket_usage_help_route(app: FastAPI) -> None:
    @app.get(
        "/api/websocket-info",
        tags=["WebSocket"],
        summary="WebSocket usage info",
        description="Provides documentation on WebSocket endpoints (if enabled in this deployment).",
        operation_id="websocket_usage_info",
    )
    def ws_info():
        return {
            "note": "WebSocket endpoints are not enabled in this reference deployment. If enabled, they would be documented here with connection URL and subscription topics.",
            "status": "disabled",
        }

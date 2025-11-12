"""
FastAPI Security Testing API

This is the main entry point for the FastAPI application.
It sets up the API with security testing endpoints and JWT authentication.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

from auth.routes import router as auth_router
from app.api.v1.security import router as security_router

# Create FastAPI app
app = FastAPI(
    title="Security Testing API",
    description="FastAPI application with security testing endpoints and JWT authentication",
    version="1.0.0",
    docs_url=None,  # Disable default docs URL
    redoc_url=None,  # Disable default redoc URL
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, tags=["auth"])
app.include_router(security_router, tags=["security"])


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    Custom Swagger UI endpoint.
    
    Returns:
        Swagger UI HTML
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint to check if the API is running.
    
    Returns:
        Dictionary with a welcome message
    """
    return {
        "message": "Welcome to Security Testing API",
        "docs_url": "/docs",
        "endpoints": {
            "security_testing": "/api/v1/security-testing"
        }
    }


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

"""
FastAPI JWT Authentication API

This is the main entry point for the FastAPI application.
It sets up the API with JWT authentication using access and refresh tokens.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.routes import router as auth_router

# Create FastAPI app
app = FastAPI(
    title="FastAPI JWT Auth",
    description="FastAPI application with JWT authentication",
    version="1.0.0"
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


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint to check if the API is running.
    
    Returns:
        Dictionary with a welcome message
    """
    return {
        "message": "Welcome to FastAPI JWT Auth API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


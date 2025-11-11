"""
Configuration settings for the FastAPI application.
Contains JWT token settings and secrets.
"""
from datetime import timedelta

# JWT Settings
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # In production, use a secure random key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 days

# Convert refresh token expiry to minutes for consistency
REFRESH_TOKEN_EXPIRE_MINUTES = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60

# Token type
TOKEN_TYPE = "bearer"


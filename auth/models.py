"""
Pydantic models for request and response validation.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user model with common attributes."""
    username: str
    email: str
    role: str


class UserInDB(UserBase):
    """User model as stored in the mock database."""
    id: str
    password: str


class User(UserBase):
    """User model for API responses (excludes password)."""
    id: str


class UserLogin(BaseModel):
    """Model for login request validation."""
    username: str
    password: str


class Token(BaseModel):
    """Model for token response."""
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Model for token payload validation."""
    sub: str  # User ID
    exp: int  # Expiration time
    type: str  # Token type (access or refresh)


class RefreshToken(BaseModel):
    """Model for refresh token request validation."""
    refresh_token: str


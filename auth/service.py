"""
User and token service logic.
"""
from typing import Optional, Dict, List, Any
from fastapi import HTTPException, status

from auth.models import User, UserInDB
from auth.jwt_helper import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token_type
)
from config import TOKEN_TYPE

# Mock user database (in-memory storage)
USERS_DB = [
    {
        "id": "aa4ed5cd-58f9-431e-9900-7a820633bc40",
        "username": "admin",
        "email": "admin@gmail.com",
        "password": "12345",
        "role": "Admin"
    },
    {
        "id": "61a87d82-db93-4622-bda2-c87c5d22b413",
        "username": "nippu",
        "email": "nipp@gmail.com",
        "password": "12345",
        "role": "User"
    }
]


def get_user_by_username(username: str) -> Optional[UserInDB]:
    """
    Get a user from the mock database by username.
    
    Args:
        username: Username to search for
        
    Returns:
        User object if found, None otherwise
    """
    for user_data in USERS_DB:
        if user_data["username"] == username:
            return UserInDB(**user_data)
    return None


def get_user_by_id(user_id: str) -> Optional[User]:
    """
    Get a user from the mock database by ID.
    
    Args:
        user_id: User ID to search for
        
    Returns:
        User object if found, None otherwise
    """
    for user_data in USERS_DB:
        if user_data["id"] == user_id:
            # Return User model (without password)
            return User(
                id=user_data["id"],
                username=user_data["username"],
                email=user_data["email"],
                role=user_data["role"]
            )
    return None


def authenticate_user(username: str, password: str) -> UserInDB:
    """
    Authenticate a user with username and password.
    
    Args:
        username: Username to authenticate
        password: Password to verify
        
    Returns:
        Authenticated user object
        
    Raises:
        HTTPException: If authentication fails
    """
    user = get_user_by_username(username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # In a real application, you would use password hashing
    # For example: if not verify_password(password, user.password):
    if password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def create_tokens_for_user(user_id: str) -> Dict[str, str]:
    """
    Create access and refresh tokens for a user.
    
    Args:
        user_id: User ID to create tokens for
        
    Returns:
        Dictionary containing access_token, refresh_token, and token_type
    """
    # Create token data
    token_data = {"sub": user_id}
    
    # Create tokens
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": TOKEN_TYPE
    }


def refresh_tokens(refresh_token: str) -> Dict[str, str]:
    """
    Refresh access and refresh tokens using a valid refresh token.
    
    Args:
        refresh_token: Valid refresh token
        
    Returns:
        Dictionary containing new access_token, refresh_token, and token_type
        
    Raises:
        HTTPException: If refresh token is invalid
    """
    # Decode and validate the refresh token
    payload = decode_token(refresh_token)
    
    # Verify it's a refresh token
    verify_token_type(payload, "refresh")
    
    # Get user ID from token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user exists
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create new tokens
    return create_tokens_for_user(user_id)


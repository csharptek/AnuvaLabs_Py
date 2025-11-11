"""
JWT token handling utilities.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import jwt, JWTError
from fastapi import HTTPException, status

from config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    TOKEN_TYPE
)


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Create a new JWT access token.
    
    Args:
        data: Dictionary containing claims to encode in the token
        
    Returns:
        Encoded JWT access token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add expiration time and token type to payload
    to_encode.update({"exp": expire, "type": "access"})
    
    # Create the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a new JWT refresh token.
    
    Args:
        data: Dictionary containing claims to encode in the token
        
    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    # Add expiration time and token type to payload
    to_encode.update({"exp": expire, "type": "refresh"})
    
    # Create the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token to decode
        
    Returns:
        Dictionary containing the decoded payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_token_type(payload: Dict[str, Any], expected_type: str) -> None:
    """
    Verify that a token is of the expected type.
    
    Args:
        payload: Decoded token payload
        expected_type: Expected token type ('access' or 'refresh')
        
    Raises:
        HTTPException: If token is not of the expected type
    """
    if payload.get("type") != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type. Expected {expected_type} token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


"""
API routes for authentication and user endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from auth.models import User, UserLogin, Token, RefreshToken
from auth.service import (
    authenticate_user,
    create_tokens_for_user,
    refresh_tokens,
    get_user_by_id
)
from auth.jwt_helper import decode_token, verify_token_type

# Create router
router = APIRouter()

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get the current authenticated user.
    
    Args:
        token: JWT access token from request
        
    Returns:
        Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Decode and validate the token
    payload = decode_token(token)
    
    # Verify it's an access token
    verify_token_type(payload, "access")
    
    # Get user ID from token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and return access and refresh tokens.
    
    Args:
        form_data: OAuth2 password request form
        
    Returns:
        Token object with access_token, refresh_token, and token_type
    """
    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password)
    
    # Create tokens
    tokens = create_tokens_for_user(user.id)
    
    return Token(**tokens)


@router.post("/login/json", response_model=Token)
async def login_json(user_data: UserLogin):
    """
    Alternative login endpoint that accepts JSON instead of form data.
    
    Args:
        user_data: User login data
        
    Returns:
        Token object with access_token, refresh_token, and token_type
    """
    # Authenticate user
    user = authenticate_user(user_data.username, user_data.password)
    
    # Create tokens
    tokens = create_tokens_for_user(user.id)
    
    return Token(**tokens)


@router.post("/refresh-token", response_model=Token)
async def refresh_token(refresh_token_data: RefreshToken):
    """
    Refresh access and refresh tokens.
    
    Args:
        refresh_token_data: Refresh token data
        
    Returns:
        Token object with new access_token, refresh_token, and token_type
    """
    # Refresh tokens
    tokens = refresh_tokens(refresh_token_data.refresh_token)
    
    return Token(**tokens)


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current user details.
    
    Args:
        current_user: Current authenticated user (from dependency)
        
    Returns:
        User object with user details
    """
    return current_user


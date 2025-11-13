# Security Testing API - Architecture Documentation

## Overview

This document provides a comprehensive architecture overview of the Security Testing API, a FastAPI-based application that combines JWT authentication with security testing capabilities for uploaded ZIP files.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Security Testing API                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐                          ┌─────────────────────┐   │
│  │   Client Apps   │                          │    Swagger UI       │   │
│  │                 │                          │    Documentation    │   │
│  └────────┬────────┘                          └──────────┬──────────┘   │
│           │                                              │              │
│           ▼                                              ▼              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                       FastAPI Application                        │   │
│  │                                                                  │   │
│  │  ┌────────────────────────┐      ┌───────────────────────────┐  │   │
│  │  │                        │      │                           │  │   │
│  │  │   Authentication API   │      │   Security Testing API    │  │   │
│  │  │   (auth_router)        │      │   (security_router)       │  │   │
│  │  │                        │      │                           │  │   │
│  │  └───────────┬────────────┘      └─────────────┬─────────────┘  │   │
│  │              │                                  │                │   │
│  └──────────────┼──────────────────────────────────┼────────────────┘   │
│                 │                                  │                     │
│  ┌──────────────┼──────────────────────────────────┼────────────────┐   │
│  │              │           Service Layer          │                │   │
│  │              ▼                                  ▼                │   │
│  │  ┌────────────────────────┐      ┌───────────────────────────┐  │   │
│  │  │                        │      │                           │  │   │
│  │  │   Authentication       │      │   Security Testing        │  │   │
│  │  │   Service              │      │   Service                 │  │   │
│  │  │                        │      │                           │  │   │
│  │  └───────────┬────────────┘      └─────────────┬─────────────┘  │   │
│  │              │                                  │                │   │
│  └──────────────┼──────────────────────────────────┼────────────────┘   │
│                 │                                  │                     │
│  ┌──────────────┼──────────────────────────────────┼────────────────┐   │
│  │              │            Data Layer            │                │   │
│  │              ▼                                  ▼                │   │
│  │  ┌────────────────────────┐      ┌───────────────────────────┐  │   │
│  │  │                        │      │                           │  │   │
│  │  │   User Models &        │      │   Security Models &       │  │   │
│  │  │   Mock Database        │      │   Vulnerability Data      │  │   │
│  │  │                        │      │                           │  │   │
│  │  └────────────────────────┘      └───────────────────────────┘  │   │
│  │                                                                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## API Endpoints

### Authentication Endpoints

| Endpoint | Method | Description | Input | Output |
|----------|--------|-------------|-------|--------|
| `/login` | POST | Authenticate user and get tokens | `UserLogin` (username, password) | `Token` (access_token, refresh_token, token_type) |
| `/refresh-token` | POST | Refresh expired tokens | `RefreshToken` (refresh_token) | `Token` (access_token, refresh_token, token_type) |
| `/me` | GET | Get current user info | Bearer Token (Header) | `User` (id, username, email, role) |

### Security Testing Endpoints

| Endpoint | Method | Description | Input | Output |
|----------|--------|-------------|-------|--------|
| `/api/v1/security-testing` | POST | Upload and scan ZIP file | ZIP File (multipart/form-data) | `ScanResponse` (status, file_count, vulnerabilities) |
| `/` | GET | Root endpoint | None | Welcome message and API info |
| `/docs` | GET | API documentation | None | Swagger UI HTML |

## Authentication Flow

```
┌─────────┐                                  ┌─────────────────┐                                ┌─────────────────┐
│ Client  │                                  │  Auth Router    │                                │  Auth Service   │
└────┬────┘                                  └────────┬────────┘                                └────────┬────────┘
     │                                               │                                                   │
     │ POST /login {username, password}              │                                                   │
     │─────────────────────────────────────────────>│                                                   │
     │                                               │                                                   │
     │                                               │ authenticate_user(username, password)             │
     │                                               │─────────────────────────────────────────────────>│
     │                                               │                                                   │
     │                                               │                                                   │ Verify credentials
     │                                               │                                                   │ against USERS_DB
     │                                               │                                                   │
     │                                               │ UserInDB or HTTPException                         │
     │                                               │<─────────────────────────────────────────────────│
     │                                               │                                                   │
     │                                               │ create_tokens_for_user(user.id)                   │
     │                                               │─────────────────────────────────────────────────>│
     │                                               │                                                   │
     │                                               │                                                   │ Create JWT tokens
     │                                               │                                                   │ using jwt_helper
     │                                               │                                                   │
     │                                               │ {access_token, refresh_token, token_type}         │
     │                                               │<─────────────────────────────────────────────────│
     │                                               │                                                   │
     │ 200 OK: Token object                          │                                                   │
     │<─────────────────────────────────────────────│                                                   │
     │                                               │                                                   │
     │ GET /me (with Bearer token in header)         │                                                   │
     │─────────────────────────────────────────────>│                                                   │
     │                                               │                                                   │
     │                                               │ get_current_user(token)                           │
     │                                               │─────────────────────────────────────────────────>│
     │                                               │                                                   │
     │                                               │                                                   │ Decode & validate token
     │                                               │                                                   │ Get user from USERS_DB
     │                                               │                                                   │
     │                                               │ User or HTTPException                             │
     │                                               │<─────────────────────────────────────────────────│
     │                                               │                                                   │
     │ 200 OK: User object                           │                                                   │
     │<─────────────────────────────────────────────│                                                   │
     │                                               │                                                   │
     │ POST /refresh-token {refresh_token}           │                                                   │
     │─────────────────────────────────────────────>│                                                   │
     │                                               │                                                   │
     │                                               │ refresh_tokens(refresh_token)                     │
     │                                               │─────────────────────────────────────────────────>│
     │                                               │                                                   │
     │                                               │                                                   │ Decode & validate token
     │                                               │                                                   │ Verify token type
     │                                               │                                                   │ Create new tokens
     │                                               │                                                   │
     │                                               │ {access_token, refresh_token, token_type}         │
     │                                               │<─────────────────────────────────────────────────│
     │                                               │                                                   │
     │ 200 OK: Token object                          │                                                   │
     │<─────────────────────────────────────────────│                                                   │
     │                                               │                                                   │
```

## Security Testing Flow

```
┌─────────┐                                  ┌─────────────────┐                                ┌─────────────────┐
│ Client  │                                  │ Security Router │                                │ Security Service│
└────┬────┘                                  └────────┬────────┘                                └────────┬────────┘
     │                                               │                                                   │
     │ POST /api/v1/security-testing                 │                                                   │
     │ (with ZIP file as multipart/form-data)        │                                                   │
     │─────────────────────────────────────────────>│                                                   │
     │                                               │                                                   │
     │                                               │ Validate file is ZIP                              │
     │                                               │                                                   │
     │                                               │ Read file content                                 │
     │                                               │                                                   │
     │                                               │ process_zip_file(file_content)                    │
     │                                               │─────────────────────────────────────────────────>│
     │                                               │                                                   │
     │                                               │                                                   │ Create temp directory
     │                                               │                                                   │ Extract ZIP contents
     │                                               │                                                   │ Process each file
     │                                               │                                                   │ Generate mock issues
     │                                               │                                                   │
     │                                               │ ScanResponse                                      │
     │                                               │<─────────────────────────────────────────────────│
     │                                               │                                                   │
     │ 200 OK: ScanResponse                          │                                                   │
     │ (status, file_count, vulnerabilities)         │                                                   │
     │<─────────────────────────────────────────────│                                                   │
     │                                               │                                                   │
```

## Data Models

### Authentication Models

```python
# User Models
class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserInDB(UserBase):
    id: str
    password: str

class User(UserBase):
    id: str

class UserLogin(BaseModel):
    username: str
    password: str

# Token Models
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str  # User ID
    exp: int  # Expiration time
    type: str  # Token type (access or refresh)

class RefreshToken(BaseModel):
    refresh_token: str
```

### Security Testing Models

```python
class VulnerabilityItem(BaseModel):
    file: str
    issues: List[str]

class ScanResponse(BaseModel):
    status: str = "success"
    file_count: int
    vulnerabilities: List[VulnerabilityItem]

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    details: Optional[Dict[str, Any]] = None
```

## Component Dependencies

```
┌─────────────────────────────────────────────────────────────────────────┐
│                             FastAPI App (main.py)                       │
└───────────────┬─────────────────────────────────────┬─────────────────────┘
                │                                     │
                ▼                                     ▼
┌───────────────────────────┐             ┌───────────────────────────┐
│    Auth Router            │             │    Security Router        │
│    (auth/routes.py)       │             │    (app/api/v1/security.py)│
└───────────┬───────────────┘             └───────────┬───────────────┘
            │                                         │
            ▼                                         ▼
┌───────────────────────────┐             ┌───────────────────────────┐
│    Auth Service           │             │    Security Service       │
│    (auth/service.py)      │             │    (app/services/security_service.py)│
└───────────┬───────────────┘             └───────────┬───────────────┘
            │                                         │
            ▼                                         ▼
┌───────────────────────────┐             ┌───────────────────────────┐
│    JWT Helper             │             │    Security Models        │
│    (auth/jwt_helper.py)   │             │    (app/models/security.py)│
└───────────┬───────────────┘             └───────────────────────────┘
            │
            ▼
┌───────────────────────────┐
│    Auth Models            │
│    (auth/models.py)       │
└───────────────────────────┘
```

## File Structure

```
AnuvaLabs_Py/
├── main.py                     # FastAPI application entry point
├── config.py                   # Configuration settings
├── test_api.py                 # API testing script
├── auth/                       # Authentication module
│   ├── __init__.py
│   ├── routes.py              # Authentication endpoints
│   ├── service.py             # Authentication business logic
│   ├── models.py              # Authentication data models
│   └── jwt_helper.py          # JWT token utilities
└── app/                       # Application module
    ├── __init__.py
    ├── api/                   # API routes
    │   ├── __init__.py
    │   └── v1/
    │       ├── __init__.py
    │       └── security.py    # Security testing endpoints
    ├── models/                # Data models
    │   ├── __init__.py
    │   └── security.py        # Security testing models
    └── services/              # Business logic services
        ├── __init__.py
        └── security_service.py # Security testing logic
```

## Key Features

### 1. JWT Authentication
- **Access Tokens**: Short-lived tokens (60 minutes) for API access
- **Refresh Tokens**: Long-lived tokens (7 days) for token renewal
- **Token Validation**: Proper validation of token type and expiration
- **User Management**: Mock in-memory user database with role-based access

### 2. Security Testing
- **File Upload**: Accepts ZIP files via multipart/form-data
- **File Processing**: Extracts and analyzes files from uploaded ZIP
- **Vulnerability Detection**: Mock security scanning with predefined vulnerability patterns
- **Report Generation**: Structured response with vulnerability details

### 3. API Documentation
- **Swagger UI**: Interactive API documentation at `/docs`
- **OpenAPI Schema**: Auto-generated API schema
- **Response Models**: Structured response validation

## Security Considerations

### Current Implementation
1. **JWT Security**: Proper token validation and type checking
2. **CORS Configuration**: Cross-origin request handling
3. **File Validation**: ZIP file format validation
4. **Error Handling**: Structured error responses
5. **Temporary File Handling**: Secure cleanup of uploaded files

### Production Recommendations
1. **Password Hashing**: Replace plain text passwords with bcrypt/scrypt
2. **Database Integration**: Replace mock database with PostgreSQL/MongoDB
3. **Rate Limiting**: Implement request rate limiting
4. **Real Security Scanning**: Integrate with actual security scanning tools
5. **Environment Variables**: Move secrets to environment configuration
6. **Logging**: Implement comprehensive audit logging
7. **Input Validation**: Enhanced file type and content validation

## Configuration

### JWT Settings (config.py)
```python
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7
TOKEN_TYPE = "bearer"
```

### Mock Users Database
```python
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
```

## API Usage Examples

### Authentication Flow
```bash
# 1. Login
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "12345"}'

# Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}

# 2. Access protected endpoint
curl -X GET "http://localhost:8000/me" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 3. Refresh token
curl -X POST "http://localhost:8000/refresh-token" \
     -H "Content-Type: application/json" \
     -d '{"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}'
```

### Security Testing Flow
```bash
# Upload ZIP file for security testing
curl -X POST "http://localhost:8000/api/v1/security-testing" \
     -F "file=@test.zip"

# Response:
{
  "status": "success",
  "file_count": 3,
  "vulnerabilities": [
    {
      "file": "app.py",
      "issues": ["Hardcoded password", "Debug mode enabled"]
    },
    {
      "file": "config.js",
      "issues": ["Insecure configuration"]
    }
  ]
}
```

## Development Setup

### Prerequisites
- Python 3.8+
- FastAPI
- python-jose[cryptography]
- python-multipart
- uvicorn

### Installation
```bash
pip install fastapi uvicorn python-jose[cryptography] python-multipart

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing
```bash
# Run the test script
python test_api.py
```

## Future Enhancements

1. **Database Integration**: PostgreSQL/MongoDB for persistent storage
2. **Real Security Scanning**: Integration with SAST/DAST tools
3. **User Management**: Registration, password reset, email verification
4. **Role-Based Access Control**: Fine-grained permissions
5. **Audit Logging**: Comprehensive security event logging
6. **File Type Support**: Support for additional file formats
7. **Async Processing**: Background job processing for large files
8. **Caching**: Redis integration for session management
9. **Monitoring**: Health checks and metrics collection
10. **Containerization**: Docker support for deployment

This architecture provides a solid foundation for a security testing API with proper authentication, file processing, and extensible design patterns.


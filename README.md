# FastAPI JWT Authentication API

A FastAPI REST API project with JWT authentication using access tokens and refresh tokens.

## Features

- User authentication using JWT access tokens and refresh tokens
- Mock user data stored in memory (no database required)
- Protected routes that require valid JWT access tokens
- Token refresh functionality

## Project Structure

```
├── main.py                 # Entry point
├── config.py               # Token settings and secrets
├── auth/
│   ├── __init__.py         # Package initialization
│   ├── models.py           # Pydantic models
│   ├── service.py          # User and token logic
│   ├── jwt_helper.py       # JWT handling
│   └── routes.py           # API routes
└── requirements.txt        # Dependencies
```

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Run the application with uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

- `POST /login`: Authenticate with username and password (JSON format) to get tokens
- `POST /refresh-token`: Refresh access and refresh tokens
- `GET /me`: Get current user details (protected route)

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Sample Users

The application comes with two pre-configured users:

1. Admin User:
   - Username: admin
   - Password: 12345
   - Role: Admin

2. Regular User:
   - Username: nippu
   - Password: 12345
   - Role: User

## Token Settings

- Access token expiry: 1 hour
- Refresh token expiry: 7 days

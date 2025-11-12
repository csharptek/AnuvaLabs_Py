# Security Testing API

A FastAPI application with security testing endpoints and JWT authentication.

## Features

- **Security Testing**: Upload ZIP files for mock vulnerability scanning
- **JWT Authentication**: Secure API access with JWT tokens

## API Endpoints

### Security Testing Endpoints

1. **POST /api/v1/security-testing/**
   - Accepts a ZIP file upload (form-data key: "file")
   - Extracts files from the ZIP and returns mock vulnerability scan results
   - Example response:
     ```json
     {
       "status": "success",
       "file_count": 3,
       "vulnerabilities": [
         {"file": "main.py", "issues": ["Hardcoded password", "Debug mode enabled"]},
         {"file": "config.json", "issues": ["Sensitive data exposure"]},
         {"file": "app.js", "issues": []}
       ]
     }
     ```

### Authentication Endpoints

1. **POST /login**
   - Authenticate user and get access and refresh tokens
   - Request body: `{"username": "user", "password": "password"}`

2. **POST /refresh-token**
   - Refresh access token using refresh token
   - Request body: `{"refresh_token": "your-refresh-token"}`

3. **GET /me**
   - Get current user details (requires authentication)

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/security-testing-api.git
   cd security-testing-api
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. Access the API documentation:
   - Open your browser and navigate to http://localhost:8000/docs

## Testing the API

### Security Testing Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/security-testing \
  -F "file=@/path/to/your/file.zip" \
  -H "Content-Type: multipart/form-data"
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

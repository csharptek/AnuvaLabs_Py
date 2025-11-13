# API Flow Diagrams

This document contains detailed flow diagrams for the Security Testing API system.

## 1. Complete System Flow Overview

```mermaid
graph TB
    Client[Client Application]
    SwaggerUI[Swagger UI]
    FastAPI[FastAPI Application]
    
    AuthRouter[Authentication Router]
    SecurityRouter[Security Testing Router]
    
    AuthService[Authentication Service]
    SecurityService[Security Testing Service]
    
    JWTHelper[JWT Helper]
    UserDB[(Mock User Database)]
    TempFiles[(Temporary Files)]
    
    Client --> FastAPI
    SwaggerUI --> FastAPI
    
    FastAPI --> AuthRouter
    FastAPI --> SecurityRouter
    
    AuthRouter --> AuthService
    SecurityRouter --> SecurityService
    
    AuthService --> JWTHelper
    AuthService --> UserDB
    SecurityService --> TempFiles
    
    style Client fill:#e1f5fe
    style FastAPI fill:#f3e5f5
    style AuthService fill:#e8f5e8
    style SecurityService fill:#fff3e0
    style UserDB fill:#fce4ec
    style TempFiles fill:#f1f8e9
```

## 2. Authentication Flow Sequence

```mermaid
sequenceDiagram
    participant C as Client
    participant AR as Auth Router
    participant AS as Auth Service
    participant JWT as JWT Helper
    participant DB as User Database

    Note over C,DB: Login Process
    C->>AR: POST /login {username, password}
    AR->>AS: authenticate_user(username, password)
    AS->>DB: get_user_by_username(username)
    DB-->>AS: UserInDB or None
    AS->>AS: verify_password(password)
    AS-->>AR: UserInDB or HTTPException
    AR->>AS: create_tokens_for_user(user.id)
    AS->>JWT: create_access_token(data)
    AS->>JWT: create_refresh_token(data)
    JWT-->>AS: access_token, refresh_token
    AS-->>AR: {access_token, refresh_token, token_type}
    AR-->>C: 200 OK: Token object

    Note over C,DB: Get User Info
    C->>AR: GET /me (Bearer token)
    AR->>AS: get_current_user(token)
    AS->>JWT: decode_token(token)
    JWT-->>AS: payload or HTTPException
    AS->>JWT: verify_token_type(payload, "access")
    AS->>DB: get_user_by_id(user_id)
    DB-->>AS: User or None
    AS-->>AR: User or HTTPException
    AR-->>C: 200 OK: User object

    Note over C,DB: Token Refresh
    C->>AR: POST /refresh-token {refresh_token}
    AR->>AS: refresh_tokens(refresh_token)
    AS->>JWT: decode_token(refresh_token)
    JWT-->>AS: payload or HTTPException
    AS->>JWT: verify_token_type(payload, "refresh")
    AS->>DB: get_user_by_id(user_id)
    DB-->>AS: User or None
    AS->>AS: create_tokens_for_user(user_id)
    AS-->>AR: {access_token, refresh_token, token_type}
    AR-->>C: 200 OK: Token object
```

## 3. Security Testing Flow Sequence

```mermaid
sequenceDiagram
    participant C as Client
    participant SR as Security Router
    participant SS as Security Service
    participant FS as File System
    participant ZIP as ZIP Handler

    Note over C,ZIP: File Upload and Processing
    C->>SR: POST /api/v1/security-testing (ZIP file)
    SR->>SR: validate_file_type(filename)
    SR->>SR: read_file_content()
    SR->>SS: process_zip_file(file_content)
    
    SS->>FS: create_temporary_directory()
    SS->>FS: write_temp_file(content)
    SS->>ZIP: is_zipfile(temp_file)
    ZIP-->>SS: True or False
    
    alt Valid ZIP file
        SS->>ZIP: extract_all(temp_dir)
        SS->>ZIP: get_namelist()
        ZIP-->>SS: file_list
        
        loop For each file
            SS->>SS: generate_mock_issues(filename)
            SS->>SS: create_vulnerability_item(file, issues)
        end
        
        SS->>FS: cleanup_temp_directory()
        SS-->>SR: ScanResponse{status, file_count, vulnerabilities}
        SR-->>C: 200 OK: ScanResponse
    else Invalid ZIP file
        SS->>FS: cleanup_temp_directory()
        SS-->>SR: ValueError("Invalid ZIP file")
        SR-->>C: 400 Bad Request: ErrorResponse
    end
```

## 4. JWT Token Lifecycle

```mermaid
stateDiagram-v2
    [*] --> LoginRequest
    LoginRequest --> TokenValidation: Validate Credentials
    TokenValidation --> TokenCreation: Valid User
    TokenValidation --> LoginFailed: Invalid User
    
    TokenCreation --> AccessToken: Create Access Token (60 min)
    TokenCreation --> RefreshToken: Create Refresh Token (7 days)
    
    AccessToken --> TokenActive: Token Valid
    RefreshToken --> TokenActive: Token Valid
    
    TokenActive --> TokenExpired: Time Expires
    TokenActive --> APIAccess: Use for API Calls
    
    TokenExpired --> RefreshProcess: Use Refresh Token
    TokenExpired --> LoginRequired: Refresh Token Expired
    
    RefreshProcess --> TokenCreation: Valid Refresh Token
    RefreshProcess --> LoginRequired: Invalid Refresh Token
    
    APIAccess --> TokenActive: Continue Using
    LoginFailed --> [*]
    LoginRequired --> [*]
```

## 5. File Processing Pipeline

```mermaid
flowchart TD
    A[Client Uploads ZIP File] --> B{File Extension Check}
    B -->|Not .zip| C[Return 400 Error]
    B -->|Is .zip| D[Read File Content]
    
    D --> E[Create Temporary Directory]
    E --> F{Valid ZIP File?}
    F -->|No| G[Return 400 Error]
    F -->|Yes| H[Extract ZIP Contents]
    
    H --> I[Get File List]
    I --> J[Process Each File]
    
    J --> K{File Type?}
    K -->|.py| L[Python Vulnerabilities]
    K -->|.js| M[JavaScript Vulnerabilities]
    K -->|.json| N[JSON Vulnerabilities]
    K -->|.html| O[HTML Vulnerabilities]
    K -->|.php| P[PHP Vulnerabilities]
    K -->|.java| Q[Java Vulnerabilities]
    K -->|Other| R[Generic Vulnerabilities]
    
    L --> S[Generate Mock Issues]
    M --> S
    N --> S
    O --> S
    P --> S
    Q --> S
    R --> S
    
    S --> T{More Files?}
    T -->|Yes| J
    T -->|No| U[Cleanup Temp Directory]
    
    U --> V[Return Scan Results]
    
    C --> W[End]
    G --> W
    V --> W
    
    style A fill:#e3f2fd
    style V fill:#e8f5e8
    style C fill:#ffebee
    style G fill:#ffebee
```

## 6. Error Handling Flow

```mermaid
flowchart TD
    A[API Request] --> B{Authentication Required?}
    B -->|Yes| C{Valid Token?}
    B -->|No| D[Process Request]
    
    C -->|No| E[401 Unauthorized]
    C -->|Yes| F{Token Type Correct?}
    
    F -->|No| G[401 Invalid Token Type]
    F -->|Yes| H{User Exists?}
    
    H -->|No| I[401 User Not Found]
    H -->|Yes| D
    
    D --> J{Request Valid?}
    J -->|No| K[400 Bad Request]
    J -->|Yes| L[Process Business Logic]
    
    L --> M{Processing Successful?}
    M -->|No| N{Error Type?}
    M -->|Yes| O[200 Success Response]
    
    N -->|Validation Error| P[400 Bad Request]
    N -->|Server Error| Q[500 Internal Server Error]
    
    E --> R[Return Error Response]
    G --> R
    I --> R
    K --> R
    P --> R
    Q --> R
    O --> S[Return Success Response]
    
    R --> T[End]
    S --> T
    
    style O fill:#e8f5e8
    style E fill:#ffebee
    style G fill:#ffebee
    style I fill:#ffebee
    style K fill:#ffebee
    style P fill:#ffebee
    style Q fill:#ffebee
```

## 7. Data Model Relationships

```mermaid
erDiagram
    UserBase {
        string username
        string email
        string role
    }
    
    UserInDB {
        string id
        string password
    }
    
    User {
        string id
    }
    
    UserLogin {
        string username
        string password
    }
    
    Token {
        string access_token
        string refresh_token
        string token_type
    }
    
    TokenPayload {
        string sub
        int exp
        string type
    }
    
    RefreshToken {
        string refresh_token
    }
    
    ScanResponse {
        string status
        int file_count
    }
    
    VulnerabilityItem {
        string file
        array issues
    }
    
    ErrorResponse {
        string status
        string message
        object details
    }
    
    UserBase ||--|| UserInDB : extends
    UserBase ||--|| User : extends
    ScanResponse ||--o{ VulnerabilityItem : contains
```

## 8. Component Interaction Matrix

| Component | Auth Router | Security Router | Auth Service | Security Service | JWT Helper | Models |
|-----------|-------------|-----------------|--------------|------------------|------------|--------|
| **Auth Router** | - | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Security Router** | ❌ | - | ❌ | ✅ | ❌ | ✅ |
| **Auth Service** | ✅ | ❌ | - | ❌ | ✅ | ✅ |
| **Security Service** | ❌ | ✅ | ❌ | - | ❌ | ✅ |
| **JWT Helper** | ✅ | ❌ | ✅ | ❌ | - | ✅ |
| **Models** | ✅ | ✅ | ✅ | ✅ | ✅ | - |

Legend:
- ✅ Direct interaction/dependency
- ❌ No direct interaction
- - Self reference

## 9. Security Vulnerability Detection Logic

```mermaid
flowchart TD
    A[File Extracted] --> B{Get File Extension}
    
    B --> C{Extension Type?}
    C -->|.py| D[Python Issues Pool]
    C -->|.js| E[JavaScript Issues Pool]
    C -->|.json| F[JSON Issues Pool]
    C -->|.html| G[HTML Issues Pool]
    C -->|.php| H[PHP Issues Pool]
    C -->|.java| I[Java Issues Pool]
    C -->|Other| J[Generic Issues Pool]
    
    D --> K[Hardcoded password<br/>Debug mode enabled<br/>Insecure random<br/>SQL injection<br/>Command injection]
    E --> L[XSS vulnerability<br/>Insecure eval()<br/>Prototype pollution<br/>Insecure JWT]
    F --> M[Sensitive data exposure<br/>Insecure configuration]
    G --> N[XSS vulnerability<br/>Insecure CSP]
    H --> O[SQL injection<br/>Remote file inclusion<br/>Insecure file upload]
    I --> P[Insecure deserialization<br/>XXE vulnerability<br/>Path traversal]
    J --> Q[Unknown vulnerability]
    
    K --> R{Random Check<br/>70% chance}
    L --> R
    M --> R
    N --> R
    O --> R
    P --> R
    Q --> R
    
    R -->|Has Issues| S[Select 1-3 Random Issues]
    R -->|No Issues| T[Return Empty List]
    
    S --> U[Return Issue List]
    T --> V[File Clean]
    
    U --> W[Add to Vulnerability Report]
    V --> W
    
    style K fill:#ffcdd2
    style L fill:#ffcdd2
    style M fill:#ffcdd2
    style N fill:#ffcdd2
    style O fill:#ffcdd2
    style P fill:#ffcdd2
    style Q fill:#ffcdd2
    style V fill:#c8e6c9
```

## 10. API Response Flow

```mermaid
flowchart TD
    A[API Endpoint Called] --> B{Endpoint Type?}
    
    B -->|Authentication| C[Auth Response Flow]
    B -->|Security Testing| D[Security Response Flow]
    B -->|Root/Docs| E[Info Response Flow]
    
    C --> F{Auth Operation?}
    F -->|Login| G[Return Token Object]
    F -->|Refresh| H[Return New Token Object]
    F -->|Get User| I[Return User Object]
    
    D --> J{File Processing?}
    J -->|Success| K[Return ScanResponse]
    J -->|Error| L[Return ErrorResponse]
    
    E --> M[Return Welcome/Docs]
    
    G --> N[HTTP 200 + Token JSON]
    H --> N
    I --> O[HTTP 200 + User JSON]
    K --> P[HTTP 200 + Scan Results JSON]
    L --> Q{Error Type?}
    M --> R[HTTP 200 + Info JSON]
    
    Q -->|Validation| S[HTTP 400 + Error JSON]
    Q -->|Server Error| T[HTTP 500 + Error JSON]
    Q -->|Auth Error| U[HTTP 401 + Error JSON]
    
    N --> V[Client Receives Response]
    O --> V
    P --> V
    R --> V
    S --> V
    T --> V
    U --> V
    
    style N fill:#c8e6c9
    style O fill:#c8e6c9
    style P fill:#c8e6c9
    style R fill:#c8e6c9
    style S fill:#ffcdd2
    style T fill:#ffcdd2
    style U fill:#ffcdd2
```

These diagrams provide a comprehensive visual representation of how the Security Testing API system works, from high-level architecture to detailed process flows.


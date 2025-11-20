# Security Scanner API

This is a FastAPI-based security scanning API that accepts ZIP file uploads and performs comprehensive security analysis using multiple tools.

## Features

- Accepts `.zip` file uploads containing source code
- Safely extracts files (prevents zip-slip attacks)
- Detects project type (Python/Docker/Generic)
- Runs multiple security scanning tools:
  - Bandit (Python security scanner)
  - Semgrep (Multi-language static analysis)
  - pip-audit (Python dependency vulnerability scanner)
  - Gitleaks (Secret detection)
  - Ruff (Python linter)
- Transforms all tool outputs into a unified vulnerability format
- Returns a comprehensive JSON response with all findings

## Unified Vulnerability Format

All findings from all tools are mapped to this consistent format:

```json
{
  "name": "",
  "file": "",
  "lines": "",
  "severity": "",
  "impact": "",
  "exploitable": true,
  "cvssScore": 0.0,
  "description": "",
  "cve": null,
  "recommendation": "",
  "codeSnippet": "",
  "fix": ""
}
```

## API Endpoint

### POST /security-testing

**Request:**
- Content-Type: multipart/form-data
- Body: ZIP file upload (form field: "file")

**Response:**
```json
{
  "scanId": "uuid",
  "projectType": "python|docker|generic",
  "vulnerabilities": [
    {
      "name": "Tool: Rule ID",
      "file": "path/to/file.py",
      "lines": "10-15",
      "severity": "LOW|MEDIUM|HIGH",
      "impact": "Description of impact",
      "exploitable": true,
      "cvssScore": 7.5,
      "description": "Detailed description",
      "cve": "CVE-2023-12345",
      "recommendation": "How to fix",
      "codeSnippet": "def vulnerable_code()...",
      "fix": "Specific fix suggestion"
    }
  ]
}
```

## Installation

1. Install required dependencies:

```bash
pip install fastapi uvicorn python-multipart

# Install security tools
pip install bandit semgrep pip-audit ruff
# Install gitleaks (requires Go)
```

2. Run the server:

```bash
uvicorn security_scanner:app --host 0.0.0.0 --port 8000 --reload
```

## Example Usage

```bash
# Create a ZIP file of your project
zip -r myproject.zip /path/to/your/project

# Send the ZIP file to the API
curl -X POST "http://localhost:8000/security-testing" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@myproject.zip"
```

## Implementation Details

The scanner includes several helper functions:
- `run_cmd()`: Executes shell commands safely
- `safe_extract_zip()`: Prevents zip-slip attacks
- `detect_project_type()`: Identifies the project type
- Tool-specific mappers that transform each tool's output to the unified format:
  - `map_bandit_issue()`
  - `map_semgrep_issue()`
  - `map_gitleaks_issue()`
  - `map_pip_audit_issue()`
  - `map_ruff_issue()`

## Security Considerations

- ZIP files are extracted safely to prevent zip-slip attacks
- Secrets detected in code are redacted in the response
- Temporary files are cleaned up after processing
- Command execution is done with proper timeouts and error handling


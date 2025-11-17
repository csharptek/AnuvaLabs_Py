"""
Service layer for security testing functionality.
"""
import os
import tempfile
import zipfile
import random
from datetime import date, timedelta
from typing import List, Dict, Any

from app.models.security import VulnerabilityDetail


def process_zip_file(file_content: bytes) -> Dict[str, Any]:
    """
    Process a ZIP file and generate mock vulnerability scan results.
    
    Args:
        file_content: Content of the uploaded ZIP file
        
    Returns:
        Dictionary with mock vulnerability scan results
        
    Raises:
        Exception: If the file is not a valid ZIP file
    """
    # Create a temporary directory to extract files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a temporary file to save the uploaded content
        temp_zip_path = os.path.join(temp_dir, "uploaded.zip")
        
        # Write the content to the temporary file
        with open(temp_zip_path, "wb") as temp_file:
            temp_file.write(file_content)
        
        # Check if the file is a valid ZIP file
        if not zipfile.is_zipfile(temp_zip_path):
            raise ValueError("The uploaded file is not a valid ZIP file")
        
        # Extract the ZIP file
        with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
            # Get the list of files in the ZIP
            file_list = zip_ref.namelist()
            
            # Extract all files
            zip_ref.extractall(temp_dir)
            
            # Generate mock vulnerability results for each file
            vulnerabilities = []
            for file_name in file_list:
                # Skip directories
                if file_name.endswith("/"):
                    continue
                
                # Generate detailed mock vulnerabilities based on file extension
                file_vulnerabilities = generate_detailed_vulnerabilities(file_name)
                
                # Add to vulnerabilities list
                vulnerabilities.extend(file_vulnerabilities)
    
    # Return mock scan results
    return {
        "status": "success",
        "file_count": len(file_list) - sum(1 for f in file_list if f.endswith("/")),
        "vulnerabilities": vulnerabilities
    }


def generate_detailed_vulnerabilities(file_name: str) -> List[VulnerabilityDetail]:
    """
    Generate detailed mock vulnerabilities based on file extension.
    
    Args:
        file_name: Name of the file
        
    Returns:
        List of detailed vulnerability objects
    """
    # Define vulnerability templates by file type
    vulnerability_templates = {
        ".py": [
            {
                "name": "Hardcoded Password",
                "severity": "High",
                "impact": "Credentials may be exposed in source code",
                "cvssScore": 7.4,
                "description": "The application contains hardcoded credentials in source code.",
                "recommendation": "Use environment variables or a secure vault for storing credentials.",
                "codeSnippet": "password = 'admin123'  # Hardcoded password",
                "fix": "password = os.environ.get('PASSWORD')"
            },
            {
                "name": "SQL Injection Vulnerability",
                "severity": "Critical",
                "impact": "Attackers may execute arbitrary SQL commands",
                "cvssScore": 9.1,
                "description": "User input is directly concatenated into SQL queries without proper sanitization.",
                "recommendation": "Use parameterized queries or an ORM to prevent SQL injection.",
                "codeSnippet": "query = f\"SELECT * FROM users WHERE username = '{username}'\"",
                "fix": "query = \"SELECT * FROM users WHERE username = %s\"\ncursor.execute(query, (username,))"
            },
            {
                "name": "Insecure Random Number Generation",
                "severity": "Medium",
                "impact": "Predictable random values may lead to security vulnerabilities",
                "cvssScore": 5.9,
                "description": "The application uses Python's random module for security-sensitive operations.",
                "recommendation": "Use secrets module for cryptographic operations instead of random.",
                "codeSnippet": "token = ''.join(random.choice(chars) for _ in range(length))",
                "fix": "import secrets\ntoken = ''.join(secrets.choice(chars) for _ in range(length))"
            }
        ],
        ".js": [
            {
                "name": "Cross-site Scripting (XSS) Vulnerability",
                "severity": "High",
                "impact": "Attackers may inject malicious scripts affecting other users",
                "cvssScore": 7.8,
                "description": "Unescaped user input in HTML context allows JavaScript injection.",
                "recommendation": "Use output encoding or sanitization libraries (like DOMPurify).",
                "codeSnippet": "element.innerHTML = userInput;",
                "fix": "import DOMPurify from 'dompurify';\nelement.innerHTML = DOMPurify.sanitize(userInput);"
            },
            {
                "name": "Insecure Use of eval()",
                "severity": "Critical",
                "impact": "Attackers may execute arbitrary code",
                "cvssScore": 9.6,
                "description": "The application uses eval() with user-controlled input.",
                "recommendation": "Avoid using eval() entirely. Use safer alternatives like JSON.parse() for JSON data.",
                "codeSnippet": "const result = eval(userInput);",
                "fix": "const result = JSON.parse(userInput);"
            },
            {
                "name": "Weak Cryptographic Algorithm",
                "severity": "Medium",
                "impact": "Encrypted data may be compromised",
                "cvssScore": 5.3,
                "description": "The application uses MD5 for password hashing, which is cryptographically broken.",
                "recommendation": "Use modern hashing algorithms like bcrypt, scrypt, or Argon2 for password storage.",
                "codeSnippet": "const hash = crypto.createHash('md5').update(password).digest('hex');",
                "fix": "const hash = await bcrypt.hash(password, 12);"
            }
        ],
        ".java": [
            {
                "name": "Insecure Deserialization",
                "severity": "Critical",
                "impact": "Remote code execution",
                "cvssScore": 8.8,
                "description": "The application deserializes untrusted data without proper validation.",
                "recommendation": "Implement integrity checks or use safer alternatives like JSON.",
                "codeSnippet": "ObjectInputStream in = new ObjectInputStream(inputStream);\nObject obj = in.readObject();",
                "fix": "// Use JSON instead\nObjectMapper mapper = new ObjectMapper();\nMyObject obj = mapper.readValue(jsonString, MyObject.class);"
            },
            {
                "name": "Path Traversal Vulnerability",
                "severity": "High",
                "impact": "Unauthorized access to files outside intended directory",
                "cvssScore": 7.5,
                "description": "User input is used in file paths without proper validation.",
                "recommendation": "Validate and sanitize file paths, use Path.normalize() and check against allowed directories.",
                "codeSnippet": "File file = new File(basePath + userInput);",
                "fix": "Path path = Paths.get(basePath, userInput).normalize();\nif (!path.startsWith(Paths.get(basePath))) {\n    throw new SecurityException(\"Path traversal attempt\");\n}"
            }
        ],
        ".php": [
            {
                "name": "Remote File Inclusion",
                "severity": "Critical",
                "impact": "Remote code execution",
                "cvssScore": 9.3,
                "description": "The application includes files based on user input without proper validation.",
                "recommendation": "Use whitelisting for included files and disable allow_url_include in php.ini.",
                "codeSnippet": "include($_GET['page'] . '.php');",
                "fix": "$allowed_pages = ['home', 'about', 'contact'];\nif (in_array($_GET['page'], $allowed_pages)) {\n    include($_GET['page'] . '.php');\n}"
            },
            {
                "name": "SQL Injection in PHP",
                "severity": "Critical",
                "impact": "Database compromise",
                "cvssScore": 9.1,
                "description": "User input is directly inserted into SQL queries.",
                "recommendation": "Use prepared statements with PDO or mysqli_prepare().",
                "codeSnippet": "$query = \"SELECT * FROM users WHERE username = '$username'\";",
                "fix": "$stmt = $pdo->prepare(\"SELECT * FROM users WHERE username = ?\");\n$stmt->execute([$username]);"
            }
        ],
        ".html": [
            {
                "name": "Cross-site Scripting in HTML",
                "severity": "High",
                "impact": "Session hijacking, defacement",
                "cvssScore": 7.4,
                "description": "Unescaped data is inserted into HTML without proper encoding.",
                "recommendation": "Use templating engines with automatic escaping or manually escape HTML special characters.",
                "codeSnippet": "<div id=\"message\"></div>\n<script>document.getElementById('message').innerHTML = getParameterByName('msg');</script>",
                "fix": "<div id=\"message\"></div>\n<script>\nfunction escapeHTML(str) {\n    return str.replace(/[&<>\"']/g, (m) => {\n        return {'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[m];\n    });\n}\ndocument.getElementById('message').innerHTML = escapeHTML(getParameterByName('msg'));\n</script>"
            }
        ],
        ".json": [
            {
                "name": "Sensitive Data Exposure",
                "severity": "High",
                "impact": "Credential leakage",
                "cvssScore": 7.5,
                "description": "The JSON file contains sensitive information like API keys or passwords.",
                "recommendation": "Store sensitive data in environment variables or secure vaults, not in JSON configuration files.",
                "codeSnippet": "{\n  \"api_key\": \"api_key_example_12345\",\n  \"database\": {\n    \"password\": \"db_password_123\"\n  }\n}",
                "fix": "{\n  \"api_key\": \"${API_KEY}\",\n  \"database\": {\n    \"password\": \"${DB_PASSWORD}\"\n  }\n}"
            }
        ]
    }
    
    # Get file extension
    _, ext = os.path.splitext(file_name.lower())
    
    # Get vulnerability templates for this file type
    templates = vulnerability_templates.get(ext, [])
    
    # If no templates for this extension, return empty list
    if not templates:
        return []
    
    # Randomly decide if the file has vulnerabilities (70% chance)
    if random.random() < 0.7:
        # Select a random number of vulnerabilities (0-2)
        num_vulnerabilities = random.randint(0, min(2, len(templates)))
        
        # If no vulnerabilities, return empty list
        if num_vulnerabilities == 0:
            return []
        
        # Randomly select vulnerability templates
        selected_templates = random.sample(templates, num_vulnerabilities)
        
        # Generate detailed vulnerabilities
        vulnerabilities = []
        for template in selected_templates:
            # Generate random line numbers
            start_line = random.randint(1, 50)
            end_line = start_line + random.randint(1, 10)
            lines = f"{start_line}-{end_line}"
            
            # Randomly decide if it's exploitable
            exploitable = random.choice([True, False])
            
            # Randomly decide if it has a CVE
            cve = None
            if random.random() < 0.3:  # 30% chance to have a CVE
                year = random.randint(2020, 2023)
                number = random.randint(1000, 99999)
                cve = f"CVE-{year}-{number}"
            
            # Create vulnerability detail
            vulnerability = VulnerabilityDetail(
                name=template["name"],
                file=file_name,
                lines=lines,
                severity=template["severity"],
                impact=template["impact"],
                exploitable=exploitable,
                cvssScore=template["cvssScore"],
                description=template["description"],
                cve=cve,
                recommendation=template["recommendation"],
                codeSnippet=template["codeSnippet"],
                fix=template["fix"]
            )
            
            vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    else:
        # No vulnerabilities found
        return []

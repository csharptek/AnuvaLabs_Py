"""
Service layer for security testing functionality.
"""
import os
import tempfile
import zipfile
import random
from datetime import date, timedelta
from typing import List, Dict, Any

from app.models.security import VulnerabilityItem


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
                
                # Generate mock issues based on file extension
                issues = generate_mock_issues(file_name)
                
                # Add to vulnerabilities list
                vulnerabilities.append(
                    VulnerabilityItem(
                        file=file_name,
                        issues=issues
                    )
                )
    
    # Return mock scan results
    return {
        "status": "success",
        "file_count": len(vulnerabilities),
        "vulnerabilities": vulnerabilities
    }


def generate_mock_issues(file_name: str) -> List[str]:
    """
    Generate mock security issues based on file extension.
    
    Args:
        file_name: Name of the file
        
    Returns:
        List of mock security issues
    """
    # Common security issues by file type
    issues_by_extension = {
        ".py": [
            "Hardcoded password",
            "Debug mode enabled",
            "Insecure random number generation",
            "SQL injection vulnerability",
            "Command injection vulnerability"
        ],
        ".js": [
            "Cross-site scripting (XSS) vulnerability",
            "Insecure use of eval()",
            "Prototype pollution",
            "Insecure JWT implementation"
        ],
        ".json": [
            "Sensitive data exposure",
            "Insecure configuration"
        ],
        ".html": [
            "Cross-site scripting (XSS) vulnerability",
            "Insecure content security policy"
        ],
        ".php": [
            "SQL injection vulnerability",
            "Remote file inclusion vulnerability",
            "Insecure file upload"
        ],
        ".java": [
            "Insecure deserialization",
            "XML external entity (XXE) vulnerability",
            "Path traversal vulnerability"
        ]
    }
    
    # Get file extension
    _, ext = os.path.splitext(file_name.lower())
    
    # Get potential issues for this file type
    potential_issues = issues_by_extension.get(ext, ["Unknown vulnerability"])
    
    # Randomly decide if the file has issues (70% chance)
    if random.random() < 0.7:
        # Select a random number of issues (1-3)
        num_issues = random.randint(1, min(3, len(potential_issues)))
        # Randomly select issues
        return random.sample(potential_issues, num_issues)
    else:
        # No issues found
        return []

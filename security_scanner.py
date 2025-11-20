import json
import os
import shutil
import subprocess
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Security Scanner API")

# Define the unified vulnerability model
class Vulnerability(BaseModel):
    name: str
    file: str
    lines: str
    severity: str
    impact: str
    exploitable: bool
    cvssScore: float
    description: str
    cve: Optional[str] = None
    recommendation: str
    codeSnippet: str
    fix: str

# Define the scan response model
class ScanResponse(BaseModel):
    scanId: str
    projectType: str
    vulnerabilities: List[Vulnerability]

def run_cmd(cmd: List[str], cwd: str) -> Dict[str, Any]:
    """
    Run a command and return its output.
    
    Args:
        cmd: Command to run as a list of strings
        cwd: Working directory
        
    Returns:
        Dict with stdout, stderr, and return code
    """
    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(timeout=300)  # 5 minute timeout
        return {
            "stdout": stdout,
            "stderr": stderr,
            "returncode": process.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Command timed out after 300 seconds",
            "returncode": -1
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Error executing command: {str(e)}",
            "returncode": -1
        }

def safe_extract_zip(zip_file: Path, extract_to: Path) -> bool:
    """
    Safely extract a ZIP file, preventing zip slip attacks.
    
    Args:
        zip_file: Path to the ZIP file
        extract_to: Directory to extract to
        
    Returns:
        True if extraction was successful, False otherwise
    """
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Check for zip slip vulnerabilities
            for file_info in zip_ref.infolist():
                file_path = Path(extract_to) / file_info.filename
                if not file_path.is_relative_to(extract_to):
                    return False
            
            # Extract files
            zip_ref.extractall(path=extract_to)
        return True
    except Exception:
        return False

def detect_project_type(project_dir: Path) -> str:
    """
    Detect the type of project based on files present.
    
    Args:
        project_dir: Path to the project directory
        
    Returns:
        Project type as a string
    """
    # Check for Python project
    if (project_dir / "requirements.txt").exists() or \
       (project_dir / "setup.py").exists() or \
       (project_dir / "pyproject.toml").exists() or \
       list(project_dir.glob("**/*.py")):
        return "python"
    
    # Check for Docker project
    if (project_dir / "Dockerfile").exists() or \
       list(project_dir.glob("**/Dockerfile")):
        return "docker"
    
    # Default to generic
    return "generic"

def get_file_content(file_path: str, start_line: int, end_line: int) -> str:
    """
    Get content from a file between specified line numbers.
    
    Args:
        file_path: Path to the file
        start_line: Starting line number (1-indexed)
        end_line: Ending line number (1-indexed)
        
    Returns:
        Content of the file between the specified lines
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
            
        # Adjust for 0-indexed list
        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines), end_line)
        
        return ''.join(lines[start_idx:end_idx])
    except Exception:
        return ""

def map_severity_to_cvss(severity: str) -> float:
    """
    Map severity string to CVSS score.
    
    Args:
        severity: Severity string (LOW, MEDIUM, HIGH)
        
    Returns:
        CVSS score as float
    """
    severity_map = {
        "LOW": 3.0,
        "MEDIUM": 5.5,
        "HIGH": 7.5,
        "CRITICAL": 9.0,
        "INFO": 1.0,
        "WARNING": 3.0,
        "ERROR": 7.0,
    }
    
    # Normalize severity to uppercase
    upper_severity = severity.upper()
    
    # Return mapped value or default to 3.0 if not found
    return severity_map.get(upper_severity, 3.0)

def map_bandit_issue(issue: Dict[str, Any], project_dir: Path) -> Vulnerability:
    """
    Map a Bandit issue to the unified vulnerability format.
    
    Args:
        issue: Bandit issue as a dictionary
        project_dir: Path to the project directory
        
    Returns:
        Vulnerability object
    """
    # Extract data from Bandit issue
    name = f"Bandit: {issue.get('test_id', '')} - {issue.get('test_name', '')}"
    file_path = issue.get('filename', '')
    line_start = issue.get('line_number', 0)
    line_end = line_start + 10  # Approximate a reasonable code snippet
    
    # Map severity
    severity_str = issue.get('issue_severity', 'LOW').upper()
    if severity_str not in ["LOW", "MEDIUM", "HIGH"]:
        severity_str = "LOW"
    
    # Get code snippet
    full_path = project_dir / file_path
    code_snippet = get_file_content(str(full_path), line_start, line_end) if full_path.exists() else ""
    
    # Create vulnerability object
    return Vulnerability(
        name=name,
        file=file_path,
        lines=f"{line_start}-{line_end}",
        severity=severity_str,
        impact=issue.get('issue_text', 'Security issue detected'),
        exploitable=severity_str == "HIGH",
        cvssScore=map_severity_to_cvss(severity_str),
        description=issue.get('issue_text', '') + '\n\n' + issue.get('more_info', ''),
        cve=None,
        recommendation=issue.get('issue_confidence', 'Fix the identified security issue'),
        codeSnippet=code_snippet,
        fix=f"Review and fix the {issue.get('test_name', 'security issue')} in {file_path} at line {line_start}"
    )

def map_semgrep_issue(issue: Dict[str, Any], project_dir: Path) -> Vulnerability:
    """
    Map a Semgrep issue to the unified vulnerability format.
    
    Args:
        issue: Semgrep issue as a dictionary
        project_dir: Path to the project directory
        
    Returns:
        Vulnerability object
    """
    # Extract data from Semgrep issue
    name = f"Semgrep: {issue.get('check_id', '')}"
    file_path = issue.get('path', '')
    
    # Get line information
    start_line = issue.get('start', {}).get('line', 0)
    end_line = issue.get('end', {}).get('line', start_line + 5)
    
    # Map severity
    severity_str = issue.get('extra', {}).get('severity', 'LOW').upper()
    if severity_str not in ["LOW", "MEDIUM", "HIGH"]:
        severity_str = "LOW"
    
    # Get code snippet
    full_path = project_dir / file_path
    code_snippet = get_file_content(str(full_path), start_line, end_line) if full_path.exists() else ""
    
    # Create vulnerability object
    return Vulnerability(
        name=name,
        file=file_path,
        lines=f"{start_line}-{end_line}",
        severity=severity_str,
        impact=issue.get('extra', {}).get('message', 'Security issue detected'),
        exploitable=severity_str == "HIGH",
        cvssScore=map_severity_to_cvss(severity_str),
        description=issue.get('extra', {}).get('message', '') + '\n\n' + issue.get('extra', {}).get('metadata', {}).get('description', ''),
        cve=None,
        recommendation=issue.get('extra', {}).get('metadata', {}).get('fix', 'Fix the identified security issue'),
        codeSnippet=code_snippet,
        fix=f"Review and fix the issue in {file_path} at line {start_line}: {issue.get('extra', {}).get('message', '')}"
    )

def map_gitleaks_issue(issue: Dict[str, Any], project_dir: Path) -> Vulnerability:
    """
    Map a Gitleaks issue to the unified vulnerability format.
    
    Args:
        issue: Gitleaks issue as a dictionary
        project_dir: Path to the project directory
        
    Returns:
        Vulnerability object
    """
    # Extract data from Gitleaks issue
    name = f"Gitleaks: {issue.get('RuleID', '')}"
    file_path = issue.get('File', '')
    
    # Get line information
    start_line = issue.get('StartLine', 0)
    end_line = issue.get('EndLine', start_line + 2)
    
    # Always HIGH severity for leaked secrets
    severity_str = "HIGH"
    
    # Get code snippet (redact the actual secret)
    full_path = project_dir / file_path
    code_snippet = "*** Secret content redacted ***"
    if full_path.exists():
        raw_snippet = get_file_content(str(full_path), start_line, end_line)
        # Redact the secret from the snippet
        if issue.get('Secret', '') and raw_snippet:
            code_snippet = raw_snippet.replace(issue.get('Secret', ''), '*** REDACTED ***')
    
    # Create vulnerability object
    return Vulnerability(
        name=name,
        file=file_path,
        lines=f"{start_line}-{end_line}",
        severity=severity_str,
        impact=f"Potential secret leak: {issue.get('Description', 'Secret detected')}",
        exploitable=True,  # Leaked secrets are always exploitable
        cvssScore=map_severity_to_cvss(severity_str),
        description=f"Potential secret or sensitive information detected in the codebase. Rule: {issue.get('RuleID', '')}. {issue.get('Description', '')}",
        cve=None,
        recommendation="Remove the secret from the codebase and revoke it immediately. Use environment variables or a secure secret management system instead.",
        codeSnippet=code_snippet,
        fix=f"Remove the secret from {file_path} at line {start_line} and revoke it immediately."
    )

def map_pip_audit_issue(issue: Dict[str, Any], project_dir: Path) -> Vulnerability:
    """
    Map a pip-audit issue to the unified vulnerability format.
    
    Args:
        issue: pip-audit issue as a dictionary
        project_dir: Path to the project directory
        
    Returns:
        Vulnerability object
    """
    # Extract data from pip-audit issue
    vulnerability = issue.get('vulnerability', {})
    name = f"pip-audit: {vulnerability.get('id', '')}"
    
    # pip-audit doesn't provide file paths, so we use the package name
    package = issue.get('package', {})
    file_path = f"requirements.txt (Package: {package.get('name', '')})"
    
    # Get CVE information
    cve_id = None
    aliases = vulnerability.get('aliases', [])
    for alias in aliases:
        if alias.startswith('CVE-'):
            cve_id = alias
            break
    
    # Map severity
    severity_str = vulnerability.get('severity', 'UNKNOWN').upper()
    if severity_str not in ["LOW", "MEDIUM", "HIGH"]:
        severity_str = "MEDIUM"  # Default to MEDIUM for package vulnerabilities
    
    # Create vulnerability object
    return Vulnerability(
        name=name,
        file=file_path,
        lines="N/A",  # pip-audit doesn't provide line numbers
        severity=severity_str,
        impact=f"Vulnerable package: {package.get('name', '')} {package.get('version', '')}",
        exploitable=severity_str in ["HIGH", "CRITICAL"],
        cvssScore=map_severity_to_cvss(severity_str),
        description=vulnerability.get('description', 'Vulnerable package detected'),
        cve=cve_id,
        recommendation=f"Update {package.get('name', '')} to version {vulnerability.get('fix_versions', ['latest'])[0] if vulnerability.get('fix_versions') else 'latest'}",
        codeSnippet="",  # No code snippet for package vulnerabilities
        fix=f"pip install --upgrade {package.get('name', '')}=={vulnerability.get('fix_versions', ['latest'])[0] if vulnerability.get('fix_versions') else 'latest'}"
    )

def map_ruff_issue(issue: Dict[str, Any], project_dir: Path) -> Vulnerability:
    """
    Map a Ruff issue to the unified vulnerability format.
    
    Args:
        issue: Ruff issue as a dictionary
        project_dir: Path to the project directory
        
    Returns:
        Vulnerability object
    """
    # Extract data from Ruff issue
    name = f"Ruff: {issue.get('code', '')}"
    file_path = issue.get('filename', '')
    
    # Get line information
    line_num = issue.get('location', {}).get('row', 0)
    start_line = max(1, line_num - 2)
    end_line = line_num + 3
    
    # Map severity based on rule code
    rule_code = issue.get('code', '')
    
    # Security-related rules are higher severity
    security_prefixes = ['S', 'B', 'A']
    if any(rule_code.startswith(prefix) for prefix in security_prefixes):
        severity_str = "MEDIUM"
    else:
        severity_str = "LOW"
    
    # Get code snippet
    full_path = project_dir / file_path
    code_snippet = get_file_content(str(full_path), start_line, end_line) if full_path.exists() else ""
    
    # Create vulnerability object
    return Vulnerability(
        name=name,
        file=file_path,
        lines=f"{line_num}-{line_num}",
        severity=severity_str,
        impact=issue.get('message', 'Code quality issue detected'),
        exploitable=False,  # Most Ruff issues are not directly exploitable
        cvssScore=map_severity_to_cvss(severity_str),
        description=f"Code quality issue: {issue.get('message', '')}",
        cve=None,
        recommendation=f"Fix the {issue.get('code', '')} issue: {issue.get('message', '')}",
        codeSnippet=code_snippet,
        fix=f"Fix the issue in {file_path} at line {line_num}: {issue.get('message', '')}"
    )

@app.post("/security-testing", response_model=ScanResponse)
async def security_testing(file: UploadFile = File(...)) -> ScanResponse:
    """
    Upload a ZIP file and perform security scanning.
    
    Args:
        file: ZIP file to scan
        
    Returns:
        ScanResponse with scan results
    """
    # Generate a unique scan ID
    scan_id = str(uuid.uuid4())
    
    # Create temporary directories
    temp_dir = tempfile.mkdtemp()
    zip_path = Path(temp_dir) / "upload.zip"
    extract_dir = Path(temp_dir) / "extracted"
    results_dir = Path(temp_dir) / "results"
    
    try:
        # Create directories
        extract_dir.mkdir(exist_ok=True)
        results_dir.mkdir(exist_ok=True)
        
        # Save uploaded file
        with open(zip_path, "wb") as f:
            f.write(await file.read())
        
        # Extract ZIP file
        if not safe_extract_zip(zip_path, extract_dir):
            raise HTTPException(status_code=400, detail="Invalid ZIP file or potential zip slip attack detected")
        
        # Detect project type
        project_type = detect_project_type(extract_dir)
        
        # Initialize vulnerabilities list
        vulnerabilities = []
        
        # Run Bandit (Python security scanner)
        if project_type == "python":
            bandit_output = results_dir / "bandit_results.json"
            bandit_cmd = [
                "bandit", "-r", str(extract_dir), "-f", "json", "-o", str(bandit_output)
            ]
            run_cmd(bandit_cmd, str(extract_dir))
            
            # Parse Bandit results
            if bandit_output.exists():
                try:
                    with open(bandit_output, 'r') as f:
                        bandit_data = json.load(f)
                        for result in bandit_data.get('results', []):
                            vulnerabilities.append(map_bandit_issue(result, extract_dir))
                except json.JSONDecodeError:
                    pass  # Skip if JSON is invalid
        
        # Run Semgrep
        semgrep_output = results_dir / "semgrep_results.json"
        semgrep_cmd = [
            "semgrep", "--config=auto", "--json", "-o", str(semgrep_output), str(extract_dir)
        ]
        run_cmd(semgrep_cmd, str(extract_dir))
        
        # Parse Semgrep results
        if semgrep_output.exists():
            try:
                with open(semgrep_output, 'r') as f:
                    semgrep_data = json.load(f)
                    for result in semgrep_data.get('results', []):
                        vulnerabilities.append(map_semgrep_issue(result, extract_dir))
            except json.JSONDecodeError:
                pass  # Skip if JSON is invalid
        
        # Run Gitleaks
        gitleaks_output = results_dir / "gitleaks_results.json"
        gitleaks_cmd = [
            "gitleaks", "detect", "--source", str(extract_dir), "-f", "json", "-r", str(gitleaks_output)
        ]
        run_cmd(gitleaks_cmd, str(extract_dir))
        
        # Parse Gitleaks results
        if gitleaks_output.exists():
            try:
                with open(gitleaks_output, 'r') as f:
                    gitleaks_data = json.load(f)
                    for result in gitleaks_data:
                        vulnerabilities.append(map_gitleaks_issue(result, extract_dir))
            except json.JSONDecodeError:
                pass  # Skip if JSON is invalid
        
        # Run pip-audit for Python projects
        if project_type == "python":
            pip_audit_output = results_dir / "pip_audit_results.json"
            
            # Try to find requirements file
            req_file = None
            for possible_req in ["requirements.txt", "pyproject.toml", "setup.py"]:
                if (extract_dir / possible_req).exists():
                    req_file = possible_req
                    break
            
            if req_file:
                pip_audit_cmd = [
                    "pip-audit", "-r", str(extract_dir / req_file), "--format", "json", "-o", str(pip_audit_output)
                ]
                run_cmd(pip_audit_cmd, str(extract_dir))
                
                # Parse pip-audit results
                if pip_audit_output.exists():
                    try:
                        with open(pip_audit_output, 'r') as f:
                            pip_audit_data = json.load(f)
                            for result in pip_audit_data.get('vulnerabilities', []):
                                vulnerabilities.append(map_pip_audit_issue(result, extract_dir))
                    except json.JSONDecodeError:
                        pass  # Skip if JSON is invalid
        
        # Run Ruff (Python linter)
        if project_type == "python":
            ruff_output = results_dir / "ruff_results.json"
            ruff_cmd = [
                "ruff", "check", str(extract_dir), "--output-format=json", "--output-file", str(ruff_output)
            ]
            run_cmd(ruff_cmd, str(extract_dir))
            
            # Parse Ruff results
            if ruff_output.exists():
                try:
                    with open(ruff_output, 'r') as f:
                        ruff_data = json.load(f)
                        for result in ruff_data:
                            vulnerabilities.append(map_ruff_issue(result, extract_dir))
                except json.JSONDecodeError:
                    pass  # Skip if JSON is invalid
        
        # Create response
        response = ScanResponse(
            scanId=scan_id,
            projectType=project_type,
            vulnerabilities=vulnerabilities
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing scan: {str(e)}")
    
    finally:
        # Clean up temporary files
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    uvicorn.run("security_scanner:app", host="0.0.0.0", port=8000, reload=True)


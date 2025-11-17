#!/usr/bin/env python3
"""
Security API Usage Example

This script demonstrates how to use the Security Scanner API
to scan a ZIP file for vulnerabilities.
"""

import requests
import json
import zipfile
import tempfile
import os
from pathlib import Path

def create_sample_project():
    """Create a sample Python project with some vulnerabilities for testing."""
    temp_dir = tempfile.mkdtemp()
    project_dir = Path(temp_dir) / "sample_project"
    project_dir.mkdir()
    
    # Create a vulnerable Python file
    vulnerable_code = '''
import os
import subprocess
import pickle

# Vulnerable code examples for testing
def vulnerable_function():
    # SQL Injection vulnerability
    user_input = input("Enter username: ")
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    
    # Command injection vulnerability
    os.system(f"ls {user_input}")
    
    # Hardcoded secret (will be detected by Gitleaks)
    api_key = "sk-1234567890abcdef1234567890abcdef"
    
    # Unsafe pickle usage
    data = pickle.loads(user_input.encode())
    
    # Weak random number generation
    import random
    password = str(random.random())
    
    return query, data, password

if __name__ == "__main__":
    vulnerable_function()
'''
    
    # Write vulnerable code to file
    with open(project_dir / "vulnerable_app.py", "w") as f:
        f.write(vulnerable_code)
    
    # Create requirements.txt with vulnerable packages
    requirements = '''
requests==2.25.0
flask==1.0.0
django==2.0.0
'''
    
    with open(project_dir / "requirements.txt", "w") as f:
        f.write(requirements)
    
    # Create ZIP file
    zip_path = Path(temp_dir) / "sample_project.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_path in project_dir.rglob('*'):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(project_dir))
    
    return str(zip_path)

def scan_project(zip_file_path: str, api_url: str = "http://localhost:8001"):
    """
    Send a ZIP file to the Security Scanner API for scanning.
    
    Args:
        zip_file_path: Path to the ZIP file to scan
        api_url: Base URL of the Security Scanner API
        
    Returns:
        Scan results as a dictionary
    """
    
    # Prepare the file for upload
    with open(zip_file_path, 'rb') as f:
        files = {'file': ('project.zip', f, 'application/zip')}
        
        # Send POST request to the security-testing endpoint
        response = requests.post(f"{api_url}/security-testing", files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def print_scan_results(results: dict):
    """
    Print scan results in a formatted way.
    
    Args:
        results: Scan results dictionary
    """
    if not results:
        print("No results to display")
        return
    
    print(f"\n{'='*60}")
    print(f"SECURITY SCAN RESULTS")
    print(f"{'='*60}")
    print(f"Scan ID: {results['scanId']}")
    print(f"Project Type: {results['projectType']}")
    print(f"Total Vulnerabilities: {len(results['vulnerabilities'])}")
    print(f"{'='*60}")
    
    # Group vulnerabilities by severity
    severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    
    for vuln in results['vulnerabilities']:
        severity = vuln['severity']
        if severity in severity_counts:
            severity_counts[severity] += 1
    
    print(f"\nSeverity Breakdown:")
    print(f"  HIGH: {severity_counts['HIGH']}")
    print(f"  MEDIUM: {severity_counts['MEDIUM']}")
    print(f"  LOW: {severity_counts['LOW']}")
    
    print(f"\n{'='*60}")
    print("DETAILED VULNERABILITIES")
    print(f"{'='*60}")
    
    # Sort vulnerabilities by severity (HIGH first)
    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    sorted_vulns = sorted(results['vulnerabilities'], 
                         key=lambda x: severity_order.get(x['severity'], 3))
    
    for i, vuln in enumerate(sorted_vulns, 1):
        print(f"\n[{i}] {vuln['name']}")
        print(f"    File: {vuln['file']}")
        print(f"    Lines: {vuln['lines']}")
        print(f"    Severity: {vuln['severity']} (CVSS: {vuln['cvssScore']})")
        print(f"    Exploitable: {vuln['exploitable']}")
        print(f"    Impact: {vuln['impact']}")
        
        if vuln['cve']:
            print(f"    CVE: {vuln['cve']}")
        
        print(f"    Description: {vuln['description'][:100]}...")
        print(f"    Recommendation: {vuln['recommendation'][:100]}...")
        print(f"    Fix: {vuln['fix'][:100]}...")
        
        if vuln['codeSnippet'] and not vuln['codeSnippet'].startswith('***'):
            print(f"    Code Snippet:")
            snippet_lines = vuln['codeSnippet'].split('\n')[:3]
            for line in snippet_lines:
                if line.strip():
                    print(f"      {line}")
        
        print(f"    {'-'*50}")

def main():
    """Main function to demonstrate the Security Scanner API usage."""
    
    print("Security Scanner API - Usage Example")
    print("====================================")
    
    # Check if API is running
    api_url = "http://localhost:8001"
    try:
        response = requests.get(f"{api_url}/health")
        if response.status_code != 200:
            print(f"Error: Security API is not running at {api_url}")
            print("Please start the API first: python security_api.py")
            return
    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to Security API at {api_url}")
        print("Please start the API first: python security_api.py")
        return
    
    print(f"✅ Security API is running at {api_url}")
    
    # Create a sample project for testing
    print("\n📦 Creating sample vulnerable project...")
    zip_file_path = create_sample_project()
    print(f"✅ Sample project created: {zip_file_path}")
    
    # Scan the project
    print("\n🔍 Scanning project for vulnerabilities...")
    results = scan_project(zip_file_path)
    
    if results:
        print("✅ Scan completed successfully!")
        print_scan_results(results)
        
        # Save results to file
        results_file = "scan_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {results_file}")
    else:
        print("❌ Scan failed!")
    
    # Cleanup
    try:
        os.remove(zip_file_path)
        print(f"\n🧹 Cleaned up temporary file: {zip_file_path}")
    except:
        pass

if __name__ == "__main__":
    main()


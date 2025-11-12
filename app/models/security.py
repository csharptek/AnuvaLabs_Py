"""
Pydantic models for security testing API.
"""
from typing import List, Dict, Any, Optional, Union
from datetime import date
from pydantic import BaseModel, Field


class VulnerabilityDetail(BaseModel):
    """Model for detailed vulnerability information."""
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


class ScanResponse(BaseModel):
    """Response model for security scan results."""
    status: str = "success"
    file_count: int
    vulnerabilities: List[VulnerabilityDetail]


class ErrorResponse(BaseModel):
    """Response model for error messages."""
    status: str = "error"
    message: str
    details: Optional[Dict[str, Any]] = None

"""
Pydantic models for security testing API.
"""
from typing import List, Dict, Any, Optional
from datetime import date
from pydantic import BaseModel, Field


class VulnerabilityItem(BaseModel):
    """Model for vulnerability item."""
    file: str
    issues: List[str]


class ScanResponse(BaseModel):
    """Response model for security scan results."""
    status: str = "success"
    file_count: int
    vulnerabilities: List[VulnerabilityItem]


class ErrorResponse(BaseModel):
    """Response model for error messages."""
    status: str = "error"
    message: str
    details: Optional[Dict[str, Any]] = None

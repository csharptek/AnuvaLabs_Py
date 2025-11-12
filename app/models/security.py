"""
Pydantic models for security testing API.
"""
from typing import List, Dict, Any, Optional
from datetime import date
from pydantic import BaseModel, Field


class RecentScan(BaseModel):
    """Model for recent scan information."""
    project: str
    issues_found: int
    last_scan: date


class DashboardResponse(BaseModel):
    """Response model for dashboard statistics."""
    status: str = "success"
    total_projects: int
    total_scans: int
    vulnerabilities_found: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    recent_scans: List[RecentScan]


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


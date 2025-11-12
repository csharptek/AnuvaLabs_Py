"""
API routes for security testing endpoints.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse

from app.models.security import DashboardResponse, ScanResponse, ErrorResponse
from app.services.security_service import get_mock_dashboard_data, process_zip_file

# Create router
router = APIRouter(prefix="/api/v1")


@router.get(
    "/dashboard",
    response_model=DashboardResponse,
    responses={
        200: {"model": DashboardResponse, "description": "Dashboard statistics retrieved successfully"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Security Dashboard Statistics",
    description="Returns mock dashboard statistics for security testing."
)
async def get_dashboard():
    """
    Get security dashboard statistics.
    
    Returns:
        JSON response with dashboard statistics
    """
    try:
        # Get mock dashboard data
        dashboard_data = get_mock_dashboard_data()
        return dashboard_data
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve dashboard data: {str(e)}"
        )


@router.post(
    "/security-testing",
    response_model=ScanResponse,
    responses={
        200: {"model": ScanResponse, "description": "Security scan completed successfully"},
        400: {"model": ErrorResponse, "description": "Bad request or invalid file"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Run Security Test on ZIP File",
    description="Accepts a ZIP file upload, extracts files, and returns mock vulnerability scan results."
)
async def security_testing(file: UploadFile = File(...)):
    """
    Run security testing on uploaded ZIP file.
    
    Args:
        file: Uploaded ZIP file
        
    Returns:
        JSON response with security scan results
    """
    try:
        # Validate file type
        if not file.filename.endswith('.zip'):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"status": "error", "message": "Only ZIP files are supported"}
            )
        
        # Read file content
        file_content = await file.read()
        
        # Process the ZIP file
        scan_results = process_zip_file(file_content)
        
        return scan_results
    except ValueError as e:
        # Handle validation errors
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": str(e)}
        )
    except Exception as e:
        # Handle any unexpected errors
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": f"Failed to process file: {str(e)}"}
        )


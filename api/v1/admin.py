"""
Admin endpoints for ThirdEye
Provides authentication and report management for administrators
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from middleware.admin_auth import (
    verify_admin_password,
    create_admin_session,
    require_admin_auth,
    revoke_admin_session,
)
from nodes.supabase_store import get_supabase_client

router = APIRouter(prefix="/admin", tags=["admin"])


class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    success: bool
    token: str
    expires_at: str
    message: str


class LogoutRequest(BaseModel):
    token: str


class ReportFilter(BaseModel):
    flagged_only: Optional[bool] = None
    has_violations: Optional[bool] = None
    limit: Optional[int] = 50
    offset: Optional[int] = 0


@router.post("/login")
async def admin_login(request: LoginRequest) -> LoginResponse:
    """
    Authenticate admin and create a session
    """
    if not verify_admin_password(request.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    session_data = create_admin_session()
    
    return LoginResponse(
        success=True,
        token=session_data["token"],
        expires_at=session_data["expires_at"],
        message="Login successful"
    )


@router.post("/logout")
async def admin_logout(request: LogoutRequest):
    """
    Revoke an admin session
    """
    revoked = revoke_admin_session(request.token)
    return {
        "success": revoked,
        "message": "Logged out successfully" if revoked else "Session not found"
    }


@router.get("/reports")
async def get_all_reports(
    flagged_only: Optional[bool] = None,
    has_violations: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
    _token: str = Depends(require_admin_auth)
):
    """
    Get all reports with optional filtering
    Requires admin authentication
    """
    try:
        supabase = get_supabase_client()
        
        # Build query
        query = supabase.table("violation_reports").select("*")
        
        # Apply filters
        if flagged_only is True:
            query = query.eq("needs_manual_verification", True)
        
        if has_violations is not None:
            query = query.eq("is_violation", has_violations)
        
        # Order by most recent first
        query = query.order("reported_timestamp", desc=True)
        
        # Apply pagination
        query = query.range(offset, offset + limit - 1)
        
        result = query.execute()
        
        return {
            "success": True,
            "reports": result.data,
            "count": len(result.data),
            "offset": offset,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching reports: {str(e)}")


@router.get("/reports/{report_id}")
async def get_report_detail(
    report_id: int,
    _token: str = Depends(require_admin_auth)
):
    """
    Get detailed information about a specific report
    Requires admin authentication
    """
    try:
        supabase = get_supabase_client()
        result = supabase.table("violation_reports").select("*").eq("id", report_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "success": True,
            "report": result.data[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching report: {str(e)}")


@router.patch("/reports/{report_id}/flag")
async def flag_report(
    report_id: int,
    flagged: bool,
    _token: str = Depends(require_admin_auth)
):
    """
    Flag or unflag a report for manual verification
    Requires admin authentication
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("violation_reports").update({
            "needs_manual_verification": flagged
        }).eq("id", report_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "success": True,
            "message": f"Report {'flagged' if flagged else 'unflagged'} successfully",
            "report": result.data[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating report: {str(e)}")


@router.patch("/reports/{report_id}/approve")
async def approve_report(
    report_id: int,
    approved: bool,
    _token: str = Depends(require_admin_auth)
):
    """
    Approve or reject a report
    Requires admin authentication
    """
    try:
        supabase = get_supabase_client()
        
        update_data = {
            "admin_approved": approved,
            "admin_reviewed": True
        }
        
        # If approving, clear the manual verification flag
        if approved:
            update_data["needs_manual_verification"] = False
        
        result = supabase.table("violation_reports").update(update_data).eq("id", report_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "success": True,
            "message": f"Report {'approved' if approved else 'rejected'} successfully",
            "report": result.data[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error approving report: {str(e)}")


@router.get("/stats")
async def get_stats(_token: str = Depends(require_admin_auth)):
    """
    Get overall statistics for the admin dashboard
    Requires admin authentication
    """
    try:
        supabase = get_supabase_client()
        
        # Get total reports
        total_result = supabase.table("violation_reports").select("id", count="exact").execute()
        total_reports = total_result.count or 0
        
        # Get reports with violations
        violations_result = supabase.table("violation_reports").select("id", count="exact").eq("is_violation", True).execute()
        reports_with_violations = violations_result.count or 0
        
        # Get flagged reports
        flagged_result = supabase.table("violation_reports").select("id", count="exact").eq("needs_manual_verification", True).execute()
        flagged_reports = flagged_result.count or 0
        
        # Get approved reports
        approved_result = supabase.table("violation_reports").select("id", count="exact").eq("admin_approved", True).execute()
        approved_reports = approved_result.count or 0
        
        # Get pending approval (violations that haven't been reviewed)
        pending_result = supabase.table("violation_reports").select("id", count="exact").eq("is_violation", True).eq("admin_reviewed", False).execute()
        pending_approval = pending_result.count or 0
        
        return {
            "success": True,
            "stats": {
                "total_reports": total_reports,
                "reports_with_violations": reports_with_violations,
                "flagged_reports": flagged_reports,
                "reports_without_violations": total_reports - reports_with_violations,
                "approved_reports": approved_reports,
                "pending_approval": pending_approval
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

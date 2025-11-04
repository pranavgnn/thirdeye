import os
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from supabase import create_client, Client
from .vision import ImageAnalysisResult
from .violations import ViolationsResult

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


class ReportResult(BaseModel):
    success: bool
    error: Optional[str] = None
    report_id: Optional[int] = None
    analysis: ImageAnalysisResult
    violations: list[ViolationsResult]
    reporter_phone: Optional[str] = None
    reported_image: Optional[str] = None


def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("Missing Supabase credentials")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def format_violations_for_llm(violations: list[ViolationsResult]) -> str:
    if not violations:
        return "No violations detected"
    
    lines = []
    for v in violations:
        lines.append(f"- {v.name} ({v.category}): ₹{v.fine_amount} under Section {v.section}")
    return "\n".join(lines)


def store_report(data: dict) -> ReportResult:
    analysis: ImageAnalysisResult = data["analysis"]
    violations: list[ViolationsResult] = data["violations"]
    
    reporter_phone = data.get("reporter_phone")
    reported_image = data.get("reported_image")
    
    try:
        supabase = get_supabase_client()
        
        # Determine if manual verification is needed
        # Flag for manual verification if:
        # - License plate confidence is low (<0.7) but plate is present
        # - Location confidence is low (<0.7)
        # - Overall confidence is low (<0.6)
        # - Is a violation but no violations detected
        needs_manual_verification = False
        if analysis.is_violation:
            if (analysis.license_plate and analysis.license_plate_confidence < 0.7):
                needs_manual_verification = True
            elif analysis.location_confidence < 0.7:
                needs_manual_verification = True
            elif analysis.confidence_score < 0.6:
                needs_manual_verification = True
            elif not violations:
                needs_manual_verification = True
        
        # Try with new schema first (includes new fields)
        report_data = {
            "reporter_phone": reporter_phone,
            "reported_timestamp": datetime.utcnow().isoformat(),
            "reported_image": reported_image,
            "license_plate": analysis.license_plate,
            "license_plate_confidence": analysis.license_plate_confidence,
            "is_india_location": analysis.is_india_location,
            "location_confidence": analysis.location_confidence,
            "violations": [v.model_dump() for v in violations],
            "confidence_score": analysis.confidence_score,
            "short_description": analysis.short_description,
            "is_violation": analysis.is_violation,
            "detailed_description": analysis.detailed_description,
            "title": analysis.title or "Traffic Violation Report",
            "needs_manual_verification": needs_manual_verification
        }
        
        try:
            result = supabase.table("violation_reports").insert(report_data).execute()
        except Exception as insert_error:
            # If insert fails (likely due to missing columns), try with old schema
            # Remove the new fields and retry
            report_data_old = {
                "reporter_phone": reporter_phone,
                "reported_timestamp": datetime.utcnow().isoformat(),
                "reported_image": reported_image,
                "license_plate": analysis.license_plate,
                "violations": [v.model_dump() for v in violations],
                "confidence_score": analysis.confidence_score,
                "short_description": analysis.short_description,
                "is_violation": analysis.is_violation,
                "detailed_description": analysis.detailed_description,
                "title": analysis.title or "Traffic Violation Report"
            }
            result = supabase.table("violation_reports").insert(report_data_old).execute()
        
        report_id = result.data[0].get("id") if result.data else None
        
        return ReportResult(
            success=True,
            report_id=report_id,
            analysis=analysis,
            violations=violations,
            reporter_phone=reporter_phone,
            reported_image=reported_image
        )
        
    except Exception as e:
        return ReportResult(
            success=False,
            error=str(e),
            analysis=analysis,
            violations=violations,
            reporter_phone=reporter_phone,
            reported_image=reported_image
        )

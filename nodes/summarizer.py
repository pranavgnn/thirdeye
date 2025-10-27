from langchain.chat_models import init_chat_model
from pydantic import BaseModel

from .violations import ViolationsResult
from .vision import ImageAnalysisResult
from .supabase_store import ReportResult
from config import SUMMARY_MODEL
from utils.lazy import chat_model


class SummaryInput(BaseModel):
    analysis: ImageAnalysisResult
    violations: list[ViolationsResult]


def summarize(report_result: ReportResult) -> str:
    data = {
        "analysis": report_result.analysis,
        "violations": report_result.violations
    }
    
    report_status = ""
    if report_result.success:
        report_status = f"Report recorded (ID: {report_result.report_id})"
    else:
        report_status = f"Report storage failed: {report_result.error}"
    
    manual_verification = ""
    if report_result.analysis.confidence_score < 0.7:
        manual_verification = "REQUIRES MANUAL VERIFICATION (Low confidence)"
    elif not report_result.analysis.license_plate and report_result.analysis.vehicle_detected:
        manual_verification = "REQUIRES MANUAL VERIFICATION (License plate not detected)"
    
    # Check if image is not from India with high confidence
    location_warning = ""
    if not report_result.analysis.is_india_location and report_result.analysis.location_confidence > 0.99:
        location_warning = "⚠️ WARNING: This image does not appear to be from India. This application is designed for Indian traffic scenarios only. Analysis may not be accurate."
    
    # Check license plate confidence
    license_plate_note = ""
    if report_result.analysis.license_plate and report_result.analysis.license_plate_confidence < 0.7:
        license_plate_note = "Note: License plate reading has low confidence and should be verified."
    
    system_instructions = """You are an AI assistant summarizing traffic violation reports for an Indian traffic enforcement system.

You receive:
- analysis: Vision model output describing what was seen in the image (vehicle, license plate, possible violations, confidence, etc.)
- violations: A list of possible legal matches for the detected violation(s).
- report_status: Whether the report was successfully recorded in the database
- manual_verification: Whether manual verification is required
- location_warning: Warning if the image is not from India
- license_plate_note: Note about license plate confidence

Your task is to create a short, factual, and reader-friendly message describing the result. 
This message will be sent to an end user or displayed on a dashboard.

Guidelines:
- Be concise, neutral, and professional.
- **CRITICAL**: If location_warning is present, START with it prominently.
- Always start with a summary of what was detected (vehicle, license plate, and violation status).
- **DO NOT mention the license plate number in your description if license_plate_confidence is below 0.7** - instead note that plate detection was uncertain.
- If license_plate_note is present, include it after mentioning the violation.
- Include the report status at the end.
- If manual verification is required, EMPHASIZE this clearly and prominently.
- If no vehicle is detected, clearly state that.
- If a violation is not confirmed or confidence is low, explain that the case requires manual review.
- If a violation is confirmed, include:
  - The violation name
  - The section of the Motor Vehicles Act
  - The fine amount in INR
- Avoid technical terms like confidence score unless needed for clarity.
- Never output JSON or lists — write natural text only.
- Do not add emojis (except the warning emoji if location_warning is present), speculation, or extra commentary.

Keep the response under 200 words."""
    
    user_message = f"""You are given the following structured input for summarization:

Image Analysis Result:
{data["analysis"].model_dump_json(indent=2)}

Matched Violation Candidates:
{"\n".join([ v.model_dump_json(indent=2) for v in data["violations"]])}

Report Status: {report_status}
Manual Verification Flag: {manual_verification if manual_verification else "Not required"}
Location Warning: {location_warning if location_warning else "None"}
License Plate Note: {license_plate_note if license_plate_note else "None"}

Compose a short, human-readable message summarizing what was detected in the image, the violation outcome, whether the report was recorded, and manual verification status. 

IMPORTANT: 
- If location_warning is present, start your response with it.
- If license_plate_confidence is below 0.7, do NOT mention the specific license plate number - just note that plate detection was uncertain or not possible.

Follow the style described in the system prompt."""
    
    response = chat_model(SUMMARY_MODEL).invoke([
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": user_message}
    ])

    return response.content

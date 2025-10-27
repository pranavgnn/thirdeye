from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import base64
from langchain_core.runnables import RunnableLambda
from nodes.vision import analyse_image
from nodes.violations import match_violations
from nodes.supabase_store import store_report

router = APIRouter(prefix="/analyze")


@router.post("")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze an uploaded image for traffic violations.
    Processes the image through the same chain as the WhatsApp bot.
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file content
        contents = await file.read()
        
        # Convert to base64 data URI
        b64 = base64.b64encode(contents).decode("utf-8")
        data_uri = f"data:{file.content_type};base64,{b64}"
        
        # Use the same chain structure as WhatsApp bot, but return structured data
        def analyse_with_context(image_url: str):
            result = analyse_image(image_url)
            return {
                "analysis": result,
                "reporter_phone": None,  # No phone for web uploads
                "reported_image": data_uri
            }
        
        def add_violations(data: dict):
            violations = match_violations(data["analysis"])
            return {
                **data,
                "violations": violations
            }
        
        # Build chain: analyze -> match violations -> store report
        chain = (
            RunnableLambda(analyse_with_context)
            | RunnableLambda(add_violations)
            | RunnableLambda(store_report)
        )
        
        # Execute the chain
        report_result = chain.invoke(data_uri)
        
        # Return structured data for the frontend
        # Convert Pydantic models to dicts for JSON serialization
        return JSONResponse(content={
            "success": True,
            "result": {
                **report_result.analysis.model_dump(),
                "violations": [v.model_dump() for v in report_result.violations],
                "report_id": report_result.report_id,
                "report_success": report_result.success
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

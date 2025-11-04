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
    Analyze an uploaded image for traffic violations using the same structure
    as the WhatsApp bot chain, and store the report.
    Returns structured data suitable for the web UI.
    """
    try:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        contents = await file.read()
        b64 = base64.b64encode(contents).decode("utf-8")
        data_uri = f"data:{file.content_type};base64,{b64}"

        def analyse_with_context(image_url: str):
            result = analyse_image(image_url)
            return {
                "analysis": result,
                "reporter_phone": None,
                "reported_image": data_uri,
            }

        def add_violations(data: dict):
            violations = match_violations(data["analysis"])
            return {**data, "violations": violations}

        chain = (
            RunnableLambda(analyse_with_context)
            | RunnableLambda(add_violations)
            | RunnableLambda(store_report)
        )

        report_result = chain.invoke(data_uri)

        return JSONResponse(
            content={
                "success": True,
                "result": {
                    **report_result.analysis.model_dump(),
                    "violations": [v.model_dump() for v in report_result.violations],
                    "report_id": report_result.report_id,
                    "report_success": report_result.success,
                },
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

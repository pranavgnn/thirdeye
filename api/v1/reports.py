from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from nodes.supabase_store import get_supabase_client

router = APIRouter(prefix="/reports")


@router.get("")
async def list_reports(limit: int = Query(100, ge=1, le=1000)):
    try:
        sb = get_supabase_client()
        res = sb.table("violation_reports").select("*").order("reported_timestamp", desc=True).limit(limit).execute()
        data = res.data or []
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

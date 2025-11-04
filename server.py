from pathlib import Path
from fastapi import FastAPI, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
from api.v1.health import router as health_router
from api.v1.reports import router as reports_router
from api.v1.analyze import router as analyze_router
from api.v1.admin import router as admin_router
from api.v1.webhook.whatsapp import router as webhook_router

load_dotenv()

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(reports_router)
api_router.include_router(analyze_router)
api_router.include_router(admin_router)
api_router.include_router(webhook_router)
app.include_router(api_router)

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=404, content={"error": "Not found"})
    
    frontend_dist = Path(__file__).parent / "frontend" / "dist"
    if frontend_dist.exists():
        return FileResponse(frontend_dist / "index.html")
    
    return JSONResponse(status_code=404, content={"error": "Not found"})

frontend_dist = Path(__file__).parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        path = frontend_dist / full_path if full_path else frontend_dist / "index.html"
        return FileResponse(path if path.exists() else frontend_dist / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
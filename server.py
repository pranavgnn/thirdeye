import os
import traceback
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse, FileResponse
from dotenv import load_dotenv
from utils.whatsapp import handle_image

load_dotenv()

app = FastAPI()

WABA_VERIFY_TOKEN = os.getenv("WABA_VERIFY_TOKEN")


 


@app.get("/webhook/whatsapp", response_class=PlainTextResponse)
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    if mode == "subscribe" and token == WABA_VERIFY_TOKEN:
        return challenge or ""
    return PlainTextResponse("forbidden", status_code=403)


@app.post("/webhook/whatsapp")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    try:
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                for msg in value.get("messages", []):
                    wa_id = msg.get("from")
                    t = msg.get("type")
                    if t == "image" and "image" in msg:
                        media_id = msg["image"].get("id")
                        if wa_id and media_id:
                            background_tasks.add_task(handle_image, wa_id, media_id)
    except Exception:
        pass
    return {"status": "ok"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "index.html")
    return FileResponse(path, media_type="text/html")


@app.get("/privacy")
async def privacy():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "privacy.html")
    return FileResponse(path, media_type="text/html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
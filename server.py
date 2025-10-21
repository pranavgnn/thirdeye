import os
import base64
import traceback
import requests
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse, FileResponse
from dotenv import load_dotenv

from main import chain

load_dotenv()

app = FastAPI()

WABA_TOKEN = os.getenv("WABA_TOKEN")
WABA_PHONE_NUMBER_ID = os.getenv("WABA_PHONE_NUMBER_ID")
WABA_VERIFY_TOKEN = os.getenv("WABA_VERIFY_TOKEN")

GRAPH_BASE = "https://graph.facebook.com/v22.0"


def send_whatsapp_text(to_wa_id: str, body: str):
    url = f"{GRAPH_BASE}/{WABA_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WABA_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to_wa_id, "type": "text", "text": {"body": body[:4000]}}
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()


def download_media_data_uri(media_id: str) -> str:
    headers = {"Authorization": f"Bearer {WABA_TOKEN}"}
    meta_res = requests.get(f"{GRAPH_BASE}/{media_id}", headers=headers, timeout=30)
    meta_res.raise_for_status()
    media_url = meta_res.json().get("url")
    if not media_url:
        raise RuntimeError("media url missing")
    media_res = requests.get(media_url, headers=headers, timeout=60)
    media_res.raise_for_status()
    content_type = media_res.headers.get("Content-Type", "image/jpeg")
    b64 = base64.b64encode(media_res.content).decode("utf-8")
    return f"data:{content_type};base64,{b64}"


def handle_image(wa_id: str, media_id: str):
    try:
        data_uri = download_media_data_uri(media_id)
        result = chain.invoke(data_uri)
        send_whatsapp_text(wa_id, str(result))
    except Exception:
        print("process error:", traceback.format_exc())
        try:
            send_whatsapp_text(wa_id, "Error processing image")
        except Exception:
            print("reply error:", traceback.format_exc())


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
        print("webhook error:", traceback.format_exc())
    return {"status": "ok"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/privacy")
async def privacy():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "privacy.html")
    return FileResponse(path, media_type="text/html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
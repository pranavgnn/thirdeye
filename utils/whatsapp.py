import os
import base64
import traceback
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


WABA_TOKEN = os.getenv("WABA_TOKEN")
WABA_PHONE_NUMBER_ID = os.getenv("WABA_PHONE_NUMBER_ID")

GRAPH_BASE = "https://graph.facebook.com/v22.0"


def send_whatsapp_text(to_wa_id: str, body: str):
    url = f"{GRAPH_BASE}/{WABA_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WABA_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": str(to_wa_id),
        "type": "text",
        "text": {
            "preview_url": False,
            "body": str(body)[:4000],
        },
    }
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
    from main import build_chain

    try:
        data_uri = download_media_data_uri(media_id)
        chain = build_chain(reporter_phone=wa_id, reported_image=data_uri)
        result = chain.invoke(data_uri)
        send_whatsapp_text(wa_id, str(result))
    except Exception:
        try:
            send_whatsapp_text(wa_id, "Error processing image")
        except Exception:
            pass

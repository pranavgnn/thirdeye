from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse
from middleware import verify_webhook_token
from utils.whatsapp import handle_image

router = APIRouter()


@router.get("/webhook/whatsapp", response_class=PlainTextResponse)
@verify_webhook_token
async def verify_webhook(request: Request):
    pass


@router.post("/webhook/whatsapp")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    
    entries = body.get("entry", [])
    for entry in entries:
        changes = entry.get("changes", [])
        for change in changes:
            messages = change.get("value", {}).get("messages", [])
            for msg in messages:
                if msg.get("type") != "image" or "image" not in msg:
                    continue
                
                wa_id = msg.get("from")
                media_id = msg["image"].get("id")
                
                if wa_id and media_id:
                    background_tasks.add_task(handle_image, wa_id, media_id)
    
    return {"status": "ok"}

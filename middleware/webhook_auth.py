import os
from functools import wraps
from fastapi import Request
from fastapi.responses import PlainTextResponse

WABA_VERIFY_TOKEN = os.getenv("WABA_VERIFY_TOKEN")


def verify_webhook_token(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        params = dict(request.query_params)
        mode = params.get("hub.mode")
        token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")
        
        if mode == "subscribe" and token == WABA_VERIFY_TOKEN:
            return challenge or ""
        
        return PlainTextResponse("forbidden", status_code=403)
    
    return wrapper

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from dotenv import load_dotenv
import traceback
import requests
from requests.auth import HTTPBasicAuth

from main import chain

load_dotenv()

app = FastAPI()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def download_twilio_media(media_url: str) -> str:
    try:
        response = requests.get(
            media_url,
            auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        )
        response.raise_for_status()

        import base64
        image_data = base64.b64encode(response.content).decode('utf-8')

        content_type = response.headers.get('Content-Type', 'image/jpeg')

        return f"data:{content_type};base64,{image_data}"
    
    except Exception as e:
        print(f"Error downloading media: {str(e)}")
        raise


def process_image(from_number: str, media_url: str):
    try:
        authenticated_url = download_twilio_media(media_url)
        result = chain.invoke(authenticated_url)
        send_whatsapp_message(from_number, str(result))
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"Processing error: {traceback.format_exc()}")
        send_whatsapp_message(from_number, error_msg)


@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        form_data = await request.form()
        
        from_number = form_data.get("From", "")
        num_media = int(form_data.get("NumMedia", 0))

        resp = MessagingResponse()
        
        if num_media > 0:
            media_url = form_data.get("MediaUrl0", "")
            media_content_type = form_data.get("MediaContentType0", "")
            
            if media_content_type.startswith("image/"):
                resp.message("Analyzing your image...")
                
                background_tasks.add_task(process_image, from_number, media_url)
            else:
                resp.message("Please send an image file (JPEG, PNG, etc.)")
        else:
            resp.message("Send an image to analyze traffic violations")
        
        return Response(content=str(resp), media_type="application/xml")
    
    except Exception as e:
        print(f"Webhook error: {traceback.format_exc()}")
        
        resp = MessagingResponse()
        resp.message(f"Error: {str(e)}")
        return Response(content=str(resp), media_type="application/xml")


def send_whatsapp_message(to_number: str, message: str):
    try:
        if not to_number.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_number}"
        
        if not TWILIO_WHATSAPP_NUMBER.startswith("whatsapp:"):
            from_number = f"whatsapp:{TWILIO_WHATSAPP_NUMBER}"
        else:
            from_number = TWILIO_WHATSAPP_NUMBER
        
        client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        
    except Exception as e:
        print(f"Error sending message: {traceback.format_exc()}")


@app.get("/")
async def root():
    return {"status": "running", "message": "Traffic Violation Detection API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
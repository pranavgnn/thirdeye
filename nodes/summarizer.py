from langchain.chat_models import init_chat_model
from pydantic import BaseModel

from .violations import ViolationsResult
from .vision import ImageAnalysisResult


try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


model = init_chat_model("google_genai:gemini-2.5-flash-lite")


class SummaryInput(BaseModel):
    analysis: ImageAnalysisResult
    violations: list[ViolationsResult]


def summarize(data) -> str:
    response = model.invoke([
        {
            "role": "system",
            "content": """You are an AI assistant summarizing traffic violation reports for an Indian traffic enforcement system.

You receive:
- `analysis`: Vision model output describing what was seen in the image (vehicle, license plate, possible violations, confidence, etc.)
- `violations`: A list of possible legal matches for the detected violation(s).

Your task is to create a short, factual, and reader-friendly message describing the result. 
This message will be sent to an end user or displayed on a dashboard.

Guidelines:
- Be concise, neutral, and professional.
- Always start with a summary of what was detected (vehicle, license plate, and violation status).
- If no vehicle is detected, clearly state that.
- If a violation is not confirmed or confidence is low, explain that the case requires manual review.
- If a violation is confirmed, include:
  - The violation name
  - The section of the Motor Vehicles Act
  - The fine amount in INR
- Avoid technical terms like “confidence score” unless needed for clarity.
- Never output JSON or lists — write natural text only.
- Do not add emojis, speculation, or extra commentary.

Keep the response under 100 words when possible."""
        },
        {
            "role": "user",
            "content": f"""You are given the following structured input for summarization:

Image Analysis Result:
{data["analysis"].model_dump_json(indent=2)}

Matched Violation Candidates:
{"\n".join([ v.model_dump_json(indent=2) for v in data["violations"]])}

Compose a short, human-readable message summarizing what was detected in the image and the violation outcome, following the style described in the system prompt."""
        }
    ])

    return response.content
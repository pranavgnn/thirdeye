from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from config import VISION_MODEL
from utils.lazy import structured_chat_model

class ImageAnalysisResult(BaseModel):
    vehicle_detected: bool = Field(description="Indicates if a vehicle is detected in the image.")
    is_violation: Optional[bool] = Field(description="Indicates if a traffic violation is present in the image, if vehicle is present.")
    license_plate: Optional[str] = Field(description="The license plate number of the vehicle involved in the violation in all caps and no spaces, if detectable.")
    title: Optional[str] = Field(description="A short title for the analysis result.")
    short_description: Optional[str] = Field(description="A brief description of the traffic violation(s), if any.")
    detailed_description: Optional[str] = Field(description="A detailed description of the traffic violation(s), if any.")
    violations: Optional[list[str]] = Field(description="A list of specific traffic violations detected in the image, if any.")
    confidence_score: float = Field(description="Confidence score of the entire analysis, ranging from 0 to 1.")


def get_structured_model():
    return structured_chat_model(VISION_MODEL, ImageAnalysisResult)


def analyse_image(image_url: str):
    message = {
        "role": "user",
        "content": [
            {"type": "text", "text": "Analyze the following image for traffic violations."},
            {"type": "image_url", "image_url": image_url},
        ],
    }
    return get_structured_model().invoke([message])


if __name__ == "__main__":
    analysis_result = analyse_image("https://images.hindustantimes.com/auto/img/2025/03/18/1600x900/Delhi_Traffic_Violation_1713763214287_1742269490008.jpg")
    print(analysis_result.model_dump_json(indent=2))
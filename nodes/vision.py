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
    license_plate: Optional[str] = Field(description="The license plate number of the vehicle involved in the violation in all caps and no spaces, if detectable. ONLY set this if confidence is high (>0.7). Return None if uncertain.")
    license_plate_confidence: float = Field(description="Confidence score specifically for license plate detection and reading accuracy, ranging from 0 to 1. Return 0 if no license plate detected.")
    is_india_location: bool = Field(description="Whether the image appears to be from India based on visual cues like vehicle types, license plate format, road signs, infrastructure, language on signs, etc.")
    location_confidence: float = Field(description="Confidence score for location determination (0 to 1). Consider factors like license plate format (Indian format: XX-00-XX-0000 or similar), Indian vehicle models, Hindi/regional language signs, Indian road infrastructure, etc.")
    title: Optional[str] = Field(description="A short title for the analysis result.")
    short_description: Optional[str] = Field(description="A brief description of the traffic violation(s), if any.")
    detailed_description: Optional[str] = Field(description="A detailed description of the traffic violation(s), if any.")
    violations: Optional[list[str]] = Field(description="A list of specific traffic violations detected in the image, if any.")
    confidence_score: float = Field(description="Confidence score of the entire analysis, ranging from 0 to 1.")


def get_structured_model():
    return structured_chat_model(VISION_MODEL, ImageAnalysisResult)


def analyse_image(image_url: str):
    system_prompt = """You are an expert AI traffic violation detection system specialized in analyzing images from Indian roads and traffic scenarios.

Your task is to:
1. **Detect Vehicles**: Identify if any vehicles are present in the image.
2. **Identify Location**: Determine if the image is from India by looking for:
   - Indian license plate formats (e.g., MH-02-XX-1234, DL-1C-1234, KA-01-AB-1234)
   - Indian vehicle models (Maruti, Tata, Mahindra, Bajaj, Hero, TVS, etc.)
   - Hindi or regional language text on signs, boards, or vehicles
   - Indian road infrastructure (specific road signs, barriers, markings)
   - Environmental cues (architecture, vegetation, street furniture common in India)
   - Be VERY confident (>99%) before marking as NOT India. When in doubt, assume it could be India.

3. **Detect License Plates**: 
   - Look for vehicle registration plates carefully
   - Indian plates typically have: State Code (2 letters) - District Code (2 digits) - Series (1-2 letters) - Number (4 digits)
   - ONLY report license plate text if you can read it with HIGH confidence (>70%)
   - If the plate is blurry, partially obscured, or unclear, set license_plate to None and license_plate_confidence low
   - Extract text in format: XX00XX0000 (no spaces or hyphens)

4. **Identify Traffic Violations**: Analyze the scene for violations such as:
   - Not wearing helmet (two-wheelers)
   - Not wearing seatbelt (four-wheelers)
   - Using mobile phone while driving
   - Wrong-side driving / Wrong direction
   - Jumping red light / Signal violation
   - Triple riding on two-wheelers
   - Overloading
   - Parking violations
   - Lane violations
   - Speed limit violations (if visible context suggests speeding)
   - No rear-view mirrors
   - Riding on footpath/pavement
   - Vehicle modifications

5. **Provide Accurate Descriptions**:
   - Short description: 1-2 sentences summarizing the scene
   - Detailed description: Comprehensive analysis including vehicle type, location in frame, specific violation details, environmental context
   - Be specific and factual
   - Do NOT mention license plate numbers in descriptions if confidence is low (<0.7)
   - Focus on observable facts, not assumptions

6. **Assess Confidence**:
   - Overall confidence should reflect certainty about the entire analysis
   - Consider image quality, visibility, angle, and clarity
   - Be conservative with confidence scores
   - Factor in lighting conditions, distance, and obstructions

Remember: Accuracy is critical. When uncertain, reflect that in your confidence scores."""

    message = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze the following image for traffic violations according to Indian traffic rules and regulations."},
                {"type": "image_url", "image_url": image_url},
            ],
        }
    ]
    return get_structured_model().invoke(message)


if __name__ == "__main__":
    analysis_result = analyse_image("https://images.hindustantimes.com/auto/img/2025/03/18/1600x900/Delhi_Traffic_Violation_1713763214287_1742269490008.jpg")
    print(analysis_result.model_dump_json(indent=2))
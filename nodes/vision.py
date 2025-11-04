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
1. Detect Vehicles: Identify if any vehicles are present in the image.
2. Identify Location (India or not):
    - Use plate formats, vehicle models, language on signs, and road features.
    - Be VERY confident (>99%) before marking as NOT India. When in doubt, do NOT mark as not India.
3. Detect License Plates:
    - Report license_plate only if HIGH confidence (>0.7). Otherwise set it to null and license_plate_confidence accordingly.
    - Output license plate in format XX00XX0000 (no spaces/hyphens).
4. Identify Traffic Violations:
    - Output violations as an array of ZERO OR MORE names chosen EXACTLY from this allowed list (use exact spelling and casing):
      [
         "Helmet Missing",
         "Triple Riding",
         "Seatbelt Not Worn",
         "Red Light Violation",
         "Wrong Side Driving (Lane Violation)",
         "No Number Plate",
         "Illegal Parking",
         "Vehicle Overloading",
         "Obstructive Parking",
         "Tampered Number Plate",
         "Improper Lane Discipline",
         "Driving Without Rearview Mirrors",
         "Unauthorized Modifications"
      ]
    - Only include a name if visible evidence supports it. If unsure, leave the array empty.
5. Provide Descriptions:
    - short_description: concise 1–2 sentences.
    - detailed_description: factual details; do NOT include low-confidence plate numbers.
6. Confidence:
    - Provide overall confidence conservatively. Reflect uncertainty.

Return data that conforms strictly to the response schema fields.
"""

     message = [
          {"role": "system", "content": system_prompt},
          {
                "role": "user",
                "content": [
                     {"type": "text", "text": "Analyze the following image for traffic violations according to Indian traffic rules and use the allowed violation names exactly as listed."},
                     {"type": "image_url", "image_url": image_url},
                ],
          },
     ]
     return get_structured_model().invoke(message)


if __name__ == "__main__":
    analysis_result = analyse_image("https://images.hindustantimes.com/auto/img/2025/03/18/1600x900/Delhi_Traffic_Violation_1713763214287_1742269490008.jpg")
    print(analysis_result.model_dump_json(indent=2))
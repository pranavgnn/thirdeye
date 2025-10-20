from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
import json
from .vision import ImageAnalysisResult

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DETECTABLE_VIOLATIONS = [
    {
        "id": 1,
        "name": "Helmet Missing",
        "category": "Safety Gear",
        "description": "Rider or pillion on a two-wheeler is not wearing a helmet.",
        "visible_indicators": ["two-wheeler", "human head", "no helmet object"],
        "fine_amount": 1000,
        "section": "194D(1)"
    },
    {
        "id": 2,
        "name": "Triple Riding",
        "category": "Occupancy",
        "description": "More than two people riding on a two-wheeler.",
        "visible_indicators": ["two-wheeler", "three persons detected"],
        "fine_amount": 2000,
        "section": "128(1)/177"
    },
    {
        "id": 3,
        "name": "Seatbelt Not Worn",
        "category": "Safety Gear",
        "description": "Driver or front passenger not wearing a seatbelt in a four-wheeler.",
        "visible_indicators": ["car front seat", "person detected", "no seatbelt strap visible"],
        "fine_amount": 1000,
        "section": "194B(1)"
    },
    {
        "id": 4,
        "name": "Red Light Violation",
        "category": "Signal Violation",
        "description": "Vehicle is stopped or moving beyond the stop line while traffic signal is red.",
        "visible_indicators": ["traffic signal showing red", "vehicle beyond stop line"],
        "fine_amount": 5000,
        "section": "184"
    },
    {
        "id": 5,
        "name": "Wrong Side Driving (Lane Violation)",
        "category": "Road Rule",
        "description": "Vehicle seen facing or driving in the wrong direction on a one-way road.",
        "visible_indicators": ["vehicle direction opposite lane marking or signage"],
        "fine_amount": 5000,
        "section": "184"
    },
    {
        "id": 6,
        "name": "No Number Plate",
        "category": "Identity Violation",
        "description": "Vehicle has missing, obscured, or tampered number plate.",
        "visible_indicators": ["vehicle detected", "license plate region empty or unclear"],
        "fine_amount": 3000,
        "section": "50/51/177"
    },
    {
        "id": 7,
        "name": "Illegal Parking",
        "category": "Parking",
        "description": "Vehicle parked in a no-parking zone, on footpath, or obstructing road/pedestrian path.",
        "visible_indicators": ["stationary vehicle", "road markings", "no parking signage or footpath"],
        "fine_amount": 500,
        "section": "122/177"
    },
    {
        "id": 8,
        "name": "Vehicle Overloading",
        "category": "Load Violation",
        "description": "Vehicle visibly carrying excessive goods or passengers beyond permitted capacity.",
        "visible_indicators": ["goods stacked high", "too many passengers visible"],
        "fine_amount": 20000,
        "section": "194(1)"
    },
    {
        "id": 9,
        "name": "Obstructive Parking",
        "category": "Parking",
        "description": "Vehicle parked in a way that blocks other vehicles, driveways, or crosswalks.",
        "visible_indicators": ["vehicle blocking another vehicle or gate"],
        "fine_amount": 500,
        "section": "122/177"
    },
    {
        "id": 10,
        "name": "Tampered Number Plate",
        "category": "Identity Violation",
        "description": "Number plate covered, painted, or altered to hide registration details.",
        "visible_indicators": ["plate present but illegible or blurred intentionally"],
        "fine_amount": 3000,
        "section": "50/51/177"
    },
    {
        "id": 11,
        "name": "Improper Lane Discipline",
        "category": "Road Rule",
        "description": "Vehicle straddling lane markings or encroaching into other lanes improperly.",
        "visible_indicators": ["vehicle crossing lane boundary without indication"],
        "fine_amount": 2000,
        "section": "184"
    },
    {
        "id": 12,
        "name": "Driving Without Rearview Mirrors",
        "category": "Safety Gear",
        "description": "Two-wheeler missing one or both rearview mirrors.",
        "visible_indicators": ["handlebar detected", "mirrors missing on both sides"],
        "fine_amount": 1000,
        "section": "177"
    },
    {
        "id": 13,
        "name": "Unauthorized Modifications",
        "category": "Vehicle Condition",
        "description": "Vehicle modified in violation of standard design, e.g., tinted windows, loud exhaust, or altered lights.",
        "visible_indicators": ["dark window tint", "unusual exhaust or lights"],
        "fine_amount": 5000,
        "section": "190(2)"
    }
]


def create_violation_document(violation: dict) -> Document:
    """Create a Document with violation text and complete JSON as metadata."""
    text_content = (
        f"{violation['name']} — {violation['description']} "
        f"Category: {violation['category']}. "
        f"Typically visible cues: {', '.join(violation['visible_indicators'])}. "
        f"Applies fine ₹{violation['fine_amount']} under Section {violation['section']}."
    )
    
    metadata = {
        "violation_data": json.dumps(violation),
        "id": violation["id"],
        "name": violation["name"],
        "category": violation["category"],
        "fine_amount": violation["fine_amount"],
        "section": violation["section"]
    }
    
    return Document(page_content=text_content, metadata=metadata)


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vector_store = InMemoryVectorStore(embeddings)
ids = vector_store.add_documents(documents=[create_violation_document(v) for v in DETECTABLE_VIOLATIONS])


class ViolationsResult(BaseModel):
    """Model to represent matched violation details."""

    id: int = Field(description="Unique identifier for the violation.")
    name: str = Field(description="Name of the traffic violation.")
    category: str = Field(description="Category of the traffic violation.")
    description: str = Field(description="Detailed description of the traffic violation.")
    fine_amount: int = Field(description="Fine amount associated with the violation in INR.")
    section: str = Field(description="Legal section under which the violation falls.")


class ValidationResult(BaseModel):
    """Model to represent validation results for violation matching."""

    is_valid: bool = Field(description="Indicates if the given violation is applicable for the given scenario.")


model = init_chat_model("google_genai:gemini-2.5-flash")
structured_model = model.with_structured_output(ValidationResult)


def validate_violation(violation_data: ViolationsResult, analysis_result: ImageAnalysisResult) -> bool:
    return structured_model.invoke([
        {
            "role": "system",
            "content": f"You are an expert traffic violation validator. Given the violation name '{violation_data.name}' and the analysis result, determine if the violation is valid."
        },
        {
            "role": "user",
            "content": f"Analysis Result: {analysis_result.model_dump_json()}\nIs the violation: {violation_data.model_dump_json()} applicable?"
        }
    ]).is_valid
     

def match_violations(analysis_result: ImageAnalysisResult) -> list[ViolationsResult]:
    """
    Match detected violations with the violation database.
    Returns a list of violation dictionaries with complete data.
    """
    if not analysis_result.vehicle_detected or not analysis_result.is_violation or analysis_result.violations is None:
        return []
    
    matched_violations = []
    
    for violation in analysis_result.violations:
        for doc in vector_store.similarity_search(violation, k=2):
            violation_data = ViolationsResult.model_validate(json.loads(doc.metadata["violation_data"]))

            if violation_data not in matched_violations and validate_violation(violation_data, analysis_result):
                matched_violations.append(ViolationsResult.model_validate(violation_data))
    
    return matched_violations


if __name__ == "__main__":
    analysis_result = {
        "vehicle_detected": True,
        "is_violation": True,
        "license_plate": "DL01AB1234",
        "short_description": "Helmet missing and triple riding detected.",
        "detailed_description": "The image shows a two-wheeler with three persons riding, none of whom are wearing helmets.",
        "violations": [
            "Helmet Missing",
            "Triple Riding"
        ],
        "confidence_score": 0.95
    }

    res = match_violations(ImageAnalysisResult.model_validate(analysis_result))

    print(res)
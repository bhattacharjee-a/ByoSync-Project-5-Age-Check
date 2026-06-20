import cv2
import sys
import time
import csv
import os
import uuid
import logging
from typing import Optional
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, UploadFile, File, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel 
load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import Model
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("api_requests.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
LOG_FILE = "requests_log.csv"
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
API_TOKEN = os.getenv("API_TOKEN")  
INCONCLUSIVE_MARGIN = 2
# FastAPI app
app = FastAPI(
    title="Age Check API",
    description="Privacy-preserving boolean age verification API.",
    version="1.0.0"
)
# Stores the last processed request (Admin only)
LAST_ADMIN_RESULT = None
# Security
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple token-based authentication"""
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials


# Pydantic schemas
class AgeCheckResponse(BaseModel):
    module: str
    is_above_threshold: Optional[bool]
    decision: str
    confidence: float
    latency_ms: float


class AgeResult(BaseModel):
    age: int
    confidence: float


def init_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp", "user_id", "image_name", "threshold", 
                "decision", "confidence", "latency_ms"
            ])


init_log_file()


def estimate_age(file_path: str) -> AgeResult:
    try:
        img = cv2.imread(file_path) 

        if img is None:
            raise ValueError("Could not read image")

        model = Model(img)

        face_crop = model.face_detect()

        age = Model(face_crop).age_detection()
        
        logger.info("=" * 50)
        logger.info("AGE CHECK DEBUG")
        logger.info(f"Predicted Age : {age:.2f}")
        logger.info("=" * 50)

        confidence = 0.90

        logger.info(
            f"Age estimation completed for {file_path}: age={age}, confidence={confidence}"
        )

        return AgeResult(
            age=round(age),
            confidence=confidence
        )

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        logger.exception("Unexpected error during age estimation")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during age estimation."
        )

def calculate_confidence(age: int, threshold: int) -> float:
    """
    Calculate confidence based on distance from threshold.
    Confidence increases as the predicted age moves farther away
    from the selected threshold.
    """

    gap = abs(age - threshold)

    confidence = 0.50 + (gap * 0.05)

    confidence = min(confidence, 0.99)

    return round(confidence, 2) 

def validate_image_quality(file_path: str):
    """
    Check if the uploaded image is blurry.
    Raises HTTPException if the image quality is too poor.
    """

    img = cv2.imread(file_path)

    if img is None:
        raise HTTPException(
            status_code=400,
            detail="Could not read uploaded image."
        )

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    logger.info(f"Blur Score: {blur_score:.2f}")

    BLUR_THRESHOLD = 80

    if blur_score < BLUR_THRESHOLD:
        raise HTTPException(
            status_code=400,
            detail="Image is blurry. Please upload a clearer image."
        )
    
def validate_file(file: UploadFile):
    """Validate file type and size"""
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    try:
        file_content = file.file.read(MAX_FILE_SIZE + 1)
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds {MAX_FILE_SIZE / (1024*1024)}MB limit"
            )
        file.file.seek(0)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")


def generate_unique_filename(original_filename: str) -> str:
    file_ext = Path(original_filename).suffix
    unique_id = uuid.uuid4().hex
    return f"{unique_id}{file_ext}"


def log_request(user_id: str, image_name: str, threshold: int, 
                decision: str, confidence: float, latency_ms: float):
    try:
        with open(LOG_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now(), user_id, image_name, threshold,
                decision, confidence, latency_ms
            ])
        logger.info(f"Request logged: user={user_id}, decision={decision}")
    except Exception as e:
        logger.error(f"Failed to log request: {str(e)}")


@app.get("/")
def home():
    return {"message": "Home", "project": "Age Check API"}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {
        "project": "Age Check API",
        "version": "0.2.0",
        "module": "backend",
        "features": [
            "async_uploads", "file_validation", "token_auth",
            "uuid_filenames", "proper_logging", "error_handling"
        ]
    }


@app.post("/check_age", response_model=AgeCheckResponse)
async def check_age(
    user_id: str = Form(...),
    threshold: int = Form(...),
    image: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    start_time = time.time()
    VALID_THRESHOLDS = {18, 21, 60}    
    if threshold not in VALID_THRESHOLDS:
        raise HTTPException(status_code=400, detail="Threshold must be 18, 21, or 60")
    
    try:
        validate_file(image)
    except HTTPException as e:
        logger.warning(f"File validation failed for {image.filename}: {e.detail}")
        raise e
    
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create uploads directory: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create uploads directory")
    
    unique_filename = generate_unique_filename(image.filename)
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            content = await image.read() 
            buffer.write(content)
        logger.info(f"Image saved: {file_path}")
        
        validate_image_quality(file_path) 
    except Exception as e:
        logger.error(f"Failed to save image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")
    
    try:
        result = estimate_age(file_path)
        age = result.age
        confidence = calculate_confidence(age, threshold)
    except HTTPException as e:
        try:
            os.remove(file_path)
            logger.info(f"Cleaned up failed upload: {file_path}")
        except:
            pass
        raise e
    
    margin = 2
    
    if abs(age - threshold) <= INCONCLUSIVE_MARGIN:
        decision = "inconclusive"
        is_above_threshold = None
    elif age > threshold:
        decision = "pass"
        is_above_threshold = True
    else:
        decision = "fail"
        is_above_threshold = False

    latency_ms = round((time.time() - start_time) * 1000, 2)

    log_request(
        user_id,
        image.filename,
        threshold,
        decision,
        confidence,
        latency_ms
    )
    
    global LAST_ADMIN_RESULT

    LAST_ADMIN_RESULT = {
        "estimated_age": round(age, 1),
        "confidence": confidence,
        "threshold": threshold,
        "decision": decision,
        "is_above_threshold": is_above_threshold,
        "latency_ms": latency_ms,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model_used": "Model (DeepFace)"
    }
    try:
        os.remove(file_path)
        logger.info(f"Deleted uploaded image: {file_path}")
    except Exception as e:
        logger.warning(f"Could not delete uploaded image: {e}")
    return AgeCheckResponse(
        module="age_check",
        is_above_threshold=is_above_threshold,
        decision=decision,
        confidence=confidence,
        latency_ms=latency_ms
    )
@app.get("/admin/latest")
def get_latest_admin_result(
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    global LAST_ADMIN_RESULT

    if LAST_ADMIN_RESULT is None:
        raise HTTPException(
            status_code=404,
            detail="No age check has been performed yet."
        )

    return LAST_ADMIN_RESULT

@app.get("/logs")
def get_logs(limit: int = 50):
    try:
        logs = []
        with open(LOG_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                logs.append(row)
            logs.reverse()
            return logs[:limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read logs: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

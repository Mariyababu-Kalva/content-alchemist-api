from fastapi import APIRouter, HTTPException, status
from backend.schemas.summary import SummaryRequest, SummaryResponse
from backend.services.transcript import extract_video_id
from backend.services.llm_service import get_summary
import os
import json
import hashlib

# Define a prefix so all endpoints in this file start with /api/v1
router = APIRouter(prefix="/api/v1", tags=["Summarization"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE_DIR = os.path.join(BASE_DIR, "cache")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_cache_filename(url: str):
    # Create a unique SHA256 hash of the URL for the filename
    url_hash = hashlib.sha256(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{url_hash}.json")

@router.post(
    "/summarize", 
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Summarize a YouTube Video",
    description="Takes a YouTube URL, fetches its transcript, and returns a structured AI summary."
)
async def summarize_video(request: SummaryRequest):
    # Check for cached version first
    cache_path = get_cache_filename(request.url)
    should_delete_corrupted = False

    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r") as f:
                cached_data = json.load(f)
            
            if cached_data.get("status") == "success" and len(cached_data.get("summary", "")) > 20:
                cached_data["from_cache"] = True
                return cached_data
            else:
                should_delete_corrupted = True
        except Exception:
            should_delete_corrupted = True

    if should_delete_corrupted:
        try:
            os.remove(cache_path)
        except PermissionError:
            pass

    # Extract the ID from the URL provided in the request body
    video_id = extract_video_id(request.url)
    is_short = "youtube.com/shorts/" in request.url
    if not video_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube URL. Please provide a valid link."
        )
    
    try:
        # Call the LLM service (which internally fetches the transcript)
        # This returns a SummaryResponse Pydantic object
        result = get_summary(video_id, is_short)
        
        # Convert Pydantic object to dictionary for JSON serialization
        result_dict = result.model_dump()

        # Ensure the flag is False for the stored file
        result_dict["from_cache"] = False
        
        # Save to the Lab Archives
        if result_dict.get("status") == "success" and len(result_dict.get("summary", "")) > 50:
            result_dict["from_cache"] = False
            from datetime import datetime
            result_dict["distilled_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(cache_path, "w") as f:
                json.dump(result_dict, f)
            
            return result_dict
        else:
            result_dict["from_cache"] = False
            return result_dict
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during summarization: {str(e)}"
        )

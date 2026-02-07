from fastapi import APIRouter, HTTPException, status
from backend.schemas.summary import SummaryRequest, SummaryResponse
from backend.services.transcript import extract_video_id
from backend.services.llm_service import get_summary

# Define a prefix so all endpoints in this file start with /api/v1
router = APIRouter(prefix="/api/v1", tags=["Summarization"])

@router.post(
    "/summarize", 
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Summarize a YouTube Video",
    description="Takes a YouTube URL, fetches its transcript, and returns a structured AI summary."
)
async def summarize_video(request: SummaryRequest):
    # Extract the ID from the URL provided in the request body
    video_id = extract_video_id(request.url)
    
    if not video_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube URL. Please provide a valid link."
        )
    
    try:
        # Call the LLM service (which internally fetches the transcript)
        # This returns a SummaryResponse Pydantic object
        result = get_summary(video_id)
        return result
        
    except Exception as e:
        # Handle errors (e.g., video has no transcripts or Gemini API is down)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during summarization: {str(e)}"
        )

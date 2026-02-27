from pydantic import BaseModel, Field
from typing import List, Optional

class SummaryRequest(BaseModel):
    """Schema for the incoming request."""
    url: str = Field(
        ..., 
        description="The full YouTube URL of the video you want to summarize.",
        examples=["https://www.youtube.com/watch?v=TOlL02slaag"]
    )

class SummaryResponse(BaseModel):
    """Schema for the structured AI output and API response."""
    status: str = Field(
        "success",
        description="The status of the transmutation: 'success' or 'error'."
    )
    video_id: str = Field(
        ..., 
        description="The unique 11-character YouTube video ID."
    )
    summary: str = Field(
        ..., 
        description="A comprehensive but concise paragraph summarizing the video's main theme."
    )
    key_points: List[str] = Field(
        default_factory=list,
        description="A list of the top 3-5 actionable takeaways from the video."
    )
    title: str = Field(
        ..., 
        description="A catchy, AI-generated title for this specific summary."
    )
    transcript: str = Field(
        ..., 
        description="The original transcript of the video"
    )
    is_short: bool = Field(
        False, 
        description="Flag to identify if the video is a YouTube Short"
    )
    from_cache: bool = Field(
        False,
        description='Flag to identify if the transmutation is cached'
    )
    distilled_at: Optional[str] = Field(
        None,
        description="The timestamp of when this summary was first created."
    )
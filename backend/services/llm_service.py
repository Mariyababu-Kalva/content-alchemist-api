from google import genai
from google.genai import types
from backend.core.config import settings
from backend.services.transcript import fetch_transcript
from backend.schemas.summary import SummaryResponse

# Load env and setup Client
client = genai.Client(
    api_key=settings.google_api_key,
    http_options=types.HttpOptions(api_version="v1alpha") # Force v1 to avoid 404s
)

def get_summary(video_id: str, is_short: bool)-> SummaryResponse:
    transcript = fetch_transcript(video_id)
    
    # We remove the conversational request and replace it with a command
    prompt = f"TRANSCRIPT: {transcript}"

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SummaryResponse, # Enforce the Pydantic structure
            system_instruction=(
                "You are a data extraction engine. Input: YouTube transcript. "
                "Output: JSON following the schema precisely. "
                "SCHEMA: { 'status': 'success' | 'error', 'title': string, 'summary': string, 'key_points': list, 'is_short': boolean, 'transcript': string } "
                "LOGIC: "
                "1. If a valid transcript is provided: set 'status' to 'success'. "
                "   The 'summary' must be a cohesive paragraph. "
                "   The 'key_points' must be 3-5 strings. "
                "   The 'title' must be a professional heading. "
                "2. If the input is empty, invalid, or says 'transcript unavailable': set 'status' to 'error'. "
                "   Set 'title' to 'Transmutation Failed'. "
                "   Set 'summary' to a brief explanation of why it failed. "
                "   Set 'key_points' to an empty list []. "
                "3. TRANSCRIPT HANDLING: If it is a Short, provide a polished 'transcript'. "
                "   Otherwise, return an empty string for 'transcript'."
            )
        )
    )

    # Access the pre-parsed Pydantic object
    result = response.parsed

    # Ensure the video_id is set (since Gemini only reads the transcript text)
    result.video_id = video_id
    
    if not is_short:
        result.transcript = ""
    
    result.is_short = is_short

    return result

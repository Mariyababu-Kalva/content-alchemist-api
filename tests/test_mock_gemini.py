import pytest
from backend.schemas.summary import SummaryResponse

# Constants for consistency
SUMMARIZE_URL = "/api/v1/summarize"
VALID_YT_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def test_successful_transmutation(client, mocker):
    """Test the API endpoint with a successful fake AI response."""
    mock_ai = mocker.patch("backend.routers.summarize.get_summary")
    
    # Ensure all fields required by SummaryResponse are present
    mock_ai.return_value = SummaryResponse(
        status="success", # This must be present
        title="Mock Video",
        summary="This is a successful mocked summary.",
        key_points=["Point 1"],
        is_short=False,
        transcript="", 
        video_id="dQw4w9WgXcQ"
    )
    
    response = client.post(SUMMARIZE_URL, json={"url": VALID_YT_URL})
    
    assert response.status_code == 200
    data = response.json()
    
    # Asserting against the JSON dictionary
    assert data.get("status") == "success"
    assert data.get("title") == "Mock Video"

def test_no_transcript_available(client, mocker):
    """Tests when the AI reports that no summary could be generated."""
    mock_ai = mocker.patch("backend.routers.summarize.get_summary")
    
    mock_ai.return_value = SummaryResponse(
        status="error", # This must be present
        title="Transmutation Failed",
        summary="No English transcript was available for this video.",
        key_points=[],
        is_short=False,
        transcript="",
        video_id="dQw4w9WgXcQ"
    )
    
    response = client.post(SUMMARIZE_URL, json={"url": VALID_YT_URL})
    
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "error"
    assert "No English transcript" in data.get("summary", "")

def test_quota_exhausted(client, mocker):
    """Test how the API handles a simulated AI Quota error (429)."""
    mock_ai = mocker.patch("backend.routers.summarize.get_summary")
    
    # We simulate the 429 error manually to test error handling
    mock_ai.side_effect = Exception("429 RESOURCE_EXHAUSTED")
    
    response = client.post(SUMMARIZE_URL, json={"url": VALID_YT_URL})
    
    assert response.status_code == 500
    assert "429" in response.json()["detail"]

def test_short_video_handling(client, mocker):
    """Tests if the Alchemist identifies a video as too short to distill."""
    mock_ai = mocker.patch("backend.routers.summarize.get_summary")
    
    mock_ai.return_value = SummaryResponse(
        status="success",
        title="Short Clip",
        summary="Brief distillation.",
        key_points=[],
        is_short=True,
        transcript="Polished transcript for short",
        video_id="dQw4w9WgXcQ"
    )
    
    response = client.post(SUMMARIZE_URL, json={"url": VALID_YT_URL})
    
    assert response.status_code == 200
    assert response.json()["is_short"] is True
    assert response.json()["transcript"] != ""
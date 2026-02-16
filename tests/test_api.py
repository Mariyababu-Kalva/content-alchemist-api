import pytest

# Define the endpoint once for easy maintenance
SUMMARIZE_URL = "/api/v1/summarize"

# --- CONNECTIVITY TESTS ---
def test_root_connection(client):
    """Verify the Alchemist is brewing at the root level."""
    response = client.get("/")
    assert response.status_code == 200
    # Adjusted to check for a successful response from health check
    assert response.json() is not None

# --- VALIDATION TESTS ---
def test_summarize_empty_body(client):
    """The Alchemist rejects an empty scroll (no JSON body)."""
    response = client.post(SUMMARIZE_URL, json={})
    # FastAPI returns 422 Unprocessable Entity for missing required fields (url)
    assert response.status_code == 422

def test_summarize_invalid_field(client):
    """The Alchemist rejects a request with the wrong keys."""
    # Sending 'link' instead of the expected 'url' defined in SummaryRequest
    response = client.post(SUMMARIZE_URL, json={"link": "https://youtu.be/test"})
    assert response.status_code == 422

def test_summarize_invalid_youtube_url(client):
    """Verify handling of strings that are not valid YouTube links."""
    # This hits the 'if not video_id' check in your summarize.py router
    response = client.post(SUMMARIZE_URL, json={"url": "https://google.com"})
    assert response.status_code == 400
    assert "Invalid YouTube URL" in response.json()["detail"]

# --- 3. ROUTING TESTS ---
def test_nonexistent_endpoint(client):
    """The Alchemist's lab has no such room."""
    response = client.get("/api/v1/forbidden-ritual")
    assert response.status_code == 404
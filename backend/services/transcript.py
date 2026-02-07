import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url: str) -> str:
    """
    Extracts the 11-character YouTube video ID from various URL formats.
    Handles: Standard, Shortened (youtu.be), Shorts, and Embed links.
    """
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

def fetch_transcript(video_id: str) -> str:
    """
    Retrieves the transcript for a given video ID and joins it into a single string.
    """
    try:
        # Note: We call get_transcript directly on the class (Industry standard)
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id)
        # Join the list of dictionaries into a single space-separated string
        full_text = ' '.join([i.text for i in transcript_list])
        return full_text
        
    except Exception as e:
        return f'Could not get transcript for video {video_id}: {e}'

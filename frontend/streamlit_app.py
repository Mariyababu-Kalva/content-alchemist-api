import streamlit as st
import requests
import time
from st_copy_to_clipboard import st_copy_to_clipboard # Import the new tool

# UI Branding
st.set_page_config(page_title="Content Alchemist", page_icon="🧪", layout="wide") # 'wide' helps with columns
st.title("🧪 Content Alchemist")
st.markdown("### The AI-Powered YouTube Distiller")

# User Input
video_url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

# Sidebar for Settings
with st.sidebar:
    st.header("Status")
    # We check if the backend is alive
    try:
        health = requests.get("http://127.0.0.1:8000/")
        if health.status_code == 200:
            st.success("Backend: Connected ✅")
    except:
        st.error("Backend: Disconnected ❌")

# Action Button
if st.button("Transmute to Summary"):
    if video_url:
        start_time = time.time()
        data = None
        with st.status("The Alchemist is at work...", expanded=True) as status:
            try:
                st.write("🔍 Extracting essence from YouTube...")

                # Send the URL to our FastAPI /api/v1/summarize endpoint
                payload = {"url": video_url}
                response = requests.post("http://127.0.0.1:8000/api/v1/summarize", json=payload)

                if response.status_code == 200:
                    st.write("⚗️ Distilling insights with Gemini AI...")
                    data = response.json()

                    duration = round(time.time() - start_time, 2)
                    status.update(label=f"Transmutation Complete in {duration}s!", state="complete", expanded=False)
                else:
                    status.update(label="Transmutation Failed!", state="error")
                    # Extract the error detail from the backend response
                    error_detail = response.json().get('detail', 'The transmutation failed.')

                    # Provide user-friendly guidance based on the error type
                    if "Invalid YouTube URL" in error_detail:
                        st.error("🧙‍♂️ **The Alchemist is puzzled!** That link doesn't seem to lead to a valid YouTube video. Please check the URL and try again.", icon="⚠️")
                    elif "quota" in error_detail.lower():
                        st.warning("⚖️ **Laboratory Overloaded!** We've reached our maximum AI power for now. Please try again in a few minutes.", icon="⏳")
                    else:
                        st.error(f"🧪 **Lab Error:** {error_detail}", icon="❌")
            except Exception as e:
                # Handle connection failures (e.g., backend server is down)
                status.update(label="Connection Error!", state="error")
                st.error("📡 **Communication Lost!** The Alchemist's lab is currently silent. Please ensure the transformation engine is active and try again.", icon="🔌")
        if data:
            # Show the Main Title
            st.header(data.get("title", "Summary Result"))
            st.divider()

            # --- ENHANCED TABBED LAYOUT ---
            # Organizes content into three distinct sections for better user engagement
            tab_summary, tab_points, tab_transcript = st.tabs([
                "📝 Summary", 
                "✨ Key Takeaways", 
                "📜 Transcript"
            ])

            with tab_summary:
                st.subheader("📝 Summary")
                summary_text = data.get("summary", "No summary available.")

                # Display text normally
                st.write(summary_text)

                # Add a "Copy to Clipboard"
                st.caption("Click the icon below to copy summary:")
                st_copy_to_clipboard(
                    summary_text, 
                    before_copy_label="📋 Copy Summary", 
                    after_copy_label="✅ Copied to Clipboard!"
                )

            with tab_points:
                st.subheader("✨ Key Takeaways")
                points = data.get("key_points", [])
                if points:
                    # Create a single string of points for the copy-to-clipboard functionality
                    points_string = "\n".join([f"• {p}" for p in points])

                    for point in points:
                        # Creates nice colored boxes for key points
                        st.info(point)

                    # Allow user to copy all key takeaways at once
                    st_copy_to_clipboard(
                        points_string,
                        before_copy_label="📋 Copy All Key Takeaways",
                        after_copy_label="✅ Takeaways Copied!"
                    )
                else:
                    st.info("The Alchemist didn't find specific key points.")

            with tab_transcript:
                # Logic to display transcript only for Shorts to keep UI clean
                if data.get("is_short"):
                    st.subheader("📜 Refined Transcript")
                    # Added a small note to explain the quality improvement
                    st.caption("The Alchemist has polished this scroll for readability while preserving every original word.")

                    transcript_text = data.get("transcript", "No transcript available.")

                    # Display transcript in a scrollable container for better UX
                    st.container(height=400).write(transcript_text)

                    # Copy tool for the full transcript
                    st_copy_to_clipboard(
                        transcript_text,
                        before_copy_label="📋 Copy Full Transcript",
                        after_copy_label="✅ Transcript Copied!"
                    )
                else:
                    # Informative note for long-form videos
                    st.info("💡 Transcript hidden for brevity as this is a long-form video.")
            # ------------------------------
    else:
        # Use a 'Toast' for a less intrusive warning when the input is empty
        st.toast("Please provide a YouTube link first!", icon="🧪")

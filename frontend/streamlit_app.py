import streamlit as st
import requests
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
        with st.spinner("Talking to the Alchemist's Lab..."):
            try:
                # Send the URL to our FastAPI /api/v1/summarize endpoint
                payload = {"url": video_url}
                response = requests.post("http://127.0.0.1:8000/api/v1/summarize", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Transmutation Complete!")
                    st.balloons()

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
                            st.subheader("📜 Transcript")
                            transcript_text = data.get("transcript", "No transcript available.")
                            
                            # Copy tool for the full transcript
                            st_copy_to_clipboard(
                                transcript_text,
                                before_copy_label="📋 Copy Full Transcript",
                                after_copy_label="✅ Transcript Copied!"
                            )
                            
                            # Display transcript in a scrollable container for better UX
                            st.container(height=400).write(transcript_text)
                        else:
                            # Informative note for long-form videos
                            st.info("💡 Transcript hidden for brevity as this is a long-form video.")
                    # ------------------------------

                else:
                    st.error(f"Error from Backend: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"Could not connect to API: {e}")
    else:
        st.warning("Please enter a link first!")

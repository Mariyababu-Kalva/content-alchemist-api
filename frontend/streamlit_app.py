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

                    # Two Column Layout
                    col1, col2 = st.columns([1.5, 1], gap="large")

                    with col1:
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

                    with col2:
                        st.subheader("✨ Key Takeaways")
                        points = data.get("key_points", [])
                        if points:
                            for point in points:
                                # Creates nice colored boxes for key points
                                st.info(point)
                        else:
                            st.info("The Alchemist didn't find specific key points.")
                    # ------------------------------

                else:
                    st.error(f"Error from Backend: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"Could not connect to API: {e}")
    else:
        st.warning("Please enter a link first!")

import streamlit as st
import requests

# UI Branding
st.set_page_config(page_title="Content Alchemist", page_icon="🧪")
st.title("🧪 Content Alchemist")
st.markdown("### The AI-Powered YouTube Distiller")

# User Input
video_url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

# Sidebar for Settings (Optional)
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
                # We send the URL to our FastAPI /api/v1/summarize endpoint
                payload = {"url": video_url}
                response = requests.post("http://127.0.0.1:8000/api/v1/summarize", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Transmutation Complete!")
                    # Show the Title
                    st.header(data.get("title", "Summary"))
                    
                    # 3. Show the Key Points as a Bulleted List
                    st.subheader("✨ Key Takeaways")
                    points = data.get("key_points", [])
                    if points:
                        for point in points:
                            st.write(f"- {point}")
                    else:
                        st.info("The Alchemist didn't find specific key points.")
                    st.balloons()
                else:
                    st.error(f"Error from Backend: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"Could not connect to API: {e}")
    else:
        st.warning("Please enter a link first!")

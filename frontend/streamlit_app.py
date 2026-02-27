import streamlit as st
import requests
import time
from st_copy_to_clipboard import st_copy_to_clipboard

# UI Branding
st.set_page_config(page_title="Content Alchemist", page_icon="🧪", layout="wide")
st.title("🧪 Content Alchemist")
st.markdown("### The AI-Powered YouTube Distiller")

# User Input
with st.form("alchemist_form", clear_on_submit=False):
    video_url = st.text_input(
        "Enter YouTube URL:", 
        placeholder="https://www.youtube.com/watch?v=..."
    )
    
    # In a form, you MUST use st.form_submit_button instead of st.button
    submit_button = st.form_submit_button("Transmute to Summary", type='primary')

# Initialize version variable
current_version = None

# Check if the backend is alive
with st.sidebar:
    st.header("Lab Status")

    col_status, col_refresh = st.columns([2, 1])
    start_check = time.time()
    try:
        health = requests.get(
            "https://127.0.0.1:8000/", 
            verify=False, 
            timeout=5, 
            allow_redirects=True
        )

        latency = round((time.time() - start_check) * 1000)

        if health.status_code == 200:
            data = health.json()
            current_version = data.get("version", "1.2.0-beta")

            with col_status:
                st.success("Connected ✅")
            
            with col_refresh:
                if st.button("🔄", help="Refresh connection status"):
                    st.rerun()

            st.metric(label="Server Latency", value=f"{latency} ms", delta="- Low" if latency < 150 else "+ High", delta_color="inverse")
        else:
            st.warning(f"Backend: Status {health.status_code} ⚠️")
            if st.button("🔄 Retry"):
                st.rerun()
    except Exception as e:
        with col_status:
            st.error("Offline ❌")
        with col_refresh:
            if st.button("🔄", help="Try to reconnect"):
                st.rerun()

    st.divider()

    # Lab Info
    st.subheader("📜 Lab Records")
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Version")
        version_display = f"v{current_version}" if current_version else "N/A"
        st.code(version_display)
    with col2:
        st.caption("Engine")
        engine_display = "Gemini 2.0" if current_version else "OFFLINE"
        st.code(engine_display)

# Action Button
if submit_button:
    if video_url:
        start_time = time.time()
        data = None
        with st.status("The Alchemist is at work...", expanded=True) as status:
            try:
                st.write("🔍 Extracting essence from YouTube...")
                payload = {"url": video_url}
                response = requests.post("https://127.0.0.1:8000/api/v1/summarize", json=payload, verify=False)

                if response.status_code == 200:
                    st.write("⚗️ Distilling insights with Gemini AI...")
                    data = response.json()

                    duration = round(time.time() - start_time, 2)
                    status.update(label=f"Transmutation Complete in {duration}s!", state="complete", expanded=False)
                else:
                    status.update(label="Transmutation Failed!", state="error")
                    
                    error_detail = response.json().get('detail', 'The transmutation failed.')
                    if "Invalid YouTube URL" in error_detail:
                        st.error("🧙‍♂️ **The Alchemist is puzzled!** That link doesn't seem to lead to a valid YouTube video. Please check the URL and try again.", icon="⚠️")
                    elif "quota" in error_detail.lower():
                        st.warning("⚖️ **Laboratory Overloaded!** We've reached our maximum AI power for now. Please try again in a few minutes.", icon="⏳")
                    else:
                        st.error(f"🧪 **Lab Error:** {error_detail}", icon="❌")

            except Exception as e:
                status.update(label="Connection Error!", state="error")
                st.error("📡 **Communication Lost!** The Alchemist's lab is currently silent. Please ensure the transformation engine is active and try again.", icon="🔌")
                data = None

        if data is not None:
            if data.get('status', 'error') == 'success':
                if data.get('from_cache'):
                    ts = data.get('distilled_at', 'an unknown time')
                    st.info(f"📜 **Alchemist's Record:** This essence was retrieved from the archives (Distilled: {ts}).")
                else:
                    st.success("✨ **Fresh Transmutation:** The Alchemist has just distilled this video for you!")

                # Show main title
                # - Organizes content into three distinct sections for better user engagement
                st.header(data.get('title', 'Summary Result'))
                st.divider()

                tab_summary, tab_points, tab_transcript = st.tabs([
                    "📝 Summary", 
                    "✨ Key Takeaways", 
                    "📜 Transcript"
                ])

                # Display summary:
                # - Allow user to copy summary
                with tab_summary:
                    st.subheader("📝 Summary")
                    st.write(data.get("summary"))

                    st.caption("Click the icon below to copy summary:")
                    st_copy_to_clipboard(
                        data.get("summary"), 
                        before_copy_label="📋 Copy Summary", 
                        after_copy_label="✅ Copied to Clipboard!"
                    )

                # Display key points:
                # - Create a single string of points for the copy-to-clipboard functionality
                # - Creates colored boxes for key points
                # - Allow user to copy all key takeaways at once
                with tab_points:
                    st.subheader("✨ Key Takeaways")
                    points = data.get("key_points", [])
                    if points:
                        points_string = "\n".join([f"• {p}" for p in points])

                        for point in points:
                            st.info(point)

                        st_copy_to_clipboard(
                            points_string,
                            before_copy_label="📋 Copy All Key Takeaways",
                            after_copy_label="✅ Takeaways Copied!"
                        )
                    else:
                        st.info("The Alchemist didn't find specific key points.")

                # Display transcript:
                # - Logic to display transcript only for Shorts to keep UI clean
                # - Display transcript in a scrollable container for better UX
                # - Add a small note to explain the quality improvement
                # - Allow user to copy transcript
                # - Informative note for long-form videos
                with tab_transcript:
                    if data.get("is_short"):
                        st.subheader("📜 Refined Transcript")
                        transcript_text = data.get("transcript", "[]")

                        if transcript_text:
                            st.container(height=250).write(transcript_text)

                            st.caption("The Alchemist has polished this scroll for readability while preserving every original word.")

                            st_copy_to_clipboard(
                                transcript_text,
                                before_copy_label="📋 Copy Full Transcript",
                                after_copy_label="✅ Transcript Copied!"
                            )
                        else:
                            st.info("📜 **Empty Scroll:** This video contains no spoken essence for the Alchemist to transmute.")
                    else:
                        st.info("💡 Transcript hidden for brevity as this is a long-form video.")
            else:
                fallback_title = "Transmutation Halted"
                st.warning(f"🧙‍♂️ **Alchemist Note:** {data.get('title', fallback_title)}")
                
                fallback_summary = "The laboratory was unable to extract the video's essence. Please check the URL."
                st.info(data.get("summary", fallback_summary))
    else:
        st.toast("Please provide a YouTube link first!", icon="🧪")

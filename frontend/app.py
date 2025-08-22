import streamlit as st
import requests
import json
from services import *
from UI import show_sidebar

st.set_page_config(page_title="Video Processing App", layout="centered")

# Default value so it's always defined
submit_button = False 
# Page Title
st.title("YouTube Video Transcription & Q/A Tool")


options=show_sidebar()


# YouTube link input
youtube_url = st.text_input(
    "Enter YouTube Video URL:",
    placeholder="https://www.youtube.com/watch?v=example"
)

if youtube_url:
    st.write(f"**Video URL Provided:** {youtube_url}")
    submit_button=st.button("Process Video")



if submit_button:
    if not youtube_url:
        st.error("⚠️ Please provide a YouTube URL first.")
    else:

        payload = {
            "url": youtube_url,
            "qa_option": options["generate_qa"],
            "stt_option": options["generate_subtitles"],
            "llm_name": options["model_name"],
            "stt_name": options["stt_model"],
            "stt_api_key": options["stt_apikey"],
            "llm_api_key": options["llm_apikey"]
        }

        # Run each selected service independently
        if options["download_audio"]:
            with st.spinner("Processing audio... ⏳"):
                get_audio(payload)

        if options["generate_qa"] or options["generate_subtitles"]:
            with st.spinner("Processing video... ⏳"):
                get_full_app(payload)

        # If none selected, still do something or warn
        if not (options["download_audio"] or options["generate_qa"] or options["generate_subtitles"]):
            with st.spinner("Processing video... ⏳"):
                get_full_app(payload)
 

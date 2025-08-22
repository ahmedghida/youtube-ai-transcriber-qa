import streamlit as st

def show_sidebar():
    st.sidebar.header("Options")

    download_audio = st.sidebar.checkbox("Download Audio")
    generate_subtitles = st.sidebar.checkbox("Use STT if no subtitle")
    generate_qa = st.sidebar.checkbox("Generate Q/A (requires text)")

    model_name = None
    needs_openai_key = False
    needs_groq_key = False

    if generate_qa:
        st.sidebar.subheader("LLM Model Selection")
        model_name = st.sidebar.selectbox(
            "Choose LLM Model:",
            ["gpt-5-nano", "gpt-4o-mini", "llama-3.3-70b-versatile"]
        )
        if model_name in ["gpt-5-nano", "gpt-4o-mini"]:
            needs_openai_key = True
        elif model_name == "llama-3.3-70b-versatile":
            needs_groq_key = True
            needs_openai_key = False  # LLaMA still needs OpenAI for STT

    stt_model = None
    if generate_subtitles:
        st.sidebar.subheader("STT Model Selection (for videos without subtitles)")
        stt_model = st.sidebar.selectbox(
            "Choose STT Model:",
            ["gpt-4o-mini-transcribe", "gpt-4o-transcribe", "whisper-1"]
        )
        needs_openai_key = True  # جميع موديلات STT تستخدم OpenAI

    # API key inputs
    openai_key = None
    groq_key = None

    if needs_openai_key:
        openai_key_label = "OpenAI API Key"
        if generate_qa and generate_subtitles:
            openai_key_label += " (for both LLM & STT)"
        elif generate_qa:
            openai_key_label += " (for LLM)"
        elif generate_subtitles:
            openai_key_label += " (for STT)"

        openai_key = st.sidebar.text_input(openai_key_label, type="password", placeholder="sk-...")

    if needs_groq_key:
        groq_key = st.sidebar.text_input("Groq API Key (for LLaMA)", type="password", placeholder="gsk-...")


    llm_apikey = None
    stt_apikey = None

    if generate_qa:
        if model_name == "llama-3.3-70b-versatile":
            llm_apikey = groq_key
        else:
            llm_apikey = openai_key

    if generate_subtitles:
        stt_apikey = openai_key

    return {
        "download_audio": download_audio,
        "generate_subtitles": generate_subtitles,
        "generate_qa": generate_qa,
        "model_name": model_name,
        "stt_model": stt_model,
        "llm_apikey": llm_apikey,
        "stt_apikey": stt_apikey
    }

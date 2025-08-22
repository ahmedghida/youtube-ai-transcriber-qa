import sys, os

import streamlit as st
from .utlis import request
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Config import Config



def get_audio(input_data: dict):
    """
    Call the backend audio endpoint and provide a download button in Streamlit.
    """
    response = request(route=f"{Config.BACKEND_URL}/download-audio", input=input_data)
    
    if response is not None:
        st.download_button(
            label="Download Audio",
            data=response,                  
            file_name="output.mp3",         
            mime="audio/mpeg"               
        )
        st.balloons()
    # else:
    #     st.warning("Audio request failed or returned no data.")

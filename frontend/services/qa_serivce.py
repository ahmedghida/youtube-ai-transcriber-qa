import sys, os
import requests
import streamlit as st
from .utlis import request
from .display import qa_result_display
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Config import Config



def get_full_app(input_data: dict):
    """
    Call the backend full-app endpoint and display results in Streamlit.
    """
    response = request(route=f"{Config.BACKEND_URL}/full-app", input=input_data)
    
    if response is not None:
        qa_result_display(response)
        st.balloons()
    # else:
    #     st.warning("No data returned from the backend.")



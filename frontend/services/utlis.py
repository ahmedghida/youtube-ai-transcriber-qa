import json
import requests
import streamlit as st

def request(route: str, input: dict):
    try:
        response = requests.post(route, json=input)
        response.raise_for_status()  # Raise error for bad responses

        # If route ends with /download-audio → treat as audio
        if route.endswith("/download-audio"):
            return response.content  # raw bytes

        # Otherwise → JSON endpoint
        return response.json()  # requests can decode JSON automatically

    except Exception as e:
        st.warning(f"Request failed: {e}")
        return None
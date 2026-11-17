import os

import streamlit as st


def get_api_url() -> str:
    if os.getenv("API_URL"):
        return os.getenv("API_URL").rstrip("/")
    try:
        return st.secrets["API_URL"].rstrip("/")
    except Exception:
        return "http://127.0.0.1:8001"


API_URL = get_api_url()
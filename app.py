import streamlit as st
import time
import urllib.parse

# --- ULTRA-COMPACT STYLING ---
st.set_page_config(page_title="Flames Master v1.8", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    /* Force buttons to be smaller and tighter */
    div.stButton > button { 
        background-color: #1a1a1a; 
        color: #FFD700; 
        border: 1px solid #FFD700; 
        border-radius: 4px; 
        padding: 0px 4px !important;
        font-size: 0.75em !important;
        height: 28px !important;
    }
    .goal-text { font-size: 0.7em


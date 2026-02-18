import streamlit as st
import time
import urllib.parse

# --- ULTRA-COMPACT STYLING ---
st.set_page_config(page_title="Flames Master v2.0", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
    div.stButton > button { 
        background-color: #1a1a1a; color: #FFD700; border: 1px solid #FFD700; 
        border-radius: 4px; padding: 0px !important; font-size: 0.75em !important; height: 26px !important;
    }
    .goal-text { font-size: 0.75em; color: #FFD700; margin-top: 4px; line-height: 1; }
    .stDivider { margin: 0.2rem 0 !important; }
    </style>
    """, unsafe_allow_html=True)

if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

def balance_minutes(target_

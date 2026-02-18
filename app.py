import streamlit as st
import time
import urllib.parse

# --- STYLING & CONFIG ---
st.set_page_config(
    page_title="Flames Master v1.1", 
    layout="centered"
)

# Subtle Black & Yellow Sideline Theme
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    div.stButton > button { 
        background-color: #1a1a1a; 
        color: #FFD700; 
        border: 1px solid #FFD700; 
        border-radius: 8px; 
        font-weight: bold; 
    }
    div.stButton > button:hover { background-color: #FFD700; color: black; }
    .gas-alert { color: #ff4b4b; font-weight: bold; font-size: 0.8em; }
    .version-tag { color: #555; font-size: 0.7em; text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- INIT STATE ---
if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

# --- PAGE 1: SETUP ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Setup")
    try: st.image("logo.png", width=150)
    except: st.write("🔥")
    
    roster_input = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    
    if st.button("START GAME", use_container_width=True):
        names = [n.strip() for n in roster_input.split(",") if n.strip()]
        st.session_state.players = {n: {
            "h1": 0, "h2": 0, "status": "On Court" if i < 5 else "Bench", 
            "target": 100/len(names), "consecutive": 0
        } for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- PAGE 2: GAME ---
elif st.session_state.page == "Game":
    st.subheader(f"Flames Rotation: {st.session_state.game['half

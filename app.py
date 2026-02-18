import streamlit as st
import time
import urllib.parse

# --- STYLING ---
st.set_page_config(page_title="Flames Master Stable", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    div.stButton > button { 
        background-color: #1a1a1a; color: #FFD700; border: 1px solid #FFD700; 
        border-radius: 8px; font-weight: bold; 
    }
    .goal-text { font-size: 0.9em; font-weight: bold; color: #FFD700; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INIT STATE ---
if "page" not in st.session_state: 
    st.session_state.page = "Setup"
if "players" not in st.session_state: 
    st.session_state.players = {}
if "game" not in st.session_state: 
    st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

# SMART BALANCING LOGIC
def balance_minutes(target_player, adjustment):
    others = [p for p in st.session_state.players if p != target_player]
    if not others:
        return
    per_player_adj = adjustment / len(others)
    st.session_state.players[target_player]["target"] += adjustment
    for p in others:
        st.session_state.players[p]["target"] -= per_player_adj

# --- PAGE 1: SETUP ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Setup")
    try: 
        st.image("logo.png", width=120)
    except: 
        st.write("🔥")
    
    roster_input = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    
    if st.button("CALCULATE & START EVEN", use_container_width=True):
        names = [n.strip() for n in roster_input.split(",") if n.strip()]
        count = len(names)
        even_share = 100 / count if count > 0 else 0 
        st.session_state.players = {n: {
            "h1": 0, "h2": 0, "status": "On Court" if i < 5 else "Bench", 
            "target": even_share, "consecutive": 0
        } for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- PAGE 2: GAME ---
elif st.session_state.page == "Game":
    col_l, col_r = st.columns([1, 4])
    with col_l:
        try:
            st.image("logo.png", width=80)
        except:
            st.write("🔥")
    with col_r:
        st.subheader(f"Flames Rotation: {st.session_state.game['half']}")
    
    m, s = divmod(st.session_state.game["clock"], 60)
    st.markdown(f"

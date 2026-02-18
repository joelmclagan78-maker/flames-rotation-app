import streamlit as st
import time
import urllib.parse

# --- ULTRA-COMPACT STYLING ---
st.set_page_config(page_title="Flames Master v1.9", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    /* Shave off every pixel of extra space */
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
    div.stButton > button { 
        background-color: #1a1a1a; 
        color: #FFD700; 
        border: 1px solid #FFD700; 
        border-radius: 4px; 
        padding: 0px !important;
        font-size: 0.75em !important;
        height: 26px !important;
    }
    .goal-text { font-size: 0.75em; color: #FFD700; margin-top: 4px; }
    .stDivider { margin: 0.3rem 0 !important; }
    h3, h1 { margin-bottom: 0px !important; padding-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

def balance_minutes(target_player, adjustment):
    others = [p for p in st.session_state.players if p != target_player]
    if not others: return
    per_player_adj = adjustment / len(others)
    st.session_state.players[target_player]["target"] += adjustment
    for p in others:
        st.session_state.players[p]["target"] -= per_player_adj

# --- SETUP PAGE ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Setup")
    try: st.image("logo.png", width=80)
    except: st.write("🔥")
    roster_input = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    if st.button("CALCULATE & START EVEN", use_container_width=True):
        names = [n.strip() for n in roster_input.split(",") if n.strip()]
        even_share = 100 / len(names) if names else 0 
        st.session_state.players = {n: {"h1": 0, "h2": 0, "status": "On Court" if i < 5 else "Bench", "target": even_share, "consecutive": 0} for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- GAME PAGE: MAXIMIZED FOR MOBILE ---
elif st.session_state.page == "Game":
    col_l, col_t, col_s = st.columns([1, 2, 2])
    with col_l:
        try: st.image("logo.png", width=35)
        except: st.write("🔥")
    with col_t:
        m, s = divmod(st.session_state.game["clock"], 60)
        st.write(

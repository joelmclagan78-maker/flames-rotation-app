import streamlit as st
import time
import urllib.parse

# --- ULTRA-COMPACT MOBILE STYLING ---
st.set_page_config(page_title="Flames Master v2.2", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    /* Force the app to take up the full width and remove padding */
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
    /* Shrink buttons to their absolute minimum height */
    div.stButton > button { 
        background-color: #1a1a1a; color: #FFD700; border: 1px solid #FFD700; 
        border-radius: 4px; padding: 0px !important; font-size: 0.7em !important; height: 24px !important;
    }
    /* Compact text for minutes and goals */
    .goal-text { font-size: 0.7em; color: #FFD700; margin-top: 5px; line-height: 1; white-space: nowrap; }
    .stDivider { margin: 0.1rem 0 !important; }
    /* Remove vertical spacing between columns */
    [data-testid="column"] { padding: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

# FIXED: Corrected all bracket/parenthesis issues
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
    try: st.image("logo.png", width=60)
    except: st.write("🔥")
    roster_input = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    if st.button("CALCULATE & START EVEN", use_container_width=True):
        names = [n.strip() for n in roster_input.split(",") if n.strip()]
        even_share = 100 / len(names) if names else 0 
        st.session_state.players = {n: {"h1": 0, "h2": 0, "status": "On Court" if i < 5 else "Bench", "target": even_share, "consecutive": 0} for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- GAME PAGE: ONE-SCREEN GRID ---
elif st.session_state.page == "Game":
    col_l, col_t, col_s = st.columns([1, 2, 2])
    with col_l:
        try: st.image("logo.png", width=30)
        except: st.write("🔥")
    with col_t:
        m, s = divmod(st.session_state.game["clock"], 60)
        st.write(f"**{m:02d}:{s:02d}**") # FIXED: Closed bracket
    with col_s:
        st.write(f"**{st.session_state.game['half']}**")

    c1, c2, c3 = st.columns(3)
    if c1.button("START"): st.session_state.game["running"] = True
    if c2.button("STOP"): st.session_state.game["running"] = False
    if c3.button("NEXT"):
        st.session_state.game["half"] = "2nd Half"; st.session_state.game["clock"] = 1200; st.rerun()

    st.divider()
    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    
    # GRID: Status/Name (4) | Stats (3) | Minus


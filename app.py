import streamlit as st
import time
import urllib.parse

# --- ULTRA-COMPACT STYLING ---
st.set_page_config(page_title="Flames Master v2.1", layout="centered")
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

# FIXED: Added missing closing parenthesis
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

# --- GAME PAGE: COMPACT GRID ---
elif st.session_state.page == "Game":
    col_l, col_t, col_s = st.columns([1, 2, 2])
    with col_l:
        try: st.image("logo.png", width=35)
        except: st.write("🔥")
    with col_t:
        m, s = divmod(st.session_state.game["clock"], 60)
        st.write(f"**{m:02d}:{s:02d}**")
    with col_s:
        st.write(f"**{st.session_state.game['half']}**")

    c1, c2, c3 = st.columns(3)
    if c1.button("START"): st.session_state.game["running"] = True
    if c2.button("STOP"): st.session_state.game["running"] = False
    if c3.button("NEXT"):
        st.session_state.game["half"] = "2nd Half"; st.session_state.game["clock"] = 1200; st.rerun()

    st.divider()
    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    
    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        c_name, c_stats, c_m, c_p = st.columns([4, 3, 1, 1])
        
        gas = "⚠️" if (is_on and data["consecutive"] > 360) else ""
        if c_name.button(f"{'✅' if is_on else '🪑'} {name}{gas}", key=f"b_{name}", use_container_width=True):
            data["status"] = "Bench" if is_on else "On Court"; data["consecutive"] = 0; st.rerun()
        
        goal_color = "red" if (is_on and data[half_key] >= data["target"]) else "#FFD700"
        c_stats.markdown(f"<p style='color: {goal_color};' class='goal-text'>{int(data[half_key])}m/{data['target']:.0f}m</p>", unsafe_allow_html=True)

        if c_m.button("-", key=f"m_{name}"): balance_minutes(name, -1); st.rerun()
        if c_p.button("+", key=f"p_{name}"): balance_minutes(name, 1); st.rerun

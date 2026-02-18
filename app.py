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
if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

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
    # FIXED: Added missing quote and variable name
    st.title("🏀 Flames Setup")
    try: st.image("logo.png", width=120)
    except: st.write("🔥")
    
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
    st.subheader(f"Flames Rotation: {st.session_state.game['half']}")
    
    m, s = divmod(st.session_state.game["clock"], 60)
    st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{m:02d}:{s:02d}</h1>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if c1.button("START"): st.session_state.game["running"] = True
    if c2.button("STOP"): st.session_state.game["running"] = False
    if c3.button("NEXT"):
        st.session_state.game["half"] = "2nd Half"; st.session_state.game["clock"] = 1200; st.rerun()

    st.divider()

    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        gas_warning = " ⚠️ GAS LOW" if (is_on and data["consecutive"] > 360) else ""
        
        col_name, col_goal, col_m, col_p = st.columns([3, 2, 1, 1])
        
        if col_name.button(f"{'✅' if is_on else '🪑'} {name}{gas_warning}", key=f"btn_{name}", use_container_width=True):
            data["status"] = "Bench" if is_on else "On Court"
            data["consecutive"] = 0
            st.rerun()
        
        goal_color = "red" if (is_on and data[half_key] >= data["target"]) else "#FFD700"
        col_goal.markdown(f"<p style='color: {goal_color};' class='goal-text'>{int(data[half_key])}m / {data['target']:.1f}m</p>", unsafe_allow_html=True)

        if col_m.button("➖", key=f"m_{name}"):
            balance_minutes(name, -1)
            st.rerun()
        if col_p.button("➕", key=f"a_{name}"):
            balance_minutes(name, 1)
            st.rerun()

    st.divider()
    subject = urllib.parse.quote("Flames Feedback")
    mail_link = f"mailto:docdvba@mary

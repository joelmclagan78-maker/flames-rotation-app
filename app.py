import streamlit as st
import time

# --- STYLING & INIT ---
st.set_page_config(page_title="Flames Smart Rotation", layout="centered")

# Subtle Black & Yellow Theme (Better visibility)
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    div.stButton > button { 
        background-color: #1a1a1a; 
        color: #FFD700; 
        border: 1px solid #FFD700;
        border-radius: 8px; 
    }
    div.stButton > button:hover { background-color: #FFD700; color: black; }
    /* Target text styling */
    .goal-text { font-size: 0.9em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

def balance_minutes(target_player, adjustment):
    """Smart Balancing: redistributes time among other players."""
    others = [p for p in st.session_state.players if p != target_player]
    if not others: return
    per_player_adj = adjustment / len(others)
    st.session_state.players[target_player]["target"] += adjustment
    for p in others:
        st.session_state.players[p]["target"] -= per_player_adj

# --- PAGE 1: SETUP ---
if st.session_state.page == "Setup":
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        try: st.image("logo.png", width=80)
        except: st.write("🏀")
    with col_title:
        st.title("Flames Smart Setup")
    
    roster_input = st.text_area("Enter Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    
    if st.button("CALCULATE & START EVEN", use_container_width=True):
        names = [n.strip() for n in roster_input.split(",") if n.strip()]
        count = len(names)
        even_share = 100 / count if count > 0 else 0 
        st.session_state.players = {n: {
            "h1": 0, "h2": 0, "status": "On Court" if i < 5 else "Bench", 
            "target": even_share, "stints": 0 if i < 5 else 1
        } for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- PAGE 2: GAME ---
elif st.session_state.page == "Game":
    # Header with Logo
    col_l, col_h = st.columns([1, 5])
    with col_l:
        try: st.image("logo.png", width=60)
        except: st.write("🔥")
    with col_h:
        st.subheader(f"Flames Rotation: {st.session_state.game['half']}")

    m, s = divmod(st.session_state.game["clock"], 60)
    timer_color = "#FFD700" if st.session_state.game["running"] else "red"
    st.markdown(f"<h1 style='text-align: center; color: {timer_color}; margin-top: -20px;'>{m:02d}:{s:02d}</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    if c1.button("START", use_container_width=True): st.session_state.game["running"] = True
    if c2.button("STOP", use_container_width=True): st.session_state.game["running"] = False
    if c3.button("HALF", use_container_width=True):
        st.session_state.game["half"] = "2nd Half"
        st.session_state.game["clock"] = 1200
        st.rerun()

    st.divider()
    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    
    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        over_time = data[half_key] >= data["target"]
        
        col_main, col_goal, col_m, col_p = st.columns([3, 2, 1, 1])
        
        # Action Button (Black with yellow text, turns Solid Yellow when On Court)
        btn_style = "primary" if is_on else "secondary"
        btn_label = f"{'✅' if is_on else '🪑'} {name}: {int(data[half_key])}m (Off: {data['stints']})"
        
        if col_main.button(btn_label, key=f"p_{name}", type=btn_style, use_container_width=True):
            if is_on:
                st.session_state.players[name]["status"] = "Bench"
                st.session_state.players[name]["stints"] += 1
            else:
                st.session_state.players[name]["status"] = "On Court"
            st.rerun()

        # Goal display - turns Red only if player is over their limit
        goal_color = "red" if (is_on and over_time) else "#FFD700"
        col_goal.markdown(f"<p style='color: {goal_color}; margin-top: 10px;' class='goal-text'>Goal: {data['target']:.1f}m</p>", unsafe_allow_html=True)

        if col_m.button("➖", key=f"m_{name}"):
            balance_minutes(name, -1)
            st.rerun()
        if col_p.button("➕", key=f"a_{name}"):
            balance_minutes(name, 1)
            st.rerun()

    # --- ENGINE ---
    if st.session_state.game["running"] and st.session_state.game["clock"] > 0:
        time.sleep(1)
        st.session_state.game["clock"] -= 1
        for name, data in st.session_state.players.items():
            if data["status"] == "On Court":
                data[half_key] += 1/60
        st.rerun()

    if st.button("⬅️ RESET"):
        st.session_state.page = "Setup"
        st.rerun()

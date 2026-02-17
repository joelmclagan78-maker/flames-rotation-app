import streamlit as st
import time

# --- STYLING & INIT ---
st.set_page_config(page_title="Flames Smart Rotation", layout="centered")
st.markdown("<style>body {background-color: black; color: white;}</style>", unsafe_allow_html=True)

if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

def balance_minutes(target_player, adjustment):
    """Zero-sum redistribution: if one gains time, others lose it evenly."""
    others = [p for p in st.session_state.players if p != target_player]
    if not others: return
    per_player_adj = adjustment / len(others)
    st.session_state.players[target_player]["target"] += adjustment
    for p in others:
        st.session_state.players[p]["target"] -= per_player_adj

# --- PAGE 1: SETUP ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Smart Setup")
    roster_input = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    
    if st.button("CALCULATE & START EVEN", use_container_width=True):
        names = [n.strip() for n in roster_input.split(",") if n.strip()]
        count = len(names)
        even_share = 100 / count if count > 0 else 0 
        
        # Start: First 5 on court, others on bench with 1 stint
        st.session_state.players = {n: {
            "h1": 0, "h2": 0, "status": "On Court" if i < 5 else "Bench", 
            "target": even_share, "stints": 0 if i < 5 else 1
        } for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- PAGE 2: GAME ---
elif st.session_state.page == "Game":
    st.title(f"🔥 {st.session_state.game['half']}")
    
    m, s = divmod(st.session_state.game["clock"], 60)
    st.metric("Time Remaining", f"{m:02d}:{s:02d}")
    
    c1, c2, c3 = st.columns(3)
    if c1.button("START"): st.session_state.game["running"] = True
    if c2.button("STOP"): st.session_state.game["running"] = False
    if c3.button("NEXT HALF"):
        st.session_state.game["half"] = "2nd Half"
        st.session_state.game["clock"] = 1200
        st.rerun()

    st.divider()

    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    
    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        
        # Grid: [Rotation & Stints] [Goal] [Adjustments]
        col_main, col_goal, col_m, col_p = st.columns([3, 2, 1, 1])
        
        btn_label = f"{'✅' if is_on else '🪑'} {name}: {int(data[half_key])}m (Off: {data['stints']})"
        if col_main.button(btn_label, key=f"p_{name}", type="primary" if is_on else "secondary", use_container_width=True):
            if is_on: # Moving to bench
                st.session_state.players[name]["status"] = "Bench"
                st.session_state.players[name]["stints"] += 1
            else: # Moving to court
                st.session_state.players[name]["status"] = "On Court"
            st.rerun()

        col_goal.write(f"Goal: {data['target']:.1f}m")

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

    if st.button("⬅️ RESET ROSTER"):
        st.session_state.page = "Setup"
        st.rerun()

import streamlit as st
import time

# --- STYLING & INIT ---
st.set_page_config(page_title="Flames Smart Rotation", layout="centered")
st.markdown("<style>body {background-color: black; color: white;}</style>", unsafe_allow_html=True)

if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

def balance_minutes(target_player, adjustment):
    """Zero-sum redistribution of court time."""
    others = [p for p in st.session_state.players if p != target_player]
    if not others: return
    per_player_adj = adjustment / len(others)
    st.session_state.players[target_player]["target"] += adjustment
    for p in others:
        st.session_state.players[p]["target"] -= per_player_adj

# --- PAGE 1: SETUP ---
if st.session_state.page == "Setup":
    st.title("🏀 Smart Team Setup")
    roster_input = st.text_area("Roster (comma separated)", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    
    if st.button("CALCULATE & START EVEN", use_container_width=True):
        names = [n.strip() for n in roster_input.split(",") if n.strip()]
        count = len(names)
        even_share = 100 / count if count > 0 else 0 
        
        # Initialize players with Bench Stints at 0
        st.session_state.players = {n: {
            "h1": 0, "status": "On Court" if i < 5 else "Bench", 
            "target": even_share, "stints": 0 if i < 5 else 1
        } for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- PAGE 2: GAME ---
elif st.session_state.page == "Game":
    st.title(f"🔥 {st.session_state.game['half']}")
    
    m, s = divmod(st.session_state.game["clock"], 60)
    st.metric("Time Remaining", f"{m:02d}:{s:02d}")
    
    c1, c2 = st.columns(2)
    if c1.button("START"): st.session_state.game["running"] = True
    if c2.button("STOP"): st.session_state.game["running"] = False

    st.divider()

    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        
        # Added 'Stints' display to the main column
        col_main, col_target, col_minus, col_plus = st.columns([3, 2, 1, 1])
        
        # Tapping to Bench increments the counter
        btn_label = f"{'✅' if is_on else '🪑'} {name}: {int(data['h1'])}m (Off: {data['stints']})"
        if col_main.button(btn_label, key=f"p_{name}", use_container_width=True):
            if is_on: # Moving to bench
                st.session_state.players[name]["status"] = "Bench"
                st.session_state.players[name]["stints"] += 1
            else: # Moving to court
                st.session_state.players[name]["status"] = "On Court"
            st.rerun()

        col_target.write(f"Goal: {data['target']:.1f}m")

        if col_minus.button("➖", key=f"m_{name}"):
            balance_minutes(name, -1)
            st.rerun()
        if col_plus.button("➕", key=f"a_{name}"):
            balance_minutes(name, 1)
            st.rerun()

    # TIMER ENGINE
    if st.session_state.game["running"] and st.session_state.game["clock"] > 0:
        time.sleep(1)
        st.session_state.game["clock"] -= 1
        for name, data in st.session_state.players.items():
            if data["status"] == "On Court":
                data["h1"] += 1/60
        st.rerun()

    if

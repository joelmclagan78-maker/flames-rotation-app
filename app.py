import streamlit as st
import time

# --- STYLING & INIT ---
st.set_page_config(page_title="Flames Rotation Master", layout="centered")
st.markdown("<style>body {background-color: black; color: white;}</style>", unsafe_allow_html=True)

if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

# --- PAGE 1: SETUP (THE PRE-GAME) ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Team Setup")
    roster_input = st.text_area("Enter Player Names (comma separated)", 
                                value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    
    col_s1, col_s2 = st.columns(2)
    
    # Restored 'Even Time' logic for the starting 5
    if col_s1.button("START WITH EVEN ROTATION", use_container_width=True):
        names = [n.strip() for n in roster_input.split(",") if n.strip()]
        st.session_state.players = {n: {"h1": 0, "h2": 0, "status": "On Court" if i < 5 else "Bench"} 
                                    for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

    if col_s2.button("MANUAL START (ALL BENCH)", use_container_width=True):
        names = [n.strip() for n in roster_input.split(",") if n.strip()]
        st.session_state.players = {n: {"h1": 0, "h2": 0, "status": "Bench"} for n in names}
        st.session_state.page = "Game"
        st.rerun()

# --- PAGE 2: GAME (THE SIDELINE) ---
elif st.session_state.page == "Game":
    st.title(f"🔥 {st.session_state.game['half']}")
    
    # 1. VISUAL CLOCK
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

    # 2. THE ROTATION BOARD
    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    
    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        # Large buttons for coaching on the move
        col_btn, col_adj = st.columns([4, 1])
        
        btn_text = f"{'✅ ON COURT' if is_on else '🪑 BENCH'} | {name} ({int(data[half_key])}m)"
        if col_btn.button(btn_text, key=f"p_{name}", type="primary" if is_on else "secondary", use_container_width=True):
            st.session_state.players[name]["status"] = "Bench" if is_on else "On Court"
            st.rerun()
            
        # Quick-fix minutes buttons
        if col_adj.button("➕", key=f"add_{name}"):
            st.session_state.players[name][half_key] += 1
            st.rerun()

    # 3. AUTO-TIMER ENGINE
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

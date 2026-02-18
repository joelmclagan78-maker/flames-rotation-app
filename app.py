import streamlit as st
import time

# --- STABLE MOBILE STYLING ---
st.set_page_config(page_title="Flames Master v4.1", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    .block-container { padding: 0.5rem !important; }
    div.stButton > button { 
        background-color: #1a1a1a; color: #FFD700; border: 1px solid #FFD700; 
        border-radius: 4px; font-weight: bold; width: 100%; height: 35px !important;
    }
    .goal-text { font-size: 1em; color: #FFD700; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- INIT STATE ---
if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

# REBALANCING ENGINE: Verified math
def rebalance(target_player, adjustment):
    others = [p for p in st.session_state.players if p != target_player]
    if not others: return
    st.session_state.players[target_player]["target"] += adjustment
    adj_per_person = adjustment / len(others)
    for p in others:
        st.session_state.players[p]["target"] -= adj_per_person

# --- SETUP PAGE ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Setup")
    roster_input = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    names = [n.strip() for n in roster_input.split(",") if n.strip()]
    finishing_5 = st.multiselect("Select Finishing 5", options=names, max_selections=5)
    
    if st.button("CALCULATE & START EVEN", use_container_width=True):
        st.session_state.players = {n: {
            "h1": 0.0, "h2": 0.0, "status": "On Court" if i < 5 else "Bench", 
            "target": 20.0, "consecutive": 0, "bench_time": 0,
            "is_finisher": (n in finishing_5)
        } for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- GAME PAGE ---
elif st.session_state.page == "Game":
    m, s = divmod(st.session_state.game["clock"], 60)
    st.markdown(f"<h2 style='text-align: center;'>{st.session_state.game['half']} - {m:02d}:{s:02d}</h2>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    if c1.button("START"): st.session_state.game["running"] = True
    if c2.button("PAUSE"): st.session_state.game["running"] = False
    if c3.button("STOP"): st.session_state.game["running"] = False; st.session_state.game["clock"] = 1200
    if c4.button("NEXT"):
        st.session_state.game["half"] = "2nd Half"; st.session_state.game["clock"] = 1200; st.session_state.game["running"] = False; st.rerun()

    if st.button("🔥 GO TO FINISHING 5", use_container_width=True):
        for name in st.session_state.players:
            st.session_state.players[name]["status"] = "On Court" if st.session_state.players[name]["is_finisher"] else "Bench"
            st.session_state.players[name]["consecutive"] = 0
        st.rerun()

    st.divider()
    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    
    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        # NEW: Wider columns to ensure buttons render
        col_btn, col_stats, col_adj = st.columns([5, 3, 2])
        
        gas = "⚠️" if (is_on and data["consecutive"] > 360) else ""
        bench = f"({int(data['bench_time'])}s)" if not is_on else ""
        
        if col_btn.button(f"{'✅' if is_on else '🪑'} {name} {gas} {bench}", key=f"p_{name}"):
            data["status"] = "Bench" if is_on else "On Court"
            data["consecutive"] = 0; data["bench_time"] = 0; st.rerun()
        
        goal_color = "red" if (is_on and data[half_key] >= data["target"]) else "#FFD700"
        col_stats.markdown(f"<p class='goal-text' style='color:{goal_color};'>{int(data[half_key])} / {data['target']:.1f}m</p>", unsafe_allow_html=True)

        # ADJUSTMENT: Combined +/- for stability
        sub1, sub2 = col_adj.columns(2)
        if sub1.button("-", key=f"m_{name}"): rebalance(name, -1.0); st.rerun()
        if sub2.button("+", key=f"a_{name}"): rebalance(name, 1.0); st.rerun()

    # BACKGROUND ENGINE: Live Tracking
    if st.session_state.game["running"] and st.session_state.game["clock"] > 0:
        time.sleep(1)
        st.session_state.game["clock"] -= 1
        for n, d in st.session_state.players.items():
            if d["status"] == "On Court":
                d[half_key] += 1/60; d["consecutive"] += 1; d["bench_time"] = 0
            else:
                d["bench_time"] += 1
        st.rerun()

    if st.button("⬅️ RESET"): st.session_state.page = "Setup"; st.rerun()

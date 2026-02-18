import streamlit as st
import time

# --- PRO-WIDTH STYLING ---
st.set_page_config(page_title="Flames Master v4.4", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    div.stButton > button { 
        background-color: #1a1a1a; color: #FFD700; border: 2px solid #FFD700; 
        border-radius: 8px; font-weight: bold; height: 50px !important; width: 100%;
        font-size: 1.2em !important;
    }
    .goal-text { font-size: 1.4em; color: #FFD700; font-weight: bold; text-align: center; margin-top: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- INIT STATE ---
if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

# REBALANCING LOGIC: Verified math to keep total time consistent
def rebalance(target_player, adjustment):
    others = [p for p in st.session_state.players if p != target_player]
    if not others: return
    st.session_state.players[target_player]["target"] += adjustment
    adj_per_person = adjustment / len(others)
    for p in others:
        st.session_state.players[p]["target"] -= adj_per_person

# --- PAGE 1: SETUP ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Setup")
    try: st.image("logo.png", width=150)
    except: st.write("🔥 Flames Basketball")
    
    roster_input = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    names = [n.strip() for n in roster_input.split(",") if n.strip()]
    finishing_5 = st.multiselect("Select Finishing 5", options=names, max_selections=5)
    
    if st.button("CALCULATE & START GAME"):
        st.session_state.players = {n: {
            "h1": 0.0, "h2": 0.0, "status": "On Court" if i < 5 else "Bench", 
            "target": 12.0, "consecutive": 0, "bench_time": 0,
            "is_finisher": (n in finishing_5)
        } for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- PAGE 2: GAME ---
elif st.session_state.page == "Game":
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        try: st.image("logo.png", width=100)
        except: st.write("🔥")
    with col_title:
        m, s = divmod(st.session_state.game["clock"], 60)
        st.markdown(f"<h1 style='color: #FFD700;'>{st.session_state.game['half']} - {m:02d}:{s:02d}</h1>", unsafe_allow_html=True)

    # GAME CONTROLS
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("START"): st.session_state.game["running"] = True
    if c2.button("PAUSE"): st.session_state.game["running"] = False
    if c3.button("STOP"): st.session_state.game["running"] = False; st.session_state.game["clock"] = 1200
    if c4.button("NEXT HALF"):
        st.session_state.game["half"] = "2nd Half"; st.session_state.game["clock"] = 1200; st.session_state.game["running"] = False; st.rerun()

    if st.button("🔥 ACTIVATE FINISHING 5", use_container_width=True):
        for name in st.session_state.players:
            st.session_state.players[name]["status"] = "On Court" if st.session_state.players[name]["is_finisher"] else "Bench"
            st.session_state.players[name]["consecutive"] = 0
        st.rerun()

    st.divider()
    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    
    # RESTORED: Long name boxes and SYMBOL adjustment buttons
    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        # Layout: Name(6), Goal(2), Minus(1), Plus(1) for maximum box length
        col_btn, col_stats, col_minus, col_plus = st.columns([6, 2, 1, 1])
        
        gas = "⚠️ GAS!" if (is_on and data["consecutive"] > 360) else ""
        bench_timer = f" (Rest: {int(data['bench_time'])}s)" if not is_on else ""
        
        if col_btn.button(f"{'✅' if is_on else '🪑'} {name} {gas} {bench_timer}", key=f"p_{name}"):
            data["status"] = "Bench" if is_on else "On Court"
            data["consecutive"] = 0; data["bench_time"] = 0; st.rerun()
        
        goal_color = "red" if (is_on and data[half_key] >= data["target"]) else "#FFD700"
        col_stats.markdown(f"<p class='goal-text' style='color:{goal_color};'>{int(data[half_key])}m / {data['target']:.1f}m</p>", unsafe_allow_html=True)

        # ADJUSTMENT BUTTONS: Restored

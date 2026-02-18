import streamlit as st
import time

# --- STYLING & INIT ---
st.set_page_config(page_title="Flames Smart Rotation", layout="centered")

# Custom CSS for the Black and Yellow theme
st.markdown("""
    <style>
    .stApp { background-color: black; color: white; }
    div.stButton > button { 
        background-color: #FFD700; 
        color: black; 
        border-radius: 10px; 
        font-weight: bold;
    }
    div.stButton > button:hover { background-color: #f7d117; color: black; }
    h1, h2, h3, p { color: #FFD700; }
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

# --- PAGE 1: SETUP ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Smart Setup")
    # This line triggers the error if logo.png isn't uploaded
    try:
        st.image("logo.png", width=250)
    except:
        st.warning("Upload 'logo.png' to GitHub to see the team branding.")
    
    roster_input = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    
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
    st.title(f"🔥 {st.session_state.game['half']}")
    m, s = divmod(st.session_state.game["clock"], 60)
    timer_color = "white" if st.session_state.game["running"] else "red"
    st.markdown(f"<h1 style='text-align: center; color: {timer_color};'>{m:02d}:{s:02d}</h1>", unsafe_allow_html=True)
    
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
        over_time = data[half_key] >= data["target"]
        text_color = "red" if (is_on and over_time) else "#FFD700"
        
        col_main, col_goal, col_m, col_p = st.columns([3, 2, 1, 1])
        btn_label = f"{'✅' if is_on else '🪑'} {name}: {int(data[half_key])}m (Off: {data['stints']})"
        if col_main.button(btn_label, key=f"p_{name}", use_container_width=True):
            if is_on:
                st.session_state.players[name]["status"] = "Bench"
                st.session_state.players[name]["stints"] += 1
            else:
                st.session_state.players[name]["status"] = "On Court"
            st.rerun()

        col_goal.markdown(f"<p style='color: {text_color}; font-weight: bold; margin: 0;'>Goal: {data['target']:.1f}m</p>", unsafe_allow_html=True)

        if col_m.button("➖", key=f"m_{name}"):
            balance_minutes(name, -1)
            st.rerun()
        if col_p.button("➕", key=f"a_{name}"):
            balance_minutes(name, 1)
            st.rerun()

    # --- ENGINE (FIXED INDENTATION) ---
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


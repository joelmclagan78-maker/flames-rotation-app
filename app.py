import streamlit as st
import time
import urllib.parse

# --- STYLING & CONFIG ---
st.set_page_config(page_title="Flames Master v1.2", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    div.stButton > button { 
        background-color: #1a1a1a; 
        color: #FFD700; 
        border: 1px solid #FFD700; 
        border-radius: 8px; 
        font-weight: bold; 
    }
    div.stButton > button:hover { background-color: #FFD700; color: black; }
    </style>
    """, unsafe_allow_html=True)

if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

# --- PAGE 1: SETUP ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Setup")
    try: st.image("logo.png", width=150)
    except: st.write("🔥")
    
    roster_input = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    
    if st.button("START GAME", use_container_width=True):
        names = [n.strip() for n in roster_input.split(",") if n.strip()]
        st.session_state.players = {n: {
            "h1": 0, "h2": 0, "status": "On Court" if i < 5 else "Bench", 
            "target": 100/len(names), "consecutive": 0
        } for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- PAGE 2: GAME ---
elif st.session_state.page == "Game":
    # FIXED: Added missing quote here
    st.subheader(f"Flames Rotation: {st.session_state.game['half']}")
    
    m, s = divmod(st.session_state.game["clock"], 60)
    timer_color = "#FFD700" if st.session_state.game["running"] else "red"
    st.markdown(f"<h1 style='text-align: center; color: {timer_color};'>{m:02d}:{s:02d}</h1>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if c1.button("START"): st.session_state.game["running"] = True
    if c2.button("STOP"): st.session_state.game["running"] = False
    if c3.button("NEXT HALF"):
        st.session_state.game["half"] = "2nd Half"; st.session_state.game["clock"] = 1200; st.rerun()

    st.divider()

    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    # FIXED: Corrected for-loop syntax
    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        gas_warning = " ⚠️ GAS LOW" if (is_on and data["consecutive"] > 360) else ""
        
        col1, col2 = st.columns([3, 1])
        if col1.button(f"{'✅' if is_on else '🪑'} {name}{gas_warning}", key=name, use_container_width=True):
            data["status"] = "Bench" if is_on else "On Court"
            data["consecutive"] = 0
            st.rerun()
        col2.write(f"{int(data[half_key])}m")

    st.divider()
    subject = urllib.parse.quote("Flames App Feedback")
    mail_link = f"mailto:docdvbamarymedebasketballclub.com.au?subject={subject}"
    st.markdown(f'<a href="{mail_link}" target="_blank"><button style="width:100%; height:40px; background-color:#1a1a1a; color:#FFD700; border:1px solid #FFD700; border-radius:8px; font-weight:bold;">✉️ SEND FEEDBACK</button></a>', unsafe_allow_html=True)

    # FIXED: Corrected indentation for the timer engine
    if st.session_state.game["running"] and st.session_state.game["clock"] > 0:
        time.sleep(1)
        st.session_state.game["clock"] -= 1
        for n, d in st.session_state.players.items():
            if d["status"] == "On Court":
                d[half_key] += 1/60
                d["consecutive"] += 1
        st.rerun()

    if st.button("⬅️ RESET ROSTER"): st.session_state.page = "Setup"; st.rerun()

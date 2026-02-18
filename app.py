import streamlit as st
import time
import urllib.parse

# --- STYLING ---
st.set_page_config(page_title="Flames Master", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    div.stButton > button { background-color: #1a1a1a; color: #FFD700; border: 1px solid #FFD700; border-radius: 8px; font-weight: bold; }
    .gas-alert { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- INIT STATE ---
if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

# --- PAGE 1: SETUP ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Setup")
    roster = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    if st.button("START GAME", use_container_width=True):
        names = [n.strip() for n in roster.split(",") if n.strip()]
        st.session_state.players = {n: {"h1": 0, "h2": 0, "status": "On Court" if i < 5 else "Bench", "target": 100/len(names), "consecutive": 0} for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- PAGE 2: GAME ---
elif st.session_state.page == "Game":
    st.subheader(f"Flames Rotation: {st.session_state.game['half']}")
    
    m, s = divmod(st.session_state.game["clock"], 60)
    st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{m:02d}:{s:02d}</h1>", unsafe_allow_html=True)

    # Controls
    c1, c2, c3 = st.columns(3)
    if c1.button("START"): st.session_state.game["running"] = True
    if c2.button("STOP"): st.session_state.game["running"] = False
    if c3.button("NEXT"): st.session_state.game["half"] = "2nd Half"; st.session_state.game["clock"] = 1200; st.rerun()

    st.divider()

    # Player Rows
    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        
        # Gas Tank Alert (> 6 mins)
        gas_warning = " ⚠️ GAS LOW" if (is_on and data["consecutive"] > 360) else ""
        
        col1, col2 = st.columns([3, 1])
        if col1.button(f"{'✅' if is_on else '🪑'} {name}{gas_warning}", key=name, use_container_width=True):
            data["status"] = "Bench" if is_on else "On Court"
            data["consecutive"] = 0
            st.rerun()
        col2.write(f"{int(data[half_key])}m")

    # --- PLAYBOOK & FEEDBACK ---
    st.divider()
    with st.expander("📖 OPEN PLAYBOOK"):
        st.info("Upload 'playbook.pdf' to GitHub to view your plays.")
    
    # FEEDBACK SECTION
    st.markdown("### Help improve the app")
    subject = urllib.parse.quote("Flames App Feedback")
    body = urllib.parse.quote("Hey Joel, here is some feedback on the rotation app:")
    # This creates the automatic email link
    mail_link = f"mailto:docdvbamarymedebasketballclub.com.au?subject={subject}&body={body}"
    
    st.markdown(f"""
        <a href="{mail_link}" target="_blank">
            <button style="width:100%; height:40px; background-color:#1a1a1a; color:#FFD700; border:1px solid #FFD700; border-radius:8px; font-weight:bold; cursor:pointer;">
                ✉️ SEND FEEDBACK TO JOEL
            </button>
        </a>
    """, unsafe_allow_html=True)

    # Timer engine logic
    if st.session_state.game["running"] and st.session_state.game["clock"] > 0:
        time.sleep(1)
        st.session_state.game["clock"] -= 1
        for n, d in

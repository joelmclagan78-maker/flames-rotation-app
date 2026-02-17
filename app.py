import streamlit as st
import time

# Official Flames Setup
st.set_page_config(page_title="Flames Rotation Master", layout="centered")
st.markdown("<style>body {background-color: #000000; color: #ffffff;}</style>", unsafe_allow_html=True)

# Initialize Roster and Game State
if "players" not in st.session_state:
    names = ["Xavier", "Max", "Jordan", "Bertrand", "Tyler", "Jerry", "Alex", "Vinnie"]
    st.session_state.players = {n: {"mins": 0, "status": "Bench"} for n in names}
    st.session_state.running = False
    st.session_state.clock = 1200

st.title("🔥 Flames Rotation Master")

# High-Visibility Sideline Clock
m, s = divmod(st.session_state.clock, 60)
st.metric("Match Clock", f"{m:02d}:{s:02d}")

c1, c2 = st.columns(2)
if c1.button("START", use_container_width=True): st.session_state.running = True
if c2.button("STOP", use_container_width=True): st.session_state.running = False

st.divider()

# Player Rotation Grid
for name, data in st.session_state.players.items():
    is_on = data["status"] == "On Court"
    label = f"ON COURT | {name} ({int(data['mins'])}m)" if is_on else f"BENCH | {name}"
    
    # Large sideline buttons
    if st.button(label, key=name, type="primary" if is_on else "secondary", use_container_width=True):
        st.session_state.players[name]["status"] = "Bench" if is_on else "On Court"
        st.rerun()

# Background Timer Logic
if st.session_state.running and st.session_state.clock > 0:
    time.sleep(1)
    st.session_state.clock -= 1
    for name, data in st.session_state.players.items():
        if data["status"] == "On Court":
            data["mins"] += 1/60
    st.rerun()

import streamlit as st
import time
import urllib.parse

# --- ULTRA-COMPACT MOBILE STYLING ---
st.set_page_config(page_title="Flames Master v3.8", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
    div.stButton > button { 
        background-color: #1a1a1a; color: #FFD700; border: 1px solid #FFD700; 
        border-radius: 4px; padding: 0px !important; font-size: 0.8em !important; height: 28px !important;
    }
    .goal-text { font-size: 0.75em; color: #FFD700; margin-top: 5px; line-height: 1; }
    .stDivider { margin: 0.2rem 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INIT STATE ---
if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

# VERIFIED CALCULATION LOGIC
def adjust_and_rebalance(target_player, adjustment):
    others = [p for p in st.session_state.players if p != target_player]
    if not others: return
    st.session_state.players[target_player]["target"] += adjustment
    per_player_adj = adjustment / len(others)
    for p in others:
        st.session_state.players[p]["target"] -= per_player_adj

# --- SETUP PAGE ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Setup")
    try: st.image("logo.png", width=80)
    except: st.write("🔥")
    roster_input = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    names = [n.strip() for n in roster_input.split(",") if n.strip()]
    finishing_5 = st.multiselect("Select Finishing 5", options=names, max_selections=5)
    
    if st.button("CALCULATE & START EVEN", use_container_width=True):
        even_share = 100 / len(names) if names else 0 
        st.session_state.players = {n: {
            "h1": 0, "h2": 0, "status": "On Court" if i < 5 else "Bench", 
            "target": even_share, "consecutive": 0, "bench_time": 0,
            "is_finisher": (n in finishing_5)
        } for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- GAME PAGE ---
elif st.session_state.page == "Game":
    col_l, col_t, col_s = st.columns([1, 2, 2])
    with col_l:
        try: st.image("logo.png", width=35)
        except: st.write("🔥")
    with col_t:
        m, s = divmod(st.session_state.game["clock"], 60)
        st.write(f"**{m:02d}:{s:02d}**") 
    with col_s:
        st.write(f"**{st.session_state.game['half']}**")

    c1, c2, c3, c4 = st.columns(4)
    if c1.button("START"): st.session_state.game["running"] = True
    if c2.button("PAUSE"): st.session_state.game["running"] = False
    if c3.button("STOP"): st.session_state.game["running"] = False; st.session_state.game["clock"] = 1200
    if c4.button("NEXT"):
        st.session_state.game["half"] = "2nd Half"; st.session_state.game["clock"] = 1200; st.session_state.game["running"] = False; st.rerun()

    st.divider()
    if st.button("🔥 GO TO FINISHING 5", use_container_width=True):
        for name in st.session_state.players:
            st.session_state.players[name]["status"] = "On Court" if st.session_state.players[name]["is_finisher"] else "Bench"
        st.rerun()

    st.divider()
    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    
    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        c_name, c_stats, c_m, c_p = st.columns([4, 3, 1, 1])
        
        gas = "⚠️" if (is_on and data["consecutive"] > 360) else ""
        bench_info = f" (🪑{int(data['bench_time'])}s)" if not is_on else ""
        finish_star = "⭐" if data["is_finisher"] else ""
        
        if c_name.button(f"{'✅' if is_on else '🪑'} {name}{finish_star}{gas}{bench_info}", key=f"b_{name}", use_container_width=True):
            data["status"] = "Bench" if is_on else "On Court"
            data["consecutive"] = 0; data["bench_time"] = 0; st.rerun()
        
        goal_color = "red" if (is_on and data[half_key] >= data["target"]) else "#FFD700"
        c_stats.markdown(f"<p style='color: {goal_color};' class='goal-text'>{int(data[half_key])}m/{data['target']:.1f}m</p>", unsafe_allow_html=True)

        # FIXED: Plain text labels for visibility
        if c_m.button(" - ", key=f"m_{name}"): 
            adjust_and_rebalance(name, -1)
            st.rerun()
        if c_p.button(" + ", key=f"p_{name}"): 
            adjust_and_rebalance(name, 1)
            st.rerun()

    st.divider()
    mail_link = f"mailto:docdvba@marymedebasketballclub.com.au?subject=Flames%20Feedback"
    st.markdown(f'<a href="{mail_link}" target="_blank"><button style="width:100%; height:26px; background-color:#1a1a1a; color:#FFD700; border:1px solid #FFD700; border-radius:4px; font-weight:bold; font-size:0.7em;">✉️ FEEDBACK</button></a>', unsafe_allow_html=True)

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

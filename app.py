import streamlit as st
import time
import urllib.parse

# --- STYLING: COMPACT MOBILE GRID ---
st.set_page_config(page_title="Flames Master v1.7", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    /* Compact buttons for mobile */
    div.stButton > button { 
        background-color: #1a1a1a; 
        color: #FFD700; 
        border: 1px solid #FFD700; 
        border-radius: 4px; 
        padding: 2px 5px;
        font-size: 0.8em;
    }
    .goal-text { font-size: 0.75em; color: #FFD700; line-height: 1; margin: 0; }
    .player-row { margin-bottom: -15px; }
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

# --- SETUP PAGE ---
if st.session_state.page == "Setup":
    st.title("🏀 Flames Setup")
    try: st.image("logo.png", width=120)
    except: st.write("🔥")
    roster_input = st.text_area("Roster", value="Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie")
    if st.button("CALCULATE & START EVEN", use_container_width=True):
        names = [n.strip() for n in roster_input.split(",") if n.strip()]
        even_share = 100 / len(names) if names else 0 
        st.session_state.players = {n: {"h1": 0, "h2": 0, "status": "On Court" if i < 5 else "Bench", "target": even_share, "consecutive": 0} for i, n in enumerate(names)}
        st.session_state.page = "Game"
        st.rerun()

# --- GAME PAGE: NEW COMPACT LAYOUT ---
elif st.session_state.page == "Game":
    col_logo, col_text = st.columns([1, 4])
    with col_logo:
        try: st.image("logo.png", width=50)
        except: st.write("🔥")
    with col_text:
        st.write(f"**Flames: {st.session_state.game['half']}**")
    
    m, s = divmod(st.session_state.game["clock"], 60)
    timer_color = "#FFD700" if st.session_state.game["running"] else "red"
    st.markdown(f"<h3 style='text-align: center; color: {timer_color}; margin-top: -20px;'>{m:02d}:{s:02d}</h3>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if c1.button("START"): st.session_state.game["running"] = True
    if c2.button("STOP"): st.session_state.game["running"] = False
    if c3.button("NEXT"):
        st.session_state.game["half"] = "2nd Half"; st.session_state.game["clock"] = 1200; st.rerun()

    st.divider()
    half_key = "h1" if st.session_state.game["half"] == "1st Half" else "h2"
    
    # NEW COMPACT PLAYER GRID
    for name, data in st.session_state.players.items():
        is_on = data["status"] == "On Court"
        # Tight 4-column layout for mobile: Status/Name | Stats | - | +
        c_name, c_stats, c_minus, c_plus = st.columns([4, 3, 1, 1])
        
        gas_warning = "⚠️" if (is_on and data["consecutive"] > 360) else ""
        btn_label = f"{'✅' if is_on else '🪑'} {name} {gas_warning}"
        
        if c_name.button(btn_label, key=f"btn_{name}", use_container_width=True):
            data["status"] = "Bench" if is_on else "On Court"
            data["consecutive"] = 0
            st.rerun()
        
        over_target = data[half_key] >= data["target"]
        goal_color = "red" if (is_on and over_target) else "#FFD700"
        c_stats.markdown(f"<p style='color: {goal_color}; padding-top: 5px;' class='goal-text'>{int(data[half_key])}m / {data['target']:.0f}m</p>", unsafe_allow_html=True)

        if c_minus.button("➖", key=f"m_{name}"): balance_minutes(name, -1); st.rerun()
        if c_plus.button("➕", key=f"a_{name}"): balance_minutes(name, 1); st.rerun()

    st.divider()
    subject = urllib.parse.quote("Flames Feedback")
    # Corrected email with @ symbol
    mail_link = f"mailto:docdvba@marymedebasketballclub.com.au?subject={subject}"
    st.markdown(f'<a href="{mail_link}" target="_blank"><button style="width:100%; height:35px; background-color:#1a1a1a; color:#FFD700; border:1px solid #FFD700; border-radius:4px; font-weight:bold;">✉️ FEEDBACK</button></a>', unsafe_allow_html=True)

    if st.session_state.game["running"] and st.session_state.game["clock"] > 0:
        time.sleep(1)
        st.session_state.game["clock"] -= 1
        for n, d in st.session_state.players.items():
            if d["status"] == "On Court":
                d[half_key] += 1/60
                d["consecutive"] += 1
        st.rerun()

    if st.button("⬅️ RESET"): st.session_state.page = "Setup"; st.rerun()



import streamlit as st
import time
import urllib.parse

# --- STYLING ---
st.set_page_config(page_title="Flames Master Stable", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #f0f0f0; }
    div.stButton > button { 
        background-color: #1a1a1a; color: #FFD700; border: 1px solid #FFD700; 
        border-radius: 8px; font-weight: bold; 
    }
    .goal-text { font-size: 0.9em; font-weight: bold; color: #FFD700; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INIT STATE ---
if "page" not in st.session_state: st.session_state.page = "Setup"
if "players" not in st.session_state: st.session_state.players = {}
if "game" not in st.session_state: st.session_state.game = {"running": False, "clock": 1200, "half": "1st Half"}

# SMART BALANCING LOGIC
def balance_minutes(target_player, adjustment):
    others = [p for p in st.session_state.players if p != target_player]
    if not others:
        return
    per_player_adj = adjustment / len(others)
    st.session_state.players[target_player]["target"] += adjustment
    for p in others:
        st.session_state.players[p]["target"] -= per_player_adj

# --- PAGE 1: SETUP ---
if st.session_state.page == "Setup":
    st.title("🏀

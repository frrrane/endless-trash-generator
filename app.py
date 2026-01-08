import streamlit as st
import subprocess
import os
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="TRASH_GEN_v1.0", page_icon="📟", layout="wide")

# 2. Glitch/Retro CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #050505;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Retro CRT Effect */
    .stApp::before {
        content: " ";
        display: block;
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 2;
        background-size: 100% 2px, 3px 100%;
        pointer-events: none;
    }

    /* Neon Green Text & Headers */
    h1, h2, h3, p, label, .stMarkdown {
        color: #00FF41 !important;
        text-shadow: 0 0 5px #00FF41;
    }

    /* The 'Glitch' Button */
    .stButton>button {
        background-color: #000000;
        color: #00FF41;
        border: 2px solid #00FF41;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .stButton>button:hover {
        background-color: #00FF41;
        color: #000000;
        box-shadow: 0 0 20px #00FF41;
    }

    /* Terminal-style text areas */
    .stTextArea textarea {
        background-color: #000000 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
    }
    </style>
    """, unsafe_allow_index=True)

# 3. Dashboard UI
st.title("📟 ENDLESS_TRASH_SYSTEM // ROOT")
st.write(f"SYSTEM_TIME: {datetime.now().strftime
import streamlit as st
import sys
import subprocess
import os
import requests
from datetime import datetime

# --- CONFIGURATION (Paste your details here) ---
API_KEY = "YOUR_YOUTUBE_API_KEY"
CHANNEL_ID = "YOUR_CHANNEL_ID"

st.set_page_config(page_title="TRASH_GEN_v1.0", page_icon="📟", layout="wide")

# --- GLITCH CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; font-family: 'Courier New', monospace; }
    .stApp::before {
        content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 2; background-size: 100% 2px, 3px 100%; pointer-events: none;
    }
    h1, h2, h3, p, label, .stMarkdown { color: #00FF41 !important; text-shadow: 0 0 5px #00FF41; }
    div.stButton > button {
        background-color: #000000; color: #00FF41; border: 2px solid #00FF41;
        font-weight: bold; width: 100%;
    }
    div.stButton > button:hover { background-color: #00FF41; color: #000000; box-shadow: 0 0 20px #00FF41; }
    .stTextArea textarea { background-color: #000000 !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- YOUTUBE STATS FUNCTION ---
def get_yt_stats():
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
    try:
        response = requests.get(url).json()
        stats = response['items'][0]['statistics']
        return stats
    except:
        return None

# --- UI LAYOUT ---
st.title("📟 ENDLESS_TRASH_SYSTEM // ROOT")
st.write(f"SYSTEM_TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# New Metrics Section
st.header("📊 CHANNEL_METRICS")
yt_data = get_yt_stats()
if yt_data:
    m1, m2, m3 = st.columns(3)
    m1.metric("SUBSCRIBERS", yt_data.get('subscriberCount', '0'))
    m2.metric("TOTAL_VIEWS", yt_data.get('viewCount', '0'))
    m3.metric("UPLOADS", yt_data.get('videoCount', '0'))
else:
    st.error("FAILED_TO_FETCH_YT_STATS")

st.write("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("CMD_EXECUTIONS")
    if st.button("RUN_PIPELINE.EXE"):
        st.write(">> INITIALIZING...")
        result = subprocess.run([sys.executable, "pipeline.py"], capture_output=True, text=True)
        st.code(result.stdout)

with col2:
    st.header("LOG_STREAM")
    if os.path.exists("cron_log.txt"):
        with open("cron_log.txt", "r") as f:
            st.text_area("SYSTEM_OUTPUT", f.read(), height=300)

st.write("---")
st.header("LATEST_OUTPUT_PREVIEW")
video_files = [f for f in os.listdir('.') if f.endswith('.mp4')]
if video_files:
    latest = max(video_files, key=os.path.getctime)
    st.video(latest)
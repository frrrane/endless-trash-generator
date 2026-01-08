# 🤖 Endless Trash Generator

An automated AI-video pipeline that dreams up surreal concepts and publishes them to YouTube. This project uses **Google Veo 3.1** for video generation and **Gemini 2.0 Flash** for creative prompt engineering.

## 🚀 How it Works
1. **Brainstorming:** The script uses Gemini 2.0 to generate a unique, surreal, or funny video prompt.
2. **Generation:** The prompt is sent to the Veo 3.1 model to create an 8-second cinematic video.
3. **Publishing:** The resulting MP4 is automatically uploaded to a YouTube channel as a Private video.
4. **Automation:** A Linux Cron job triggers the entire pipeline daily.

## 🛠️ Tech Stack
- **Language:** Python 3.11+
- **AI Models:** Google GenAI (Veo 3.1 & Gemini 2.0 Flash)
- **APIs:** YouTube Data API v3
- **Automation:** Linux Crontab

## 📦 Setup Instructions

### 1. Prerequisites
- A Google Cloud Project with the YouTube Data API enabled.
- A Gemini API Key from [Google AI Studio](https://aistudio.google.com/).
- Python virtual environment (`venv`).

### 2. Configuration
Create a `.env` file in the root directory:
```text
GEMINI_API_KEY="your_api_key_here"

import os
import time
import pickle
from dotenv import load_dotenv

from google import genai
from google.genai import types
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload

# ── NEW IMPORTS for TTS + audio merge ────────────────────────────────────────
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip

# ── PROMPT TEMPLATES IMPORT ──────────────────────────────────────────────────
from prompt_templates import generate_wild_prompt, get_current_buzzwords

# ── CONFIGURATION & SECRETS ──────────────────────────────────────────────────
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLIENT_SECRETS_FILE = "client_secrets.json"
TOKEN_FILE = "token.json"
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# (your existing get_authenticated_service() function remains unchanged)

def generate_random_prompt(use_gemini_boost=True):
    print("🧠 Generating wild trash prompt...")
    get_current_buzzwords()  # refresh trends

    client = None
    if use_gemini_boost and GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = generate_wild_prompt(use_gemini_boost=use_gemini_boost, gemini_client=client)

    print("\n" + "═" * 80)
    print("WILD TRASH PROMPT:", prompt)
    print("═" * 80 + "\n")
    return prompt


def generate_tts_voiceover(text, output_file="voiceover.mp3", lang="en", slow=False):
    """Generate simple spoken narration from the prompt using gTTS"""
    print(f"🗣️ Generating TTS voiceover for: '{text[:60]}...'")
    try:
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(output_file)
        print(f"✓ Voiceover saved: {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ TTS failed: {e}")
        return None


def add_audio_to_video(video_path, audio_path, output_path=None):
    """Merge TTS audio onto the silent Veo video using MoviePy"""
    if not output_path:
        base, ext = os.path.splitext(video_path)
        output_path = f"{base}_with_voice{ext}"

    print(f"🎥 Merging audio → {output_path}")

    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # Optional: trim/make audio fit video duration
        if audio.duration > video.duration:
            audio = audio.subclip(0, video.duration)
        elif audio.duration < video.duration:
            # Loop audio or pad with silence if desired
            pass

        final_video = video.set_audio(audio)
        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            logger=None  # quieter output
        )
        print(f"✓ Final video with voiceover: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Audio merge failed: {e}")
        return None


def generate_video_with_veo(prompt):
    """Veo generation — STILL DISABLED for testing"""
    print("⏳ Veo generation DISABLED (uncomment when ready)")
    # For testing: pretend we have a silent video
    # return "example_silent_trash.mp4"  # ← replace with real path for manual tests
    return None


def upload_to_youtube(file_path, title):
    # (your existing function – unchanged)
    pass  # ... keep your original code ...


# ── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n=== ENDLESS TRASH GENERATOR — VOICEOVER CHAOS MODE ===")
    print(f"     {time.strftime('%Y-%m-%d %H:%M:%S')} — Ljubljana\n")

    # 1. Generate crazy prompt
    prompt = generate_random_prompt(use_gemini_boost=True)

    # 2. Generate TTS narration (using the prompt itself as spoken text)
    voiceover_file = generate_tts_voiceover(
        text=prompt,                # or make smarter script from prompt
        output_file="trash_narration.mp3",
        lang="en",
        slow=False                  # True = slower/dramatic delivery
    )

    # 3. Veo video (disabled)
    print("→ Skipping Veo generation\n")
    video_file = None  # generate_video_with_veo(prompt)

    # For testing: comment out above and set manually
    # video_file = "your_silent_veo_video.mp4"

    # 4. Merge TTS onto video if both exist
    final_video = None
    if video_file and voiceover_file:
        final_video = add_audio_to_video(video_file, voiceover_file)

    # 5. Upload final result (or just the voiced version)
    if final_video:
        short_title = f"Endless Trash: {prompt[:55]}{'...' if len(prompt)>55 else ''}"
        upload_to_youtube(final_video, short_title)
    else:
        print("Test complete ✓ (no final video – check TTS file!)")
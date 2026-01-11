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

# ── TTS + Audio merge ────────────────────────────────────────────────────────
from gtts import gTTS
from moviepy import VideoFileClip, AudioFileClip

# ── PROMPT GENERATOR ─────────────────────────────────────────────────────────
import prompt_templates   # ← Import the whole module (safer)

# ── CONFIGURATION & SECRETS ──────────────────────────────────────────────────
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLIENT_SECRETS_FILE = "client_secrets.json"
TOKEN_FILE = "token.json"
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def get_authenticated_service():
    """Get authenticated YouTube service"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)


def generate_random_prompt(use_gemini_boost=True):
    """Generate chaotic trash prompt with current X trends + optional Gemini chaos"""
    print("🧠 Generating wild trash prompt...")

    # Refresh trending topics — use qualified module name
    try:
        prompt_templates.get_current_buzzwords()  # updates BUZZWORDS global
    except AttributeError:
        print("⚠️  Warning: get_current_buzzwords not found in prompt_templates.py")

    client = None
    if use_gemini_boost:
        if not GEMINI_API_KEY:
            print("⚠️ No GEMINI_API_KEY found — skipping Gemini boost")
        else:
            client = genai.Client(api_key=GEMINI_API_KEY)

    try:
        prompt = prompt_templates.generate_wild_prompt(
            use_gemini_boost=use_gemini_boost,
            gemini_client=client
        )
    except AttributeError:
        print("❌ Error: generate_wild_prompt not found in prompt_templates.py")
        return "Fallback prompt: A cursed toaster screams into the void, glitchcore style"

    print("\n" + "═" * 80)
    print("WILD TRASH PROMPT:")
    print(prompt)
    print("═" * 80 + "\n")

    return prompt


def generate_tts_voiceover(text, output_file="voiceover.mp3", lang="en", slow=False):
    """Generate spoken narration using gTTS"""
    print(f"🗣️ Generating TTS voiceover...")
    try:
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(output_file)
        print(f"✓ Voiceover saved: {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ TTS failed: {e}")
        return None


def add_audio_to_video(video_path, audio_path, output_path=None):
    """Merge TTS audio onto video"""
    if not output_path:
        base, ext = os.path.splitext(video_path)
        output_path = f"{base}_voiced{ext}"

    print(f"🎥 Merging audio → {output_path}")

    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        if audio.duration > video.duration:
            audio = audio.subclip(0, video.duration)

        final = video.set_audio(audio)
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            logger=None
        )
        print(f"✓ Final video ready: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Merge failed: {e}")
        return None


def generate_video_with_veo(prompt):
    """Veo generation – DISABLED for testing"""
    print("⏳ Veo generation DISABLED (uncomment when ready)")
    return None

    # Uncomment the block below when you want real videos
    # if not GEMINI_API_KEY: ...
    # client = genai.Client(api_key=GEMINI_API_KEY)
    # try: operation = client.models.generate_videos(...)


def upload_to_youtube(file_path, title):
    """Upload to YouTube as Private"""
    youtube = get_authenticated_service()
    print(f"🚀 Uploading: {title}")

    body = {
        'snippet': {
            'title': title,
            'description': 'Generated by Endless Trash Generator\n#AI #TrashArt',
            'categoryId': '22'
        },
        'status': {'privacyStatus': 'private'}
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    response = request.execute()
    print(f"✓ Uploaded! Video ID: {response['id']}")


# ── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n=== ENDLESS TRASH GENERATOR — CHAOS MODE ===")
    print(f"     {time.strftime('%Y-%m-%d %H:%M:%S')} — Ljubljana\n")

    # Generate prompt
    prompt = generate_random_prompt(use_gemini_boost=True)

    # TTS narration
    voiceover_file = generate_tts_voiceover(
        text=prompt,
        output_file="trash_narration.mp3"
    )

    # Video (disabled)
    print("→ Skipping video generation\n")
    video_file = None  # generate_video_with_veo(prompt)

    # Merge if possible
    final_video = None
    if video_file and voiceover_file:
        final_video = add_audio_to_video(video_file, voiceover_file)

    # Upload if we have something
    if final_video:
        title = f"Endless Trash: {prompt[:60]}{'...' if len(prompt)>60 else ''}"
        upload_to_youtube(final_video, title)
    else:
        print("Test complete ✓ (check console + trash_narration.mp3)")
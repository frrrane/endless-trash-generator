# Endless Trash Generator 🗑️✨

An absurd AI-powered daily trash video factory.  
Generates completely deranged, surreal video prompts using mad-libs chaos, current-ish trending topics, Gemini enhancement, and spoken narration via TTS.

Currently outputs:
- Wild one-sentence prompts (printed + saved as TTS audio)
- Ready for Veo video generation (disabled by default to save quota)

## Current Output Style (example)

> A terminally online pineapple pulsating with neon veins and clad in skin-tight, bio-engineered skinny jeans speedruns main character syndrome in a parallel dimension LinkedIn Premium Lounge oozing glitching, hyper-saturated Marcus Rashford memes, fueled by a Quietly Unhinged energy drink brewed from tears of discarded TikTok e-girls after the fish-eye lens apocalypse, all while desperately begging a sentient AI to end its suffering as chromatic aberration tears reality itself apart.

## Features

- Mad-libs style prompt templates with cursed word pools
- Gemini 2.0 Flash chaos boost for maximum brainrot
- Spoken narration via gTTS (English, adjustable speed)
- Static fallback trending topics (live scraping blocked/deprecated in 2026)
- YouTube upload pipeline (private, disabled until video gen enabled)
- Easy to run daily via cron

## Requirements

- Python 3.10+
- Google Gemini API key (with Veo access for video – preview model)

```bash
pip install -U \
  google-genai \
  python-dotenv \
  google-auth-oauthlib \
  google-api-python-client \
  beautifulsoup4 \
  requests \
  gtts \
  moviepy

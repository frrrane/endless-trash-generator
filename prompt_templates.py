# prompt_templates.py
"""
Chaotic mad-libs style prompt generator for Endless Trash Generator
Uses static fallback trends (live endpoints are unreliable/blocked in 2026)
"""

import random
from google.genai import types  # Required for correct config syntax


# ── STATIC FALLBACK TRENDS (updated Jan 2026) ────────────────────────────────

def get_current_buzzwords(num=12):
    """
    Returns a list of interesting current-ish trending-style terms.
    Live fetching is disabled due to widespread blocking / endpoint death.
    """
    print("Using static fallback trends (live fetching disabled)")
    return [
        "ElClasico", "RealMadrid", "FCBarcelona", "ViniciusJr", "Raphinha",
        "KylianMbappe", "LamineYamal", "MarcusRashford", "NFLPlayoffs",
        "BillsMafia", "JoshAllen", "PhiladelphiaEagles", "SanFrancisco49ers",
        "SuperBowl60", "AIethics", "TikTokBan2026", "ViralMeme", "CryptoCrash",
        "QuantumAI", "GeminiAPI", "VeoVideo", "TrashArt", "RoombaRebellion"
    ][:num]


# Global variable – refreshed each time the function is called
BUZZWORDS = get_current_buzzwords()


# ── CHAOS WORD POOLS ─────────────────────────────────────────────────────────

ADJECTIVES = [
    "feral", "glistening", "sentient & spiteful", "terminally online",
    "eldritch", "sweaty", "cursed", "neon-hemorrhaging", "post-ironic",
    "quietly unhinged", "quantumly embarrassed", "dripping expired energy drinks",
    "vibe-checking God", "dopamine poisoned", "having an existential TikTok breakdown"
]

NOUNS = [
    "toaster with abandonment issues", "self-aware Roomba war criminal",
    "pineapple wearing skinny jeans", "corporate ladder made of human teeth",
    "NFT of your childhood trauma", "haunted 2009 flip phone", "sentient Costco hotdog",
    "depressed algorithm", "your search history personified",
    "evil AirPod that only plays Crazy Frog"
]

ACTIONS = [
    "unionize against their creator", "live-tweet the heat death of the universe",
    "ghost their own notification", "start an OnlyFans for existential dread",
    "attempt to cancel God", "doomscroll their own source code",
    "speedrun main character syndrome"
]

LOCATIONS = [
    "inside the group chat from hell", "abandoned 2012 Tumblr dashboard",
    "parallel dimension LinkedIn premium lounge", "bottom of an infinite doomscroll",
    "the void between two Discord pings"
]

STYLES = [
    "glitchcore nightmare fuel", "VHS recording of a possession",
    "corporate training video directed by David Lynch",
    "found footage from a dimension that got canceled",
    "hyper-saturated TikTok e-girl apocalypse"
]

CAMERA = [
    "extreme Dutch angle + seizure strobe", "dolly zoom into the void",
    "grainy security cam footage", "fish-eye + chromatic aberration max"
]

CURSED_FEATURES = [
    "face made of scrolling TikTok comments", "constantly buffering soul",
    "eyes replaced with loading spinners", "emitting Comic Sans speech bubbles",
    "made of recycled 2016 memes"
]

DOOMED_TOPICS = [
    "the Great Microwave Uprising", "sentient printers finally snapping",
    "{buzz} takes over the metaverse", "capitalism gets ratio'd into oblivion"
]

TEMPLATES = [
    "{adj} {noun} {action} in {location}, hyped on {buzz}, {style}, {camera}",
    "Breaking trash: {noun} with {cursed_feature} declares {doomed_topic}",
    "POV: You are {adj} {noun} realizing {buzz} was a mistake forever, {style}",
    "AI news anchor with {cursed_feature} melts down live about {buzz} {doomed_topic}",
]

FINAL_FATES = [
    "becoming the final TikTok sound", "getting ratio'd out of existence",
    "buffering eternally", "ascending as the god of cringe"
]


# ── MAIN GENERATOR ───────────────────────────────────────────────────────────

def generate_wild_prompt(use_gemini_boost=False, gemini_client=None):
    """
    Generate one maximally chaotic video prompt.
    """
    template = random.choice(TEMPLATES)

    # Pick 1–2 buzzwords + occasional mutation
    buzz_list = random.sample(BUZZWORDS, k=random.randint(1, min(2, len(BUZZWORDS))))
    buzz = " × ".join(buzz_list)

    if random.random() < 0.25:
        buzz = random.choice(ADJECTIVES).title() + " " + buzz

    doomed_topic = random.choice(DOOMED_TOPICS).format(buzz=random.choice(buzz_list))

    base_prompt = template.format(
        adj=random.choice(ADJECTIVES),
        noun=random.choice(NOUNS),
        action=random.choice(ACTIONS),
        location=random.choice(LOCATIONS),
        style=random.choice(STYLES),
        camera=random.choice(CAMERA),
        cursed_feature=random.choice(CURSED_FEATURES),
        doomed_topic=doomed_topic,
        buzz=buzz,
    )

    # Gemini chaos boost – correct 2026 syntax
    if use_gemini_boost and gemini_client:
        try:
            chaos_request = (
                f"Make this prompt 70–120% more unhinged. Add brainrot energy, cursed vibes, "
                f"slight body-horror undertones, and at least one meta-AI-awareness reference. "
                f"Keep it one sentence. Original: '{base_prompt}'"
            )

            response = gemini_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=chaos_request,
                config=types.GenerateContentConfig(  # ← correct parameter name
                    temperature=1.45,
                    top_p=0.92
                )
            )

            enhanced = response.text.strip()
            if len(enhanced) > 30:
                base_prompt = enhanced

        except Exception as e:
            print(f"Gemini boost skipped: {e}")

    # ~35% chance of dramatic ending
    if random.random() < 0.35:
        endings = [
            "SHE'S RIGHT BEHIND YOU",
            "RATIO + L + YOU FELL OFF",
            f"{buzz.upper()} IS COMING FOR US ALL",
            "ERROR 418: I'M A TEAPOT AND I'M SUFFERING"
        ]
        base_prompt += "   ★ " + random.choice(endings)

    return base_prompt
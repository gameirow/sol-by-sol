"""Make Sojourner's intro voice: one MP3 per caption, saved to assets/voice/<shot>.mp3.

Uses Microsoft's free neural voices (the same natural voices as the Edge browser's "Read aloud").
Only the lines below are sent to the voice service.

    pip install edge-tts
    python tools/make_voice.py                  # default voice
    python tools/make_voice.py en-GB-SoniaNeural   # try another voice
    python tools/make_voice.py en-US-EmmaMultilingualNeural launch   # remake only one clip
    python build.py

To use your own recordings instead, save them as assets/voice/0.mp3, 1.mp3, 2.mp3, 4.mp3, 5.mp3, 6.mp3
plus launch.mp3 (the countdown). The numbers are the captions in order; the flyover has no words.
If you change a caption in SHOTS (src/index.src.html), change the line here too.
"""
import asyncio, pathlib, sys
import edge_tts

VOICE = sys.argv[1] if len(sys.argv) > 1 else "en-US-AnaNeural"   # a real child voice: young and cute (chosen by João, 15 Nov 2026)
RATE, PITCH = "+8%", "+6Hz"                                         # a little quicker and higher = brighter, more excited

# Same words as the speech bubbles, written the way they should be SAID (respelled where the voice gets it wrong:
# "So-jurner" makes it say SO-jur-ner).
LINES = {
    "launch": "Three... two... one... Lift-off!",
    0: "Hi there! I'm So-jurner! We're flying to Mars! It's so far away that a radio call home takes up to twenty-two minutes. So on Mars... you decide.",
    1: "Whoa, watch out! Sometimes the Sun throws out a radiation storm. You can't see it, and you can't feel it. Thick walls and a storm shelter keep you safe.",
    2: "Here we are: Gale crater, on Mars! NASA's rover Curiosity has measured the weather and radiation here since 2012. And this game uses its real numbers!",
    4: "Your power comes from sunlight. But dust lands on the solar panels every day. Dusty panels make less power, so someone has to go out and clean them.",
    5: "Inside the base, there's a treadmill to keep your muscles strong in Mars's weak gravity, a bunk for rest, and a farm for food. They all need looking after.",
    6: "A day on Mars is called a sol. Your mission: ten sols, and three crystals. Every choice counts, commander!",
}

async def main():
    out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "voice"
    out.mkdir(parents=True, exist_ok=True)
    only = sys.argv[2:]                           # e.g. python tools/make_voice.py <voice> launch   -> only that clip
    for shot, text in LINES.items():
        if only and str(shot) not in only: continue
        f = out / f"{shot}.mp3"
        await edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH).save(str(f))
        print(f"{f.name}  {f.stat().st_size // 1024} KB  {text[:50]}...")
    print(f"Done with {VOICE}. Now run: python build.py")

asyncio.run(main())

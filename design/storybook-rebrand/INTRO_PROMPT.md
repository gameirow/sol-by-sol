# Prompt for Claude Code: storybook restyle of the INTRO FILM only

Before you start (in a terminal, in the `sol-by-sol` repo):
```
git fetch
git checkout thea-graphics-rebranding
git pull
git checkout -b intro-storybook
```
Then start `claude` and paste everything below the line.

---

We're on the branch `intro-storybook`. Check with `git branch --show-current` and stop if it's a different branch. I'm working on **only the intro film** of Sol by Sol. Thea is restyling the rest of the game in the same storybook style on her branch `thea-graphics-rebranding`, at the same time. Our job: give the intro film the storybook look of our demo, **without changing what it says or how long it lasts**.

## Read first
1. `CLAUDE.md`: project context. The "Intro film" part of the Game design section describes how the intro works. Every rule there still applies, **except the "Look" bullet** (the mission-control look and Barlow fonts are being replaced).
2. `design/storybook-rebrand/STYLE_GUIDE.md`: the new look.
3. `design/storybook-rebrand/reference-3d-scene.html`: **our demo.** Open it in a browser first. Reuse its code directly in the intro:
   - the sky gradient shader, stars and the small blue-white Mars sun;
   - the lighting rig (hemisphere + warm rim + a few warm point lights) and the purple-rose fog;
   - flat-shaded matte materials, the patched-plate dome, glowing portholes and lanterns (emissive + additive glow sprite);
   - the string lights, drifting embers and mist.

   The demo uses Three r160 and the game uses r170, so check that every API you copy works in r170.
4. In `src/index.src.html`, only the intro code: `SHOTS`, `startIntro()`, `endIntro()`, `__shot(i,t)`, `introAudio`, `speak()`, the start card, and whatever objects and materials only the intro uses.

## What to do
1. **Inventory first:** list every intro shot (Earth → flight → solar storm → Mars → flyover of the base → dusty panels → inside → mission) and say how each will look in the storybook style, in a short table. **Show me and wait for my OK.**
2. Restyle shot by shot, one commit per shot or two, using `__shot(i,t)` to jump straight to the shot you're working on:
   - Mars and the base: the demo's dusk sky, fog, warm glows and patched habitat.
   - Space shots (Earth, flight, solar storm): the same palette, deep violet space, warm and cool glows, gentle particles. The solar storm must stay clearly visible and a bit dramatic, but not scary for kids aged 7–12.
   - Caption bubble and Sojourner's portrait during the intro: parchment, wood and brass, with the fonts IM Fell English SC (headings) and Spectral (text).
3. After each step:
   - Run `python build.py`.
   - Extract the `<script type="module">` block and run `node --check` on it.
   - Serve `dist/` (see `.claude/launch.json`) and play the whole intro at desktop size and phone size (about 390×844).
   - Check that skipping still works: Next, Enter, Space and Right skip one part, and Skip intro / Esc skips everything.

## Don't change
- **Captions, the spoken lines, the shot order, voice clips or timings.** A shot must never end while Sojourner is still talking. Captions stay in sync with `tools/make_voice.py`, so don't touch that file or `assets/voice/`.
- **The audio** (`introAudio`, `bed`, `speak()`): only restyle visuals.
- **Anything outside the intro:** the HUD, station, outside walk, title, end screens, game logic or data. Those belong to Thea's branch. If you need a shared helper or shared CSS changed, add a new one for the intro instead of editing the shared one, so the two branches merge cleanly. Tell me whenever that happens.
- Never use the browser's `speechSynthesis`.

## Hard rules
- Original art only: don't copy characters or designs from existing games or films.
- It must run smoothly on a school laptop or tablet. Prefer emissive materials and glow sprites over many real lights. Any bloom must switch off on weak devices.
- Small commits on `intro-storybook`. **Don't push, merge or touch `main` or `thea-graphics-rebranding`** without asking me. João reviews before anything is merged.

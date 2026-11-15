# Prompt for Claude Code: storybook graphics rebrand (Thea, everything except the intro)

Copy everything below the line into Claude Code, started in the root of the `sol-by-sol` repo.

---

We're on the branch `thea-graphics-rebranding`. Check with `git branch --show-current` and stop if it's a different branch. I'm Thea (game design). I want to **rebrand the look of Sol by Sol** from the current "mission control" style to the **storybook style of our demo scene**. The gameplay, rules, numbers, NASA data and text stay exactly the same. Only the graphics change.

## Read first
1. `CLAUDE.md`: the whole project context. Every rule there still applies, **except the "Look" bullet**. This branch replaces the mission-control look and the Barlow fonts.
2. `design/storybook-rebrand/STYLE_GUIDE.md`: the new look (palette, fonts, UI pieces, 3D lighting, do's and don'ts).
3. `design/storybook-rebrand/reference-3d-scene.html`: **our demo. Apply it to the game.** Open it in a browser first. Reuse its code directly wherever it fits:
   - the sky gradient shader, stars and the small blue-white Mars sun;
   - the lighting rig (hemisphere + warm rim directional + a few warm point lights) and the fog colour and distances;
   - flat-shaded matte materials, the patched-plate dome (InstancedMesh of tilted panels), glowing portholes, doorways and lanterns (emissive material + additive glow sprite);
   - the string lights and small flags, the drifting embers and ground mist, gentle bobbing and flicker animations;
   - the HUD: glass vials (Power, Air, Health), the brass sol dial, the wooden title sign on chains, parchment decision cards, gold and wood buttons.

   The demo uses Three r160 and the game uses r170, so check that every API you copy still works in r170. The demo's numbers and text (for example "Sol 4 of 15") are placeholders: keep the game's real values and wording.
4. `src/index.src.html`: the whole game.

## Not yours: the intro film
My boyfriend is restyling the **intro film** at the same time, on his own branch. **Don't touch any intro code or files:**
- `SHOTS`, `startIntro()`, `endIntro()`, `__shot`, `introAudio`, `speak()`
- the start card ("Watch the film" / "Skip to the game")
- `tools/make_voice.py`, `assets/voice/`

If a shared helper or shared CSS would need to change for your work, add a new one next to it instead of editing the old one, so our branches merge cleanly. Tell me whenever you had to touch anything near the intro.

## What to do
1. **Inventory before changing anything.** List every visual element (intro excluded) and say which part of the demo it will take its look from, in a short table:
   - CSS variables, colours and fonts
   - HUD chips, health screen, overlays and cards, buttons
   - the `ICONS` line-icon set
   - Sojourner's portrait and speech bubble (in the game, not in the intro)
   - title, "Real or game?" and end screens
   - station interior (bunk, greenhouse, AIR & HEAT, treadmill, comms, radiation monitor, power screen, airlock)
   - outside terrain, sky, fog and the 3 weather looks, crystals, solar panels, the Curiosity model

   **Show me the table and wait for my OK.**
2. Then apply the demo in small steps, one commit per step, building and checking after each:
   1. Design tokens: one block of CSS custom properties with the demo's palette and fonts (IM Fell English SC + Spectral). Swap the fonts.
   2. HUD and UI: vials, brass dial, parchment cards, wooden signs and buttons, copied from the demo's CSS. Keep it readable.
   3. Icons: keep the drawn line icons (`ic('name')`), restyled as brass or ink strokes. **Still no emojis.**
   4. Outside 3D: the demo's sky, fog, lighting, glows, embers and mist on the Gale terrain. Keep **clear / hazy / dust storm** clearly different (dust storm = thick ochre fog, dimmed lights, more particles), because they carry game information.
   5. Inside the station: warm lamplight, patched metal, wood and brass, with each station object easy to spot and tap.
   6. Sojourner's 2D portrait in the game: a friendly little patched-up rover in the new palette.
3. After every step:
   - Run `python build.py`.
   - Extract the `<script type="module">` block and run `node --check` on it.
   - Serve `dist/` (see `.claude/launch.json`) and look at it at desktop size and phone size (about 390×844).
   - Run `tests/flow_test.py` if you can, and fix selectors the rework broke. Keep the debug hooks working (`__S()`, `__open`, `__cr()`, `__dbg`, `__new()`, `__end()`).
4. At the end, update the "Look" bullet in `CLAUDE.md` to describe the new style and point to the style guide and demo, and list anything you couldn't finish.

## Hard rules
- **Don't change game logic, balance numbers, data files or any player-facing text.** If a visual change would need a text change, ask me first.
- **Kid-friendly, not scary:** ages 7–12. Cosy and a bit mysterious, never horror. Bright glows on anything important.
- **Readable:** body text contrast at least 4.5:1, buttons at least 44 px, and it must work on phone, tablet and computer.
- **Original art only.** Don't copy any existing game's characters, logos or designs.
- **Performance:** it must run smoothly on a school laptop or tablet. Prefer emissive materials and glow sprites over many real lights. Any post-processing (bloom) must switch off on weak devices.
- Small commits on this branch. **Don't push, merge or touch `main`** until I say so. João reviews before anything is merged.

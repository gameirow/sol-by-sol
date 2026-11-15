# Sol by Sol — project context for Claude

NASA Space Apps Challenge Bern (14–15 Nov 2026), challenge "Junior Astronaut Mission Trainer".
A browser game for kids 7–12: run a Mars outpost for 10 sols (Mars days), balancing health,
radiation, solar power and food, driven by real NASA data. No login, no download.
Team: João (code owner) and Thea (game design). Claude writes all the code.

## How to work with us
- Plain language, short answers. We are not NASA scientists.
- Kids' text must be short and sweet. No units (no µGy/mSv), no names kids don't know (e.g. InSight).
- Must work on computer, tablet and phone.
- Look: whimsical storybook / dark-fairytale style (rebrand on branch `thea-graphics-rebranding`, 15 Nov 2026): a cosy, slightly mysterious
  Mars outpost at dusk, patched together and glowing warmly in purple fog. Kid-friendly, never horror. Full guide: `design/storybook-rebrand/STYLE_GUIDE.md`.
  - All colours and fonts are CSS custom properties in the one `:root` block at the top of `src/index.src.html`. Change them there only.
  - Fonts: IM Fell English SC (headings, signs, canvas labels; one weight, so no bold) + Spectral (body; numbers lining + tabular). Canvas code uses `FD` / `FB`.
  - HUD = wooden shelf with a brass sol dial and glass vials; cards and Sojourner's bubble are parchment; buttons are gold or wood, at least 44 px.
  - Status colours are CSS variables: bright on wood, deep inside `.card` (it overrides `--ok`/`--warnc`/`--bad`). Use `fCol`/`radCol` in HTML, `radHex` on canvases.
  - NO emojis anywhere. Icons are the drawn line-icon set `ICONS` / `ic('name')`: brass on wood, ink on parchment.
  - 3D: always dusk. The three weather looks (clear / hazy / dust storm, `LOOK`) carry game info and must stay clearly different.
    The airlock beacon stays green and the crystal yellow (Sojourner's lines say "green light" and "yellow light").
    Glows are emissive + additive sprites (`glowSprite`), not extra lights, so they look right with bloom off (touch devices run "low" quality).

## Files
- `src/index.src.html` — the whole game (HTML + CSS + JS module, Three.js r170 from jsdelivr CDN).
  Placeholders `__POOL__`, `__WEATHER__`, `__TERRAIN__` are filled by `build.py`.
- `data/pool.json` — 27 real solar storms (DONKI) + Curiosity radiation on Mars for each (RadLab).
- `data/weather.json` — 27 real 10-sol windows from Curiosity's weather station (REMS): [date,min,max,pressure,uv]. Indices 0–1 = 2018 global dust storm.
- `data/gale.b64` — 96×96 8-bit MOLA height map of Gale crater / Mount Sharp.
- `assets/curiosity.js` — NASA Curiosity 3D model (glb, base64 ES module, meshopt).
- `assets/photos.js` — 8 real Curiosity photos (base64) with kid captions, credit NASA/JPL-Caltech.
- `assets/voice/*.mp3` — Sojourner's intro voice: `launch.mp3` (countdown) and 0,1,2,4,5,6 (one per caption; the file name is the shot's `vo`). Made by `tools/make_voice.py` (free Microsoft neural voice via `pip install edge-tts`, voice en-US-EmmaMultilingualNeural) or recorded by the team. build.py copies them to dist.
- `assets/planets.js` — real NASA maps for the intro (base64 JPEGs): Earth = Blue Marble (NASA Goddard SVS), Mars = colour mosaic from NASA-3D-Resources. Loaded with `import()`; a drawn fallback shows until then.
- `tests/flow_test.py` — Playwright test of one sol (go outside → crystal → clean panels → sleep). Needs a local server; debug hooks: `__S()`, `__open(name)`, `__cr()`, `__dbg`, `__new()` (new mission), `__end()` (end the sol), `__frame(keepCam)` (draw one frame now, e.g. in a hidden tab). Not re-run since the Nov 14 rework (it hard-codes a Linux Chrome path); the same one-sol flow was clicked through by hand in the browser after the storybook rebrand (15 Nov 2026).
- `.claude/launch.json` — preview server config (serves `dist/` on port 8765).

## Build & run
```
python build.py
cd dist && python -m http.server 8765     # then open http://localhost:8765
```
Must be served over http (not file://) because photos/model load with `import()`.
Syntax check: extract the `<script type="module">` block and run `node --check`.

## Hosting
- Live now as a Claude artifact: https://claude.ai/artifact/Fpt2ydxutX7q2Hxokyi7cc
  (only the claude.ai web chat can republish it). Share → "Anyone with the link" to let others play.
- For our own hosting (GoDaddy from NASA, GitHub Pages, Netlify): upload the `dist/` folder as-is.

## Game design (Thea's decisions + the 14 Nov 2026 rework for the challenge guidelines)
- Goal: survive 10 sols + collect 3 crystals outside. 2 activities per sol: go outside, run, call home, rest. Sleep in the bunk to end the sol.
- Health /10 = average of 5 factors: radiation, exercise, air & heat, sleep & food, mood. Game over if health < 3 OR any one factor reaches 0.
  Tap the heart chip in the HUD for the health screen (one real fact + source per factor).
- Trade-offs (the point of the challenge, "no free choice"):
  - Power is solar only (no battery). Clean panels on a mild night cover everything; dust, dust storms and cold nights make it short (do NOT say "never enough", João flagged that as untrue): air & heat, farm lights, treadmill (1), family call (1).
  - Dust lands on the panels EVERY sol (-6%, -20% in a dust storm, max -60%). Cleaning means going outside = radiation + an activity slot.
  - Food: crew eats 3 a sol, each power unit on the farm grows 1. Cutting the farm today costs food tomorrow.
  - Radiation: dose = how strong x how long. Inside you still get half of the everyday background; outside all of it plus any storm,
    in proportion to the time spent walking (60 s = a whole day). Staying in during a storm costs crystals, mood and clean panels.
  - Forecasts: each flare alert shows NASA's real forecast (may hit / will miss) and the report later shows what really happened.
  - Storm watch (added 14 Nov, late): from the alert until the storm arrives (or one sol later if it misses) the HUD shows "storm watch".
    On its first sol a storm arrives at a hidden moment; if you are outside the alarm sounds mid-walk (8–22 s in) and you run home.
    Storm dose counts only the seconds outside after it arrives, at double rate (30 s = the whole storm). `stormNow()`, `stormWatch()`.
  - Radio delay matters: Earth's storm warning arrives after the storm itself, with the real light-time for that date (`lateWarning()`).
- Radio delay: real Earth-Mars distance and light time for the mission's real date (`orbits()`), shown in COMMS and when calling home.
- Spacesuit has its own battery, so going outside costs 0 power (dusty panels must never lock you inside).
- Outside: player walks on the Gale terrain, touches a glowing yellow sulfur crystal (Curiosity found real ones in 2024) -> real NASA photo.
  Geiger clicks + suit meter show radiation and time outside. Green light marks the airlock; the Go inside button walks you home.
- The look follows the real weather: clear, hazy, or dust storm (fog + murky sky).
- Intro film (about 70 s, real-time Three.js, no video file): launch from Kennedy Space Center at sunrise (Florida, rocket flies east over the Atlantic) -> flight (boosters, escape tower, core and upper stage separate; solar wings open) -> solar storm -> Mars with Gale crater marked -> flyover of the base -> dusty panels -> inside -> mission.
  Each shot's caption is one true fact needed for a later choice. `SHOTS` (each has `world`: ksc / space / mars, `vo`, `bed`, `note`), `buildKSC()`, `buildIntro()`, `buildRocket()` + `rocketPose()`, `startIntro()`, `endIntro()`.
  Debug: `__shot(i,t)` jumps to a shot (0 = launch, 1 = flight, 2 = storm, 3 = Mars, 4 = flyover, 5 = panels, 6 = inside, 7 = mission); `__itick(sec)` runs the film forward (the preview pane is too slow for real time); `__intro()` returns the film objects.
  Look (15 Nov, João: "crispy, not foggy"): while the film plays, `introRender()` renders at full resolution (up to 2x), bloom only on very bright things, light vignette; space and launch use Neutral tone mapping, the Mars shots keep the game's look but with the clear-weather sky (`introClearSky()`). Quick cuts, a dip to black only between Earth / space / Mars. No MSAA: with the bloom pass it made black blocks.
  No NASA logo anywhere (NASA does not allow its insignia without permission); the VAB shows the US flag only. Gale crater ring sits at 5.4 S, 137.8 E (`latLonDir`).
  First visit shows a start card ("Watch the film" / "Skip to the game"); that tap is also what lets the browser play sound.
  Voice = recorded MP3 clips (`speak(s.vo)` plays assets/voice/<vo>.mp3, at `voAt` seconds if set); the portrait's mouth follows the real loudness (AnalyserNode). No clip = bubble only.
  NEVER use the browser's speechSynthesis: João rejected it as robotic (14 Nov 2026). The spoken lines live in tools/make_voice.py; keep them in sync with SHOTS captions.
  Music pad + engine/storm/wind noise are made with WebAudio (`introAudio`, `bed`), no audio files. A shot never ends while Sojourner is still talking.
  Controls: Next (or Enter/Space/Right) skips one part, Skip intro (Esc) skips all, Sound on/off. Seen flag in localStorage `solbysol_intro`; "Watch intro" on the title replays.
  Sound was never heard by Claude (no audio in the preview): only checked that clips play, the mouth follows them and a missing clip doesn't stall the film.
- Narrator: Sojourner the rover (speech bubble + 2D portrait).
- Station: bunk, greenhouse/farm, AIR & HEAT generator, treadmill with harness + bungees (low gravity), comms computer, radiation monitor, power screen, airlock. Solar panels + Curiosity model outside.
- Health wording: "inspired by NASA's space-health research". OSDR facts (checked against the OSDR records on 14 Nov 2026):
  OSD-999/1000 simulated cosmic rays changed human brain organoids; OSD-505 space radiation changed rats' prefrontal cortex;
  OSD-342 mice lost muscle + bone in 33 days on the ISS; OSD-418 rat leg muscle in simulated Mars gravity (study design, no result claimed);
  OSD-903/943 immune changes in the blood of two astronauts (Ax-1); OSD-278 a bacterium grown on the ISS was more harmful to fruit flies.
- "Real or game?" screen (title, COMMS, end screen) lists what is real NASA data and what is a game rule. Keep it in sync with any rule change.
- Title screen has one LIVE element: latest solar flare from DONKI (hidden if the fetch fails, e.g. inside the Claude artifact).

## Key numbers
- Radiation index: `round(10*ln(max(uGy,80)/80)/ln(1700/80))`, clamped 0–10 (normal day ≈ 1, May 2024 storm = 10).
- QF 3.05, budget ≈ 7.17 mSv for the 10-sol game (NASA-STD-3001 600 mSv career limit, scaled). Normal Mars day ≈ 115–210 µGy absorbed (Curiosity).
- Game rules: `INSIDE_SHARE` 0.5, `EVA_FULL` 60 s, `DUST_SOL` 0.06, `DUST_STORM` 0.2, `DUST_MAX` 0.6.
- SOLAR power by sunlight level {V:11, H:10, M:9, L:7}; farm break-even 3; air needs 3 (+1 below −75 °C, +1 below −85 °C).
- Per sol: exercise +1.5 / −1.5; rest +1.5 / −0.8; mood −1.5, call +2.5, outside +1.5.
- Balance check (400 simulated missions each, after the storm-watch change): sensible kid survives ~100%, 3 stars ~82%; never going outside survives ~78%, max 1 star;
  ignoring the storm alarm survives ~34%; random play ~75%.

## Data sources (where the data came from)
- DONKI: https://ccmc.gsfc.nasa.gov/DONKI-API/get/{FLR,SEP,CMEAnalysis,WSAEnlilSimulations} (60-day max per request).
- RadLab: https://visualization.osdr.nasa.gov/radlab/api/?spacecraft=Curiosity&... (absorbed dose = CSV column 2).
- REMS: https://mars.nasa.gov/rss/api/?feed=weather&category=msl&feedtype=json
- MOLA DEM: asc-pds-services.s3.us-west-2.amazonaws.com/mosaic/Mars_MGS_MOLA_DEM_mosaic_global_463m.tif
- NASA Images API, NASA-3D-Resources (GitHub).

## Open to-dos
0. Re-upload `sol-by-sol-site.zip` (or the `dist` folder) to Netlify after every rebuild; connect solbysol.earth (Porkbun DNS) to the Netlify site.
1. Human playtest of a full 10 sols by a real kid, and a real phone test of walking outside (only checked in a phone-sized browser window so far).
2. Republish the Claude artifact from the claude.ai web chat (the live link still shows the old version).
3. Submission page + demo video.
4. Merging `intro-storybook` into main: both branches touch the shared caption bubble / portrait CSS, so expect a small merge there.

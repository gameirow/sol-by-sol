# Sol by Sol: storybook style guide (rebrand draft)

**Mood:** a cosy, slightly mysterious fairy-tale outpost on Mars at dusk. It looks hand-made and patched together, glowing warmly in purple fog. Picture a bedtime-story world where everything important has a light on it. It should feel like an adventure, never like horror.

## Palette

| Role | Colour | Use |
|---|---|---|
| Night sky | `#1A1830` | top of sky, darkest backgrounds |
| Dusk violet | `#34304F` | mid sky, panels behind text |
| Dusty rose | `#7A5269` | low sky, fog colour (`#6E4F6A`) |
| Horizon clay | `#B9786A` | horizon band, distant haze |
| Ground | `#5E3E3E` → `#2A1C22` | Mars soil, near to dark |
| Wood | `#3B2A26` (edge `#6B4E3E`) | signs, title board, dark buttons |
| Ink | `#1A1012` | outlines, borders |
| Parchment | `#E9D9BC` (inner edge `#D6C19C`) | cards and dialogs (text on it: `#2B1E1A`) |
| Cream text | `#F3DDB3` (muted `#D9B98C`) | text on dark backgrounds |
| Brass | `#C79A5A` | dial rims, bands, icon strokes, frames |
| Warm glow | `#FFB25B` / `#FFD58A` | lamps, windows, doorway, embers |
| Cool glow | `#9FE8E0` | science, samples, water/ice, the rover's eye |
| Pink glow | `#FF9CC0` | antenna tips, health |
| Accent crimson | `#8A2E3A` | card headings, alerts on parchment |

**Resource colours:** Power `#FFC75F` · Air `#8FE3DA` · Health `#FF9CC0`.
Never rely on hue alone: always add a label or icon, and keep lightness different.

## Type
- **Headings and signs:** *IM Fell English SC* (Google Fonts), old storybook print.
- **Body and UI text:** *Spectral* 500/600 (Google Fonts). If small text is hard to read on phones, use a cleaner sans for body text and keep the storybook font for headings only.
- Numbers in readouts must stay crisp and readable.

## UI pieces
- **Resource meters:** glass vials with rounded tops, a cream rim, a glowing liquid fill and a white shine stripe. The label goes below in the heading font.
- **Sol counter:** a round brass dial ("Sol / 4 / of 10").
- **Title and big labels:** a wooden board hanging from two thin chains, tilted about 2°.
- **Cards and dialogs:** parchment with a thick ink border, inner edge line, slight tilt (1–2°) and a soft warm outer glow.
- **Buttons:** primary is gold `#FFC75F` with ink text; secondary is wood `#3B2A26` with cream text. 2 px ink border, small radius (4 px), at least 44 px tall, visible focus ring.
- **Icons:** the existing hand-drawn line icons, restyled with brass or ink strokes. No emojis.

## 3D look
- **Sky:** a vertical gradient from night → violet → rose → clay at the horizon, with stars at the top and a small blue-white Mars sun near the horizon (Mars sunsets really are bluish).
- **Fog:** linear, dusty-rose `#6E4F6A`. It hides the distance and makes glowing things pop.
- **Lights:** a soft hemisphere light (violet sky, dark-red ground), one warm rim light from behind, and a few warm point lights at doorways, windows and lanterns. Use emissive materials plus additive sprite glows for bulbs and windows instead of many real lights.
- **Materials:** flat-shaded, rough, matte. Habitat built from patched metal plates in mauve-greys `#5C4D58`–`#958078`, wood scaffolds, brass bands.
- **Atmosphere:** slowly rising embers or dust specks (additive points), low drifting mist sprites, gentle animations (bobbing, flickering bulbs).
- **Weather states (they carry game information):**
  - clear = the warm glows dominate
  - hazy = more fog, softer light
  - dust storm = thick ochre-brown fog, dimmed lights, more particles
- **Shapes:** a little crooked, leaning, hand-made. Round porthole windows, stacked and slightly tilted towers, string lights and small flags. The rounded shapes keep it friendly.

## Do / don't
- **Do:** big readable glows on anything you can tap; one clear focal light per scene; cosy warmth inside the station.
- **Don't:** horror, skulls, creepy faces, pitch-black scenes, emoji, neon overload, or copying characters or designs from existing games.

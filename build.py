"""Build Sol by Sol: fills the data placeholders in src/index.src.html and writes dist/.
Usage:  python build.py        then serve dist/ (see CLAUDE.md)."""
import pathlib, shutil

ROOT = pathlib.Path(__file__).parent
src = (ROOT / "src" / "index.src.html").read_text(encoding="utf-8")
data = ROOT / "data"
out = (src.replace("__POOL__", (data / "pool.json").read_text(encoding="utf-8"))
          .replace("__WEATHER__", (data / "weather.json").read_text(encoding="utf-8"))
          .replace("__TERRAIN__", (data / "gale.b64").read_text(encoding="utf-8").strip()))
dist = ROOT / "dist"
(dist / "assets").mkdir(parents=True, exist_ok=True)
(dist / "index.html").write_text(out, encoding="utf-8")
for f in (ROOT / "assets").glob("*.js"):
    shutil.copy(f, dist / "assets" / f.name)
voice = ROOT / "assets" / "voice"          # Sojourner's voice clips (see tools/make_voice.py)
if voice.is_dir():
    (dist / "assets" / "voice").mkdir(exist_ok=True)
    for f in voice.glob("*.mp3"):
        shutil.copy(f, dist / "assets" / "voice" / f.name)
print("Built dist/index.html")

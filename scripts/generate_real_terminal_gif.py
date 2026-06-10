from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/alex/Projects/AIChatProcessManager")
LOG_PATH = ROOT / "outputs" / "media" / "real-message-flow-clean.log"
OUT_DIR = ROOT / "outputs" / "media"
OUT_DIR.mkdir(parents=True, exist_ok=True)

GIF_PATH = OUT_DIR / "real-message-flow-terminal-real.gif"
POSTER_PATH = OUT_DIR / "real-message-flow-terminal-real-poster.png"

W, H = 1400, 900
PAD_X = 34
PAD_Y = 82
LINE_H = 28
VISIBLE_LINES = 24

BG = "#0f1722"
BAR = "#e9e9eb"
TEXT = "#ecf2f8"
MUTED = "#8aa0b6"
GREEN = "#6ee7b7"
BLUE = "#7dd3fc"
YELLOW = "#fde68a"


def load_font(size: int):
    for path in [
        "/System/Library/Fonts/Supplemental/Menlo.ttc",
        "/System/Library/Fonts/Supplemental/Andale Mono.ttf",
        "/System/Library/Fonts/Monaco.ttf",
    ]:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


FONT = load_font(18)
FONT_SMALL = load_font(15)
FONT_TITLE = load_font(20)


def wrap_line(raw: str) -> list[str]:
    if raw.startswith("aichat_backend  | "):
        raw = raw.replace("aichat_backend  | ", "", 1)
    width = 108 if "[message_flow]" in raw else 100
    return textwrap.wrap(raw, width=width, break_long_words=False, break_on_hyphens=False) or [raw]


raw_lines = [line.rstrip() for line in LOG_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
wrapped_lines: list[tuple[str, str]] = []

for raw in raw_lines:
    color = GREEN if "[message_flow]" in raw else BLUE
    for part in wrap_line(raw):
        wrapped_lines.append((part, color))


def make_frame(visible: int, cursor_on: bool):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((14, 14, W - 14, H - 14), radius=18, fill=BG, outline="#1e293b", width=2)
    draw.rounded_rectangle((28, 24, W - 28, 58), radius=16, fill=BAR)
    draw.ellipse((46, 35, 58, 47), fill="#ff5f57")
    draw.ellipse((68, 35, 80, 47), fill="#febc2e")
    draw.ellipse((90, 35, 102, 47), fill="#28c840")

    draw.text((PAD_X, PAD_Y - 38), "AIChatProcessManager :: real backend message flow", font=FONT_TITLE, fill=TEXT)
    draw.text((PAD_X, PAD_Y - 12), "source: actual POST /api/conversations/1/messages logs", font=FONT_SMALL, fill=MUTED)

    visible_slice = wrapped_lines[max(0, visible - VISIBLE_LINES):visible]
    y = PAD_Y + 22
    for line, color in visible_slice:
        if '"table": "messages"' in line or '"table": "message_contents"' in line:
            color = YELLOW
        elif '"table": "tool_calls"' in line or '"table": "tool_results"' in line or '"table": "message_metadata"' in line:
            color = GREEN
        draw.text((PAD_X, y), line, font=FONT, fill=color)
        y += LINE_H

    if cursor_on:
        draw.text((PAD_X, y), "▋", font=FONT, fill=TEXT)
    return img


frames = []
durations = []

for i in range(1, len(wrapped_lines) + 1):
    frames.append(make_frame(i, True))
    durations.append(160 if i < 3 else 240)
    frames.append(make_frame(i, False))
    durations.append(80)

frames.append(make_frame(len(wrapped_lines), False))
durations.append(1400)

frames[0].save(
    GIF_PATH,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    disposal=2,
)
frames[-1].save(POSTER_PATH)

print(GIF_PATH)
print(POSTER_PATH)

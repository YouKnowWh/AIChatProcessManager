from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/Users/alex/Projects/AIChatProcessManager")
OUT = ROOT / "outputs" / "media"
OUT.mkdir(parents=True, exist_ok=True)

GIF_PATH = OUT / "message-ingest-terminal-only-v2.gif"
PNG_PATH = OUT / "message-ingest-terminal-only-v2-poster.png"

W, H = 980, 560
TERM_BG = "#10161f"
TERM_BORDER = "#1b2430"
TEXT = "#e6edf3"
MUTED = "#93a4b8"
GREEN = "#36d399"
BLUE = "#60a5fa"
WHITE = "#ffffff"


def load_font(size: int):
    for path in [
        "/System/Library/Fonts/Supplemental/Andale Mono.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


FONT_TITLE = load_font(22)
FONT_BODY = load_font(15)
FONT_SMALL = load_font(13)

STEPS = [
    ("request accepted", "POST /api/conversations/12/messages"),
    ("context loaded", "FROM conversations + messages + message_contents\nUSE parent_message_id + sequence_number to rebuild history"),
    ("user message row", "WRITE messages\nid=301 sender_type=user role=user seq=17"),
    ("user content block", "WRITE message_contents\nmessage_id=301 type=text sort_order=0"),
    ("ai message row", "WRITE messages\nid=302 sender_type=ai role=assistant seq=18 parent=301"),
    ("ai content block", "WRITE message_contents\nmessage_id=302 type=text sort_order=0"),
    ("reasoning block", "WRITE message_reasoning\nmessage_id=302 visibility=owner_visible"),
    ("tool call block", "WRITE tool_calls\nmessage_id=302 tool_name=search status=success"),
    ("tool result block", "WRITE tool_results\ntool_call_id=81 is_error=false"),
    ("metadata block", "WRITE message_metadata\nmessage_id=302 model=deepseek-chat total_tokens=947"),
    ("audit log row", "WRITE system_logs\naction=send_message target_id=301"),
    ("transaction commit", "COMMIT"),
]


def rr(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def txt(draw, x, y, text, font, fill, spacing=5):
    draw.multiline_text((x, y), text, font=font, fill=fill, spacing=spacing)


def make_frame(step_idx: int):
    img = Image.new("RGB", (W, H), TERM_BG)
    draw = ImageDraw.Draw(img)

    rr(draw, (0, 0, W - 1, H - 1), 26, TERM_BG, TERM_BORDER, 2)
    for i, color in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        draw.ellipse((26 + i * 22, 22, 40 + i * 22, 36), fill=color)
    txt(draw, 100, 19, "send_message()", FONT_SMALL, MUTED)

    txt(draw, 28, 62, "AIChatProcessManager block-to-table write flow", FONT_TITLE, WHITE)
    txt(draw, 28, 96, "content -> message_contents | reasoning -> message_reasoning | tool -> tool_calls/tool_results", FONT_SMALL, BLUE)

    rows = []
    for i in range(step_idx + 1):
        title, body = STEPS[i]
        rows.append((f"[{i + 1:02d}] {title}", GREEN if i == step_idx else TEXT, FONT_BODY))
        rows.append((f"     {body}", MUTED, FONT_BODY))
        rows.append(("", MUTED, FONT_BODY))

    y = 150
    for line, color, font in rows:
        if line:
            txt(draw, 32, y, line, font, color)
        y += 31

    if step_idx < len(STEPS) - 1:
        txt(draw, 32, y + 4, "▋", FONT_BODY, TEXT)

    return img


frames = [make_frame(i) for i in range(len(STEPS))]
durations = [450] + [520] * (len(frames) - 2) + [1200]
frames[0].save(
    GIF_PATH,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    disposal=2,
)
frames[-1].save(PNG_PATH)
print(GIF_PATH)
print(PNG_PATH)

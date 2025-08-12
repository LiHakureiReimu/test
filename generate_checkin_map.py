from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os

W, H = 2000, 1200
OUTPUT = "/workspace/daka_map.png"
# Try multiple font candidates for Chinese glyphs
FONT_CANDIDATES = [
    "/workspace/NotoSansCJKsc-Regular.otf",
    "/workspace/NotoSansSC-Regular.otf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansSC-Regular.otf",
    "/usr/share/fonts/truetype/noto/NotoSansSC-Regular.otf",
]

# Colors
TOP_COLOR = "#0a0f2c"      # dark navy
BOTTOM_COLOR = "#0a2a6e"   # deep blue
GRID_COLOR = (0, 255, 255, 28)  # cyan, low alpha
CIRCUIT_COLOR = (0, 200, 255, 160)
CIRCUIT_GLOW = (0, 200, 255, 40)
NODE_FILL = (0, 255, 255, 220)
NODE_GLOW = (0, 255, 255, 40)
LABEL_COLOR = (220, 240, 255, 245)
TITLE_COLOR = (255, 255, 255, 245)
STAMP_BG = (12, 22, 52, 190)
STAMP_BORDER = (0, 230, 255, 160)

# Load font with fallbacks
def load_font(size: int):
    # Try CJK-capable fonts first
    for path in FONT_CANDIDATES:
        try:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        except Exception:
            continue
    # Try generic DejaVuSans if present (may miss CJK glyphs)
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()

font_title = load_font(92)
font_label = load_font(38)
font_num = load_font(40)
font_stamp = load_font(32)
font_stamp_header = load_font(42)

# Create gradient background
try:
    grad = Image.linear_gradient("L").resize((W, H))
    bg = ImageOps.colorize(grad, black=TOP_COLOR, white=BOTTOM_COLOR).convert("RGBA")
except Exception:
    bg = Image.new("RGBA", (W, H), TOP_COLOR)
    draw_tmp = ImageDraw.Draw(bg)
    for y in range(H):
        ratio = y / max(1, H - 1)
        r1, g1, b1 = (10, 15, 44)
        r2, g2, b2 = (10, 42, 110)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw_tmp.line([(0, y), (W, y)], fill=(r, g, b, 255))

img = bg.copy()

# Grid overlay
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)
spacing = 80
for x in range(0, W, spacing):
    gd.line([(x, 0), (x, H)], fill=GRID_COLOR, width=1)
for y in range(0, H, spacing):
    gd.line([(0, y), (W, y)], fill=GRID_COLOR, width=1)
img = Image.alpha_composite(img, grid.filter(ImageFilter.GaussianBlur(0.4)))

# Subtle vignette
vignette = Image.new("L", (W, H), 0)
vg = ImageDraw.Draw(vignette)
vg.rectangle([0, 0, W, H], fill=100)
vg.rectangle([80, 80, W - 80, H - 80], fill=0)
vignette = vignette.filter(ImageFilter.GaussianBlur(60))
darken = Image.new("RGBA", (W, H), (0, 0, 0, 140))
darken.putalpha(vignette)
img = Image.alpha_composite(img, darken)

# Title with glow
canvas = img.copy()
draw = ImageDraw.Draw(canvas)

def draw_glow_text(base_img, text, xy, font, fill, glow_color=(0, 255, 255), glow_radius=6):
    x, y = xy
    # Glow layer
    glow = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    dg = ImageDraw.Draw(glow)
    dg.text((x, y), text, font=font, fill=(glow_color[0], glow_color[1], glow_color[2], 130))
    glow = glow.filter(ImageFilter.GaussianBlur(glow_radius))
    out = Image.alpha_composite(base_img, glow)
    # Solid text
    d = ImageDraw.Draw(out)
    d.text((x, y), text, font=font, fill=fill)
    return out

TITLE = "周年庆打卡地图"
# Center title
bbox = draw.textbbox((0, 0), TITLE, font=font_title)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
canvas = draw_glow_text(canvas, TITLE, ((W - text_w)//2, 40), font_title, TITLE_COLOR)

# Circuit lines (simple stepped polylines)
paths = [
    [(140, 260), (520, 260), (520, 420), (860, 420), (860, 540), (1160, 540)],
    [(220, 760), (480, 760), (480, 620), (760, 620), (760, 360), (1040, 360), (1040, 280)],
    [(300, 520), (680, 520), (680, 700), (980, 700), (980, 860), (1240, 860)],
]

# Glow underlay
circuit_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cdg = ImageDraw.Draw(circuit_glow)
for pts in paths:
    cdg.line(pts, fill=CIRCUIT_GLOW, width=14, joint="curve")
circuit_glow = circuit_glow.filter(ImageFilter.GaussianBlur(6))
canvas = Image.alpha_composite(canvas, circuit_glow)

# Crisp lines
cd = ImageDraw.Draw(canvas)
for pts in paths:
    cd.line(pts, fill=CIRCUIT_COLOR, width=4, joint="curve")

# Nodes (checkpoints) on left two-thirds
nodes = [
    (300, 260, "1", "粘币游戏"),
    (600, 380, "2", "淘趣循环市集"),
    (900, 300, "3", "框住时光·与你同行"),
    (1150, 500, "4", "快问快答"),
    (800, 800, "5", "量子纠缠瓶"),
]

# Draw node with glow and label
for (nx, ny, num, label) in nodes:
    # Glow
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow_layer)
    r_outer = 26
    gdraw.ellipse([nx - r_outer, ny - r_outer, nx + r_outer, ny + r_outer], fill=NODE_GLOW)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(8))
    canvas = Image.alpha_composite(canvas, glow_layer)

    # Solid node
    dnode = ImageDraw.Draw(canvas)
    r = 16
    dnode.ellipse([nx - r, ny - r, nx + r, ny + r], fill=NODE_FILL, outline=(255, 255, 255, 200), width=2)

    # Number
    num_bbox = dnode.textbbox((0, 0), num, font=font_num)
    num_w = num_bbox[2] - num_bbox[0]
    num_h = num_bbox[3] - num_bbox[1]
    dnode.text((nx - num_w//2, ny - num_h//2), num, font=font_num, fill=(10, 20, 35, 255))

    # Label with small leader line
    label_x = nx + 28
    label_y = ny - 8
    dnode.line([(nx + r, ny), (label_x - 12, label_y + 18)], fill=(180, 230, 255, 180), width=2)
    dnode.text((label_x, label_y), label, font=font_label, fill=LABEL_COLOR)

# Stamp area panel on right
panel_margin = 40
panel_w = 620
panel_x0 = W - panel_margin - panel_w
panel_y0 = 140
panel_x1 = W - panel_margin
panel_y1 = H - panel_margin

panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(panel)
# Rounded rectangle background
try:
    pd.rounded_rectangle([panel_x0, panel_y0, panel_x1, panel_y1], radius=20, fill=STAMP_BG, outline=STAMP_BORDER, width=2)
except Exception:
    pd.rectangle([panel_x0, panel_y0, panel_x1, panel_y1], fill=STAMP_BG, outline=STAMP_BORDER, width=2)

# Header
header_text = "盖章区"
hbbox = pd.textbbox((0, 0), header_text, font=font_stamp_header)
hw = hbbox[2] - hbbox[0]
px_center = panel_x0 + (panel_w // 2)
panel_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pgd = ImageDraw.Draw(panel_glow)
pgd.text((px_center - hw//2, panel_y0 + 24), header_text, font=font_stamp_header, fill=(0, 255, 255, 150))
panel_glow = panel_glow.filter(ImageFilter.GaussianBlur(4))
panel = Image.alpha_composite(panel, panel_glow)
pd = ImageDraw.Draw(panel)
pd.text((px_center - hw//2, panel_y0 + 24), header_text, font=font_stamp_header, fill=TITLE_COLOR)

# Five stamp boxes
stamp_items = [label for (_, _, _, label) in nodes]
stamp_top = panel_y0 + 100
stamp_gap = 26
box_h = 120
box_w = panel_w - 60
for i, label in enumerate(stamp_items):
    y0 = stamp_top + i * (box_h + stamp_gap)
    y1 = y0 + box_h
    x0 = panel_x0 + 30
    x1 = x0 + box_w
    try:
        pd.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=(0, 0, 0, 0), outline=STAMP_BORDER, width=2)
    except Exception:
        pd.rectangle([x0, y0, x1, y1], fill=(0, 0, 0, 0), outline=STAMP_BORDER, width=2)

    # Label left
    lb = pd.textbbox((0, 0), label, font=font_stamp)
    pd.text((x0 + 18, y0 + (box_h - (lb[3]-lb[1]))//2), label, font=font_stamp, fill=LABEL_COLOR)

    # Placeholder text right-aligned
    ph = "盖章处"
    phb = pd.textbbox((0, 0), ph, font=font_stamp)
    pd.text((x1 - 18 - (phb[2]-phb[0]), y0 + (box_h - (phb[3]-phb[1]))//2), ph, font=font_stamp, fill=(160, 220, 255, 180))

canvas = Image.alpha_composite(canvas, panel)

# Save
canvas.save(OUTPUT)
print(f"Saved: {OUTPUT}")
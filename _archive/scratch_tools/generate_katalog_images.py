import math
from PIL import Image, ImageDraw, ImageFont

W, H = 600, 600

def create_radial_gradient(base_color, outer_color):
    img = Image.new("RGBA", (W, H), outer_color)
    draw = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    max_r = int(math.hypot(cx, cy))
    # Draw radial gradient layers
    for r in range(max_r, 0, -6):
        t = r / max_r
        # Interpolate
        cr = int(base_color[0] * (1 - t) + outer_color[0] * t)
        cg = int(base_color[1] * (1 - t) + outer_color[1] * t)
        cb = int(base_color[2] * (1 - t) + outer_color[2] * t)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(cr, cg, cb, 255))
    return img

def add_pill_label(draw, text, bg_color, text_color=(255, 255, 255)):
    try:
        font = ImageFont.truetype("arialbd.ttf", 20)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    px, py = 22, 10
    w = tw + px * 2
    h = th + py * 2
    x0 = (W - w) // 2
    y0 = H - 90
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=h//2, fill=bg_color)
    draw.text((x0 + px, y0 + py - 2), text, font=font, fill=text_color)

# 1. NETFLIX
def gen_netflix():
    img = create_radial_gradient((80, 5, 15), (15, 15, 18))
    draw = ImageDraw.Draw(img)
    # Ambient glow
    draw.ellipse([150, 120, 450, 420], fill=(229, 9, 20, 45))
    # Red ribbon N
    # Left stem
    draw.rounded_rectangle([210, 160, 260, 420], radius=4, fill=(184, 7, 15, 255))
    # Right stem
    draw.rounded_rectangle([340, 160, 390, 420], radius=4, fill=(184, 7, 15, 255))
    # Diagonal ribbon
    draw.polygon([(210, 160), (260, 160), (390, 420), (340, 420)], fill=(229, 9, 20, 255))
    add_pill_label(draw, "NETFLIX 4K UHD", (229, 9, 20))
    img.save("assets/katalog/netflix.png")

# 2. CANVA
def gen_canva():
    # Linear gradient cyan to purple
    img = Image.new("RGBA", (W, H))
    draw = ImageDraw.Draw(img)
    c1 = (0, 196, 204)
    c2 = (125, 42, 232)
    for y in range(H):
        t = y / H
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
    # White Canva C-ring
    cx, cy = 300, 270
    draw.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], fill=(255, 255, 255, 40))
    draw.ellipse([cx - 95, cy - 95, cx + 95, cy + 95], outline=(255, 255, 255, 255), width=28)
    # Cut out top-right to form 'C'
    draw.rectangle([cx + 20, cy - 70, cx + 130, cy + 30], fill=c2)
    # Draw C terminal dots
    draw.ellipse([cx + 30, cy - 75, cx + 70, cy - 35], fill=(255, 255, 255, 255))
    draw.ellipse([cx + 40, cy + 20, cx + 80, cy + 60], fill=(255, 255, 255, 255))
    add_pill_label(draw, "CANVA PRO", (255, 255, 255), text_color=(125, 42, 232))
    img.save("assets/katalog/canva.png")

# 3. YOUTUBE
def gen_youtube():
    img = create_radial_gradient((50, 10, 10), (15, 15, 18))
    draw = ImageDraw.Draw(img)
    # Ambient red glow
    draw.ellipse([140, 140, 460, 420], fill=(255, 0, 0, 40))
    # Red rounded rectangle
    x0, y0, x1, y1 = 170, 200, 430, 360
    draw.rounded_rectangle([x0, y0, x1, y1], radius=44, fill=(255, 0, 0, 255))
    # White play triangle
    draw.polygon([(275, 240), (275, 320), (345, 280)], fill=(255, 255, 255, 255))
    add_pill_label(draw, "YOUTUBE PREMIUM", (255, 0, 0))
    img.save("assets/katalog/youtube.png")

# 4. CHATGPT
def gen_chatgpt():
    img = create_radial_gradient((16, 163, 127), (10, 20, 24))
    draw = ImageDraw.Draw(img)
    # Subtle geometric rosette
    cx, cy = 300, 270
    draw.ellipse([cx - 100, cy - 100, cx + 100, cy + 100], fill=(16, 163, 127, 40))
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        ox = int(cx + 42 * math.cos(rad))
        oy = int(cy + 42 * math.sin(rad))
        draw.ellipse([ox - 48, oy - 48, ox + 48, oy + 48], outline=(255, 255, 255, 220), width=8)
    draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(255, 255, 255, 255))
    add_pill_label(draw, "CHATGPT PLUS GPT-4o", (16, 163, 127))
    img.save("assets/katalog/chatgpt.png")

# 5. SPOTIFY
def gen_spotify():
    img = create_radial_gradient((30, 180, 80), (18, 18, 18))
    draw = ImageDraw.Draw(img)
    cx, cy = 300, 270
    # Green circle
    draw.ellipse([cx - 100, cy - 100, cx + 100, cy + 100], fill=(30, 215, 96, 255))
    # 3 Curved black soundwaves
    draw.arc([cx - 70, cy - 55, cx + 70, cy + 45], start=205, end=335, fill=(18, 18, 18), width=16)
    draw.arc([cx - 60, cy - 30, cx + 60, cy + 50], start=205, end=335, fill=(18, 18, 18), width=14)
    draw.arc([cx - 50, cy - 8, cx + 50, cy + 55], start=205, end=335, fill=(18, 18, 18), width=12)
    add_pill_label(draw, "SPOTIFY PREMIUM", (30, 215, 96), text_color=(18, 18, 18))
    img.save("assets/katalog/spotify.png")

# 6. CAPCUT
def gen_capcut():
    img = create_radial_gradient((0, 160, 255), (10, 14, 20))
    draw = ImageDraw.Draw(img)
    cx, cy = 300, 270
    # Futuristic twin trapezoids
    draw.polygon([(200, 200), (280, 200), (230, 340), (150, 340)], fill=(0, 210, 255, 255))
    draw.polygon([(320, 200), (400, 200), (450, 340), (370, 340)], fill=(255, 255, 255, 255))
    draw.ellipse([270, 240, 330, 300], fill=(0, 210, 255, 255))
    add_pill_label(draw, "CAPCUT PRO", (0, 210, 255), text_color=(10, 14, 20))
    img.save("assets/katalog/capcut.png")

# 7. MICROSOFT 365
def gen_microsoft():
    img = create_radial_gradient((11, 40, 90), (8, 15, 30))
    draw = ImageDraw.Draw(img)
    # 4 Microsoft tiles
    cx, cy = 300, 260
    s = 64
    g = 12
    # Red (Top-Left)
    draw.rounded_rectangle([cx - s - g, cy - s - g, cx - g, cy - g], radius=8, fill=(242, 80, 34))
    # Green (Top-Right)
    draw.rounded_rectangle([cx + g, cy - s - g, cx + s + g, cy - g], radius=8, fill=(127, 186, 0))
    # Blue (Bottom-Left)
    draw.rounded_rectangle([cx - s - g, cy + g, cx - g, cy + s + g], radius=8, fill=(0, 164, 239))
    # Yellow (Bottom-Right)
    draw.rounded_rectangle([cx + g, cy + g, cx + s + g, cy + s + g], radius=8, fill=(255, 185, 0))
    add_pill_label(draw, "MICROSOFT 365 + 1TB", (0, 164, 239))
    img.save("assets/katalog/microsoft365.png")

# 8. DISNEY+
def gen_disney():
    img = create_radial_gradient((17, 60, 207), (4, 7, 20))
    draw = ImageDraw.Draw(img)
    cx, cy = 300, 270
    # Ambient star arch
    draw.arc([cx - 130, cy - 110, cx + 130, cy + 90], start=180, end=360, fill=(130, 210, 255), width=8)
    draw.ellipse([cx + 120, cy - 20, cx + 134, cy - 6], fill=(255, 255, 255))
    # Disney 'D'
    draw.arc([cx - 70, cy - 80, cx + 70, cy + 80], start=270, end=90, fill=(255, 255, 255), width=24)
    draw.line([(cx - 70, cy - 80), (cx - 70, cy + 80)], fill=(255, 255, 255), width=24)
    # Plus sign
    draw.line([(cx + 80, cy - 10), (cx + 80, cy + 30)], fill=(130, 210, 255), width=10)
    draw.line([(cx + 60, cy + 10), (cx + 100, cy + 10)], fill=(130, 210, 255), width=10)
    add_pill_label(draw, "DISNEY+ HOTSTAR", (17, 60, 207))
    img.save("assets/katalog/disney.png")

# 9. CLAUDE
def gen_claude():
    img = create_radial_gradient((217, 119, 6), (28, 24, 20))
    draw = ImageDraw.Draw(img)
    cx, cy = 300, 260
    # Anthropic starburst rays
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = cx + int(85 * math.cos(rad))
        y1 = cy + int(85 * math.sin(rad))
        draw.line([(cx, cy), (x1, y1)], fill=(225, 140, 30), width=16)
    draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(255, 240, 210))
    add_pill_label(draw, "CLAUDE 3.5 SONNET", (217, 119, 6))
    img.save("assets/katalog/claude.png")

# 10. TURNITIN
def gen_turnitin():
    img = create_radial_gradient((0, 112, 121), (10, 37, 64))
    draw = ImageDraw.Draw(img)
    cx, cy = 300, 260
    # Document shape
    w, h = 130, 160
    x0, y0 = cx - w//2, cy - h//2
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=14, fill=(255, 255, 255))
    # Document lines
    draw.rounded_rectangle([x0 + 20, y0 + 30, x0 + w - 20, y0 + 40], radius=4, fill=(0, 112, 121))
    draw.rounded_rectangle([x0 + 20, y0 + 55, x0 + w - 20, y0 + 65], radius=4, fill=(200, 210, 220))
    draw.rounded_rectangle([x0 + 20, y0 + 80, x0 + w - 40, y0 + 90], radius=4, fill=(200, 210, 220))
    # Big verified green check badge
    bx, by = cx + 35, cy + 45
    draw.ellipse([bx - 32, by - 32, bx + 32, by + 32], fill=(34, 197, 94))
    draw.line([(bx - 14, by), (bx - 4, by + 10), (bx + 14, by - 10)], fill=(255, 255, 255), width=6)
    add_pill_label(draw, "TURNITIN NO-REPO", (0, 112, 121))
    img.save("assets/katalog/turnitin.png")

# 11. VPN
def gen_vpn():
    img = create_radial_gradient((2, 132, 199), (8, 16, 38))
    draw = ImageDraw.Draw(img)
    cx, cy = 300, 260
    # Shield
    draw.polygon([(cx, cy - 95), (cx + 85, cy - 50), (cx + 85, cy + 35), (cx, cy + 95), (cx - 85, cy + 35), (cx - 85, cy - 50)], fill=(2, 132, 199))
    # Lock inner
    draw.rounded_rectangle([cx - 36, cy - 10, cx + 36, cy + 45], radius=8, fill=(255, 255, 255))
    draw.arc([cx - 24, cy - 45, cx + 24, cy - 5], start=180, end=360, fill=(255, 255, 255), width=10)
    draw.ellipse([cx - 8, cy + 10, cx + 8, cy + 26], fill=(2, 132, 199))
    add_pill_label(draw, "EXPRESS / NORD VPN", (2, 132, 199))
    img.save("assets/katalog/vpn.png")

# 12. GOOGLE ONE
def gen_googleone():
    img = create_radial_gradient((240, 243, 249), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    cx, cy = 300, 260
    # 4-color Google ring
    r = 85
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=0, end=90, fill=(52, 168, 83), width=24) # Green
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=90, end=180, fill=(251, 188, 5), width=24) # Yellow
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=180, end=270, fill=(234, 67, 53), width=24) # Red
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=270, end=360, fill=(66, 133, 244), width=24) # Blue
    # Big stylized "1" in center
    draw.rounded_rectangle([cx - 10, cy - 50, cx + 12, cy + 45], radius=4, fill=(66, 133, 244))
    draw.polygon([(cx - 28, cy - 25), (cx - 10, cy - 50), (cx - 10, cy - 35)], fill=(66, 133, 244))
    add_pill_label(draw, "GOOGLE ONE CLOUD", (66, 133, 244))
    img.save("assets/katalog/googleone.png")

print("Generating 12 images...")
gen_netflix()
gen_canva()
gen_youtube()
gen_chatgpt()
gen_spotify()
gen_capcut()
gen_microsoft()
gen_disney()
gen_claude()
gen_turnitin()
gen_vpn()
gen_googleone()
print("All 12 images generated successfully!")

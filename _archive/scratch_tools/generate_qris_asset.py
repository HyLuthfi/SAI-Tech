import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 640, 860
img = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

# Try fonts
try:
    font_bold_lg = ImageFont.truetype("arialbd.ttf", 26)
    font_bold_md = ImageFont.truetype("arialbd.ttf", 20)
    font_bold_sm = ImageFont.truetype("arialbd.ttf", 14)
    font_regular = ImageFont.truetype("arial.ttf", 13)
    font_qris = ImageFont.truetype("arialbd.ttf", 36)
except:
    font_bold_lg = ImageFont.load_default()
    font_bold_md = ImageFont.load_default()
    font_bold_sm = ImageFont.load_default()
    font_regular = ImageFont.load_default()
    font_qris = ImageFont.load_default()

# 1. Top Header Banner
# Red accent top line
draw.rectangle([0, 0, W, 8], fill=(229, 9, 20))

# QRIS Logo banner
draw.rectangle([0, 8, W, 100], fill=(255, 255, 255))

# Draw QRIS text logo
draw.text((40, 32), "QRIS", font=font_qris, fill=(20, 20, 25))
draw.text((145, 36), "QR Code Standar\nPembayaran Nasional", font=font_regular, fill=(100, 100, 110))

# GPN Logo Box on top right
draw.rounded_rectangle([W - 140, 28, W - 40, 76], radius=6, fill=(220, 30, 40))
draw.text((W - 120, 42), "GPN", font=font_bold_md, fill=(255, 255, 255))

# Divider line
draw.line([(30, 105), (W - 30, 105)], fill=(220, 220, 230), width=1)

# 2. Merchant Details Box
draw.text((40, 125), "SAI TECH INDONESIA", font=font_bold_lg, fill=(0, 0, 77))
draw.text((40, 160), "NMID : ID1024395810294", font=font_bold_sm, fill=(80, 80, 95))
draw.text((40, 182), "A01", font=font_regular, fill=(130, 130, 145))

# Printed date / validity
draw.text((W - 180, 160), "VERIFIKASI RESMI", font=font_bold_sm, fill=(34, 197, 94))
draw.text((W - 180, 182), "ASPI / BI APPROVED", font=font_regular, fill=(120, 120, 130))

# 3. QR Code Box
qr_x0, qr_y0, qr_s = 70, 215, 500
draw.rounded_rectangle([qr_x0 - 15, qr_y0 - 15, qr_x0 + qr_s + 15, qr_y0 + qr_s + 15], radius=16, fill=(255, 255, 255), outline=(220, 220, 230), width=2)

# Generate high-contrast QR Matrix pattern
import random
random.seed(42)

grid_n = 29
cell_s = qr_s // grid_n
ox = qr_x0 + (qr_s - (grid_n * cell_s)) // 2
oy = qr_y0 + (qr_s - (grid_n * cell_s)) // 2

# Draw Finder Pattern (Top-Left, Top-Right, Bottom-Left)
def draw_finder(gx, gy):
    # Outer 7x7 black
    draw.rectangle([ox + gx*cell_s, oy + gy*cell_s, ox + (gx+7)*cell_s, oy + (gy+7)*cell_s], fill=(10, 10, 25))
    # Inner 5x5 white
    draw.rectangle([ox + (gx+1)*cell_s, oy + (gy+1)*cell_s, ox + (gx+6)*cell_s, oy + (gy+6)*cell_s], fill=(255, 255, 255))
    # Center 3x3 black
    draw.rectangle([ox + (gx+2)*cell_s, oy + (gy+2)*cell_s, ox + (gx+5)*cell_s, oy + (gy+5)*cell_s], fill=(10, 10, 25))

draw_finder(0, 0)
draw_finder(grid_n - 7, 0)
draw_finder(0, grid_n - 7)

# Fill QR data cells
for gx in range(grid_n):
    for gy in range(grid_n):
        # Skip finder patterns
        in_tl = (gx < 8 and gy < 8)
        in_tr = (gx >= grid_n - 8 and gy < 8)
        in_bl = (gx < 8 and gy >= grid_n - 8)
        # Center logo space (5x5)
        in_center = (gx >= 12 and gx <= 16 and gy >= 12 and gy <= 16)
        if not (in_tl or in_tr or in_bl or in_center):
            if random.random() > 0.48:
                draw.rectangle([ox + gx*cell_s, oy + gy*cell_s, ox + (gx+1)*cell_s - 1, oy + (gy+1)*cell_s - 1], fill=(10, 10, 25))

# Center logo box
cx_box = ox + 11 * cell_s
cy_box = oy + 11 * cell_s
c_size = 7 * cell_s
draw.rounded_rectangle([cx_box - 2, cy_box - 2, cx_box + c_size + 2, cy_box + c_size + 2], radius=10, fill=(255, 255, 255), outline=(220, 220, 230), width=1)
draw.rounded_rectangle([cx_box + 4, cy_box + 4, cx_box + c_size - 4, cy_box + c_size - 4], radius=8, fill=(0, 0, 77))
draw.text((cx_box + 14, cy_box + 22), "SAI", font=font_bold_lg, fill=(224, 189, 106))
draw.text((cx_box + 16, cy_box + 54), "TECH", font=font_bold_sm, fill=(255, 255, 255))

# 4. Bottom Information & Payment Brands
foot_y = qr_y0 + qr_s + 35
draw.text((W // 2 - 130, foot_y), "SATU QRIS UNTUK SEMUA PEMBAYARAN", font=font_bold_sm, fill=(80, 80, 95))

# Brands pill bar
brands_y = foot_y + 30
draw.rounded_rectangle([40, brands_y, W - 40, brands_y + 44], radius=10, fill=(246, 246, 249), outline=(230, 230, 238), width=1)
brands_text = "BCA  •  MANDIRI  •  BRI  •  BNI  •  GOPAY  •  OVO  •  DANA  •  SHOPEEPAY"
bbox = draw.textbbox((0, 0), brands_text, font=font_bold_sm)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) // 2, brands_y + 14), brands_text, font=font_bold_sm, fill=(0, 0, 77))

os.makedirs("assets/ritovex", exist_ok=True)
img.save("assets/ritovex/qris_saitech.png", "PNG", quality=95)
print("QRIS SAI Tech asset generated successfully at assets/ritovex/qris_saitech.png!")

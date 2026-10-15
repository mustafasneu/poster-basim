"""Kılavuz ekran görüntüleri için tarafsız bir örnek poster üretir."""

from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw

W, H = 2400, 1200
img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

# Yumuşak degrade zemin
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(18 + 40 * t), int(38 + 90 * t), int(90 + 120 * t)))

# Oran kontrolü için tam daireler (sünme olursa elips görünürler)
for cx, cy, r, renk in [
    (600, 600, 320, (250, 204, 21)),
    (1400, 480, 190, (248, 113, 113)),
    (1900, 780, 260, (52, 211, 153)),
]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=renk)

# Kare ızgara — parça birleştirme hizasını göstermek için
for x in range(0, W, 100):
    d.line([(x, 0), (x, H)], fill=(255, 255, 255, 60), width=1)
for y in range(0, H, 100):
    d.line([(0, y), (W, y)], fill=(255, 255, 255, 60), width=1)

# Köşegen çizgiler
for i in range(0, W + H, 160):
    d.line([(i, 0), (i - H, H)], fill=(255, 255, 255), width=2)

# Merkezde bir hedef işareti
for r in range(60, 300, 60):
    d.arc([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r], 0, 360, fill=(15, 23, 42), width=6)

d.rectangle([40, 40, W - 40, H - 40], outline=(255, 255, 255), width=8)

cikti = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ornek_poster.jpg")
img.save(cikti, "JPEG", quality=92)
print(cikti, img.size, math.pi)

# powered by Ömer ÖZTÜRK & Mustafa ŞEKER

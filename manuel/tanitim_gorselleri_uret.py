#!/usr/bin/env python3
"""docs/ tanıtım sayfasının görsellerini üretir.

Ekran görüntülerini web için küçültür ve paylaşım kartını (Open Graph) çizer.
Çalıştırma: .venv/bin/python manuel/tanitim_gorselleri_uret.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

KOK = Path(__file__).resolve().parent.parent
KAYNAK = KOK / "manuel" / "gorseller"
HEDEF = KOK / "docs" / "img"

# (kaynak dosya, hedef ad, web'de görünecek azami genişlik)
EKRAN_GORUNTULERI = [
    ("05_iyilestirme.png", "arayuz.png", 1150),
    ("10_dizme_modu.png", "dizme.png", 1150),
]

MAVI_KOYU = (23, 37, 84)
MAVI = (37, 99, 235)
KIRMIZI = (239, 68, 68)
BEYAZ = (255, 255, 255)


def yazi_tipi(boyut: int, kalin: bool = False) -> ImageFont.FreeTypeFont:
    adaylar = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if kalin
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if kalin
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for yol in adaylar:
        if Path(yol).exists():
            return ImageFont.truetype(yol, boyut)
    return ImageFont.load_default(boyut)


def ekran_goruntulerini_kucult() -> None:
    for kaynak_ad, hedef_ad, genislik in EKRAN_GORUNTULERI:
        kaynak = KAYNAK / kaynak_ad
        with Image.open(kaynak) as im:
            im = im.convert("RGB")
            if im.width > genislik:
                oran = genislik / im.width
                im = im.resize((genislik, round(im.height * oran)), Image.LANCZOS)
            im.save(HEDEF / hedef_ad, optimize=True)
        print(f"{hedef_ad}: {im.width}×{im.height}")


def paylasim_karti() -> None:
    """1200×630 Open Graph kartı: koyu mavi zemin, altı A4 karosu, başlık."""
    W, H = 1200, 630
    kart = Image.new("RGB", (W, H), MAVI_KOYU)
    ciz = ImageDraw.Draw(kart)

    # Kesme kılavuzu dokusu
    for x in range(0, W, 60):
        ciz.line([(x, 0), (x, H)], fill=(32, 49, 103), width=1)
    for y in range(0, H, 60):
        ciz.line([(0, y), (W, y)], fill=(32, 49, 103), width=1)

    # Sağ tarafta 3×2 karo düzeni. Tek bir görsel üretilip karolara kırpılıyor;
    # amaç "aynı resim altı kez basılmış" değil "tek resim bölünmüş" göstermek.
    kx, ky = 700, 175
    ic_w, ic_h = 136, 92
    kenar = 7
    bosluk = 9
    eser = Image.new("RGB", (ic_w * 3, ic_h * 2))
    e_ciz = ImageDraw.Draw(eser)
    for y in range(eser.height):  # dikey mavi geçiş
        t = y / eser.height
        e_ciz.line(
            [(0, y), (eser.width, y)],
            fill=(round(30 + 26 * t), round(58 + 131 * t), round(138 + 110 * t)),
        )
    e_ciz.ellipse([12, 30, 148, 166], fill=(253, 224, 71))
    e_ciz.ellipse([176, 8, 268, 100], fill=(248, 113, 113))
    e_ciz.ellipse([286, 74, 396, 184], fill=(52, 211, 153))
    for r in (14, 28, 42):
        e_ciz.ellipse([166 - r, 96 - r, 166 + r, 96 + r], outline=(15, 23, 42), width=3)

    for satir in range(2):
        for sutun in range(3):
            x0 = kx + sutun * (ic_w + 2 * kenar + bosluk)
            y0 = ky + satir * (ic_h + 2 * kenar + bosluk)
            ciz.rectangle([x0, y0, x0 + ic_w + 2 * kenar, y0 + ic_h + 2 * kenar], fill=BEYAZ)
            parca = eser.crop((sutun * ic_w, satir * ic_h, (sutun + 1) * ic_w, (satir + 1) * ic_h))
            kart.paste(parca, (x0 + kenar, y0 + kenar))

    orta_x = kx + ic_w + 2 * kenar + bosluk // 2
    orta_y = ky + ic_h + 2 * kenar + bosluk // 2
    ciz.ellipse([orta_x - 26, orta_y - 26, orta_x + 26, orta_y + 26], outline=KIRMIZI, width=5)

    # Simge — uygulamanın kendi dosyası
    with Image.open(KOK / "simge.png") as simge:
        simge = simge.convert("RGBA").resize((72, 72), Image.LANCZOS)
        kart.paste(simge, (80, 80), simge)

    ciz.text((172, 96), "Poster Basım", font=yazi_tipi(34, kalin=True), fill=BEYAZ)

    baslik = ["Görseli A4 kağıtlara", "bölün, poster olarak", "yazdırın"]
    y = 205
    for satir in baslik:
        ciz.text((80, y), satir, font=yazi_tipi(52, kalin=True), fill=BEYAZ)
        y += 66

    ciz.text(
        (80, 432),
        "Oranı bozmaz · kurulum istemez · dosyanız\nbilgisayarınızdan çıkmaz",
        font=yazi_tipi(26),
        fill=(191, 219, 254),
        spacing=12,
    )
    ciz.text((80, 530), "Windows · macOS · Linux · ücretsiz, açık kaynak",
             font=yazi_tipi(22), fill=(147, 178, 240))

    kart.save(HEDEF / "onizleme-karti.png", optimize=True)
    print(f"onizleme-karti.png: {W}×{H}")


def main() -> None:
    HEDEF.mkdir(parents=True, exist_ok=True)
    shutil.copy2(KOK / "simge.png", HEDEF / "simge.png")
    ekran_goruntulerini_kucult()
    paylasim_karti()


if __name__ == "__main__":
    main()

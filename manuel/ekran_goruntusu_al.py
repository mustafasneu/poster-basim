"""Kullanım kılavuzu için uygulamayı gerçekten çalıştırıp ekran görüntülerini alır.

Kullanım:  .venv/bin/python manuel/ekran_goruntusu_al.py
Çıktı:     manuel/gorseller/*.png
"""

from __future__ import annotations

import os
import subprocess
import sys
import tkinter as tk

PROJE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJE)

from poster_bolme import SunmesizBaskiApp  # noqa: E402

GORSEL_DIZINI = os.path.join(PROJE, "manuel", "gorseller")
ORNEK = os.path.join(PROJE, "manuel", "ornek_poster.jpg")
os.makedirs(GORSEL_DIZINI, exist_ok=True)


def cek(root: tk.Misc, ad: str, tum_ekran: bool = False):
    """Uygulama penceresini çeker.

    Diyalog pencereleri ayrı bir toplevel olduğu için tüm ekran alınır; ancak
    arka plandaki diğer programlar kılavuza sızmasın diye görüntü, uygulama
    penceresinin çerçevesine kırpılır.
    """
    root.update()
    yol = os.path.join(GORSEL_DIZINI, f"{ad}.png")
    if not tum_ekran:
        subprocess.run(["import", "-window", str(root.winfo_id()), yol], check=True)
    else:
        subprocess.run(["import", "-window", "root", yol], check=True)
        from PIL import Image

        with Image.open(yol) as ekran:
            sol = max(0, root.winfo_rootx())
            ust = max(0, root.winfo_rooty() - 44)  # pencere başlık çubuğu
            sag = min(ekran.width, root.winfo_rootx() + root.winfo_width())
            alt = min(ekran.height, root.winfo_rooty() + root.winfo_height())
            ekran.crop((sol, ust, sag, alt)).save(yol)
    print("çekildi:", yol)


def pano_kirp(root: tk.Misc, widget: tk.Misc, ad: str, pay: int = 0):
    """Pencereyi çekip yalnızca verilen widget'ın alanını saklar.

    Tek bir ayar bölümünü göstermek için tüm pencereyi basmak gerekmiyor;
    kılavuzda bölüm yakın plandan daha okunur çıkıyor.
    """
    from PIL import Image

    root.update()
    yol = os.path.join(GORSEL_DIZINI, f"{ad}.png")
    subprocess.run(["import", "-window", str(root.winfo_id()), yol], check=True)
    with Image.open(yol) as pencere:
        sol = max(0, widget.winfo_rootx() - root.winfo_rootx() - pay)
        ust = max(0, widget.winfo_rooty() - root.winfo_rooty() - pay)
        sag = min(pencere.width, sol + widget.winfo_width() + 2 * pay)
        alt = min(pencere.height, ust + widget.winfo_height() + 2 * pay)
        pencere.crop((sol, ust, sag, alt)).save(yol)
    print("çekildi:", yol)


def main():
    root = tk.Tk()
    app = SunmesizBaskiApp(root)
    adimlar = []

    def sirala(*isler):
        """İşleri olay döngüsünde sırayla çalıştırır."""
        adimlar.extend(isler)
        calistir()

    def calistir():
        if not adimlar:
            root.after(300, root.destroy)
            return
        is_ = adimlar.pop(0)
        try:
            is_()
        finally:
            root.after(450, calistir)

    def dosya_dialogu():
        # Tk'nin kendi dosya seçme penceresi; açıkken görüntüsü alınıp kapatılır.
        root.after(900, lambda: cek(root, "02_dosya_secme", tum_ekran=True))
        root.after(1600, lambda: root.tk.eval("catch {destroy .__tk_filedialog}"))
        try:
            from tkinter import filedialog

            filedialog.askopenfilename(
                title="Bir Resim Dosyası Seçin", initialdir=os.path.join(PROJE, "manuel")
            )
        except tk.TclError:
            pass

    def link_dialogu():
        # "İnternetten Link ile Al" penceresi; örnek bir adresle açılıp görüntüsü alınır.
        root.clipboard_clear()
        root.clipboard_append("https://ornek.com/poster-gorseli.jpg")
        root.after(900, lambda: cek(root, "02b_link_penceresi", tum_ekran=True))
        root.after(
            1600,
            lambda: [w.destroy() for w in root.winfo_children() if isinstance(w, tk.Toplevel)],
        )
        app.linkten_al()

    def pdf_sayfa_dialogu():
        # Çok sayfalı PDF seçilince çıkan pencere; kılavuz için üç sayfalık örnek üretilir.
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas as pdf_canvas

        ornek_pdf = os.path.join(GORSEL_DIZINI, "_ornek_cok_sayfa.pdf")
        tuval = pdf_canvas.Canvas(ornek_pdf, pagesize=A4)
        for sayfa in range(3):
            tuval.drawString(80, 700, f"Ornek afis tasarimi - sayfa {sayfa + 1}")
            tuval.showPage()
        tuval.save()

        root.after(900, lambda: cek(root, "02c_pdf_sayfa_secme", tum_ekran=True))
        root.after(
            1600,
            lambda: [w.destroy() for w in root.winfo_children() if isinstance(w, tk.Toplevel)],
        )
        try:
            app.resmi_yukle(ornek_pdf)
        finally:
            root.after(2200, lambda: os.path.exists(ornek_pdf) and os.remove(ornek_pdf))

    def dizme_ekrani():
        """'Çok resmi tek A4'e diz' modunun ekran görüntüsü (örnek resimler üretilir)."""
        import shutil
        import tempfile

        from PIL import Image, ImageDraw

        gecici = tempfile.mkdtemp(prefix="dizme_ornek_")
        renkler = [(198, 70, 70), (70, 155, 100), (70, 100, 190), (215, 165, 55),
                   (140, 75, 175), (60, 160, 175)]
        for sira in range(1, 10):
            boy = (900, 600) if sira % 2 else (600, 900)  # farklı oranlar: sığdırma görünsün
            ornek = Image.new("RGB", boy, renkler[sira % len(renkler)])
            ImageDraw.Draw(ornek).text((40, 40), f"Resim {sira}", fill=(255, 255, 255))
            ornek.save(os.path.join(gecici, f"resim{sira}.png"))

        app.mod.set("dizme")
        app.modu_uygula()
        app._dizme_dosyalari_ekle(
            [os.path.join(gecici, ad) for ad in os.listdir(gecici)]
        )
        app.dizme_sutun.set(3)
        app.dizme_satir.set(3)
        app.dizme_onizle()
        root.after(700, lambda: cek(root, "10_dizme_modu"))
        root.after(1400, lambda: (app.mod.set("poster"), app.modu_uygula(),
                                  shutil.rmtree(gecici, ignore_errors=True)))

    def rapor_ekrani():
        root.after(700, lambda: cek(root, "11_baski_raporu", tum_ekran=True))
        root.after(1500, lambda: [w.destroy() for w in root.winfo_children()
                                  if isinstance(w, tk.Toplevel)])
        app.baski_raporunu_goster()

    def birebir_ekrani():
        root.after(900, lambda: cek(root, "12_birebir_onizleme", tum_ekran=True))
        root.after(1700, lambda: [w.destroy() for w in root.winfo_children()
                                  if isinstance(w, tk.Toplevel)])
        app.gercek_boyut_onizleme()

    def uret():
        from tkinter import messagebox

        gercek_showinfo = messagebox.showinfo

        def yakala_ve_kapat(*a, **k):
            root.after(1200, lambda: cek(root, "06_tamamlandi", tum_ekran=True))
            root.after(2000, lambda: root.tk.eval("catch {destroy .__tk__messagebox}"))
            return gercek_showinfo(*a, **k)

        messagebox.showinfo = yakala_ve_kapat
        try:
            app.parcala_ve_pdf_yap()
        finally:
            messagebox.showinfo = gercek_showinfo

    sirala(
        lambda: cek(root, "01_baslangic"),
        dosya_dialogu,
        link_dialogu,
        pdf_sayfa_dialogu,
        lambda: app.resmi_yukle(ORNEK),
        lambda: cek(root, "03_resim_yuklendi"),
        lambda: (
            app.sutun_spin.delete(0, tk.END),
            app.sutun_spin.insert(0, "3"),
            app.satir_spin.delete(0, tk.END),
            app.satir_spin.insert(0, "2"),
        ),
        lambda: cek(root, "04_bolme_ayarlari"),
        lambda: (
            app.onayar_combo.set("Fotoğraf"),
            app.onayari_uygula(),
            app.kontrast_slider.set(1.25),
            app.renk_slider.set(1.35),
            app.onizlemeyi_guncelle(),
        ),
        lambda: cek(root, "05_iyilestirme"),
        # Çıktı formatı kutuları: kılavuzda üçü de işaretli görünsün, sonra
        # üretim varsayılan ayarlarla sürsün diye geri kapatılır.
        lambda: (
            app.kayipsiz_var.set(True),
            app.tiff_var.set(True),
            app.png_var.set(True),
        ),
        lambda: pano_kirp(root, app.format_cercevesi, "04d_cikti_formati"),
        lambda: (
            app.kayipsiz_var.set(False),
            app.tiff_var.set(False),
            app.png_var.set(False),
        ),
        rapor_ekrani,
        birebir_ekrani,
        uret,
        lambda: cek(root, "07_bitis_durumu"),
        dizme_ekrani,
        lambda: None,
    )
    root.mainloop()


if __name__ == "__main__":
    main()

# powered by Omer OZTURK

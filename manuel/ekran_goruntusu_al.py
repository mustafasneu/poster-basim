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
            app.keskinlik_slider.set(2.4),
            app.kontrast_slider.set(1.35),
            app.renk_slider.set(1.45),
            app.parlaklik_slider.set(1.1),
            app.onizlemeyi_guncelle(),
        ),
        lambda: cek(root, "05_iyilestirme"),
        uret,
        lambda: cek(root, "07_bitis_durumu"),
    )
    root.mainloop()


if __name__ == "__main__":
    main()

# powered by Omer OZTURK

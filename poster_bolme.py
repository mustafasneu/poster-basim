#!/usr/bin/env python3
"""Poster Basım — sünmesiz & oran korumalı A4 poster üretici (Tkinter arayüz).

Bir resmi seçip N sütun x M satır A4 sayfaya bölerek yazdırmaya hazır tek bir
PDF üretir. Parçalar ayrıca JPEG olarak da kaydedilir.

Bu dosya KENDİ KENDİNE KURULUR: çift tıklandığında ya da `python3 poster_bolme.py`
ile çalıştırıldığında eksik bağımlılıkları (Pillow, ReportLab, gerekirse tkinter'lı
bir Python) yanındaki `.venv` klasörüne kendisi kurar, sonra kendini yeniden başlatır.
Kullanıcının hiçbir şey yüklemesi gerekmez.

Windows, Linux ve macOS üzerinde aynı şekilde çalışır.
"""

from __future__ import annotations

import os
import subprocess
import sys

# ---------------------------------------------------------------- kendi kendine kurulum
GEREKLI_PAKETLER = (
    "pillow>=10",
    "reportlab>=4",
    "pypdfium2>=4",
    "pillow-heif>=0.16",
    "rawpy>=0.21",
)
# Bu üç bileşen programın açılması için şart değildir; kurulamazlarsa yalnızca ilgili
# biçim devre dışı kalır, program çalışmaya devam eder (bkz. _calisir_mi).
PDF_PAKETI = "pypdfium2>=4"
HEIC_PAKETI = "pillow-heif>=0.16"
RAW_PAKETI = "rawpy>=0.21"
PROJE_DIZINI = os.path.dirname(os.path.abspath(__file__))
VENV_DIZINI = os.path.join(PROJE_DIZINI, ".venv")

# PyInstaller ile tek dosyalık pakete dönüştürüldüğünde program geçici bir klasörden
# çalışır: bağımlılıklar zaten pakette olduğu için kurulum adımları atlanır, kalıcı
# dosyalar (AI modeli) kullanıcının uygulama verisi klasörüne yazılır.
PAKETLENMIS = getattr(sys, "frozen", False)
KAYNAK_DIZINI = getattr(sys, "_MEIPASS", PROJE_DIZINI)  # simge gibi salt-okunur dosyalar


def veri_dizini() -> str:
    """Kalıcı dosyalar için kullanıcıya ait klasör (paketlenmiş sürümde şart)."""
    if not PAKETLENMIS:
        return PROJE_DIZINI
    ev = os.path.expanduser("~")
    if os.name == "nt":
        kok = os.environ.get("LOCALAPPDATA", os.path.join(ev, "AppData", "Local"))
    elif sys.platform == "darwin":
        kok = os.path.join(ev, "Library", "Application Support")
    else:
        kok = os.environ.get("XDG_DATA_HOME", os.path.join(ev, ".local", "share"))
    yol = os.path.join(kok, "PosterBasim")
    os.makedirs(yol, exist_ok=True)
    return yol
YENIDEN_BASLATMA_ISARETI = "POSTER_BOLME_KURULUM"

WINDOWS = os.name == "nt"
MACOS = sys.platform == "darwin"

# Windows'ta yardımcı komutlar çalışırken siyah konsol penceresi açılmasın.
_SESSIZ = {"creationflags": 0x08000000} if WINDOWS else {}

if WINDOWS:
    _TKINTER_COZUMU = (
        "python.org adresinden Python'u kurup kurulum sırasında\n"
        "'tcl/tk and IDLE' seçeneğini işaretli bırakın."
    )
elif MACOS:
    _TKINTER_COZUMU = (
        "Şu komutu bir kez çalıştırın:  brew install python-tk\n"
        "(Homebrew yoksa python.org kurulumu tkinter ile birlikte gelir.)"
    )
else:
    _TKINTER_COZUMU = (
        "Şu komutlardan dağıtımınıza uyanı bir kez çalıştırın:\n"
        "  Debian/Ubuntu : sudo apt install -y python3-tk\n"
        "  Fedora        : sudo dnf install -y python3-tkinter\n"
        "  Arch          : sudo pacman -S --needed tk"
    )


def _venv_python(venv: str) -> str:
    alt = "Scripts" if WINDOWS else "bin"
    return os.path.join(venv, alt, "python.exe" if WINDOWS else "python")


def _pencereli_python(python_yolu: str) -> str:
    """Windows'ta konsolsuz yorumlayıcı (pythonw.exe) varsa onu döndürür."""
    if not WINDOWS:
        return python_yolu
    aday = os.path.join(os.path.dirname(python_yolu), "pythonw.exe")
    return aday if os.path.exists(aday) else python_yolu


def _calisir_mi(python_yolu: str) -> bool:
    """İlgili yorumlayıcıda hem tkinter hem de görüntü/PDF paketleri var mı?"""
    if not os.path.exists(python_yolu):
        return False
    try:
        return (
            subprocess.run(
                [python_yolu, "-c", "import tkinter, PIL, reportlab"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=90,
                **_SESSIZ,
            ).returncode
            == 0
        )
    except (OSError, subprocess.SubprocessError):
        return False


def _python_adaylari() -> list[str]:
    """İşletim sistemine göre denenecek Python yorumlayıcısı yolları."""
    from shutil import which

    surumler = ("3.13", "3.12", "3.11", "3.10", "3")
    adaylar = [sys.executable]

    if WINDOWS:
        # Windows'ta yorumlayıcılar sabit bir yerde durmaz; PATH ve py başlatıcısı
        # üzerinden bulunur, ayrıca tipik kurulum dizinlerine bakılır.
        adaylar += [which(f"python{s}") for s in surumler]
        adaylar.append(which("python"))
        yerel = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
        for s in surumler:
            kisa = s.replace(".", "")
            adaylar += [
                os.path.join(yerel, "Programs", "Python", f"Python{kisa}", "python.exe"),
                f"C:\\Python{kisa}\\python.exe",
                f"C:\\Program Files\\Python{kisa}\\python.exe",
            ]
    else:
        for s in surumler:
            adaylar += [
                which(f"python{s}"),
                os.path.expanduser(f"~/.local/bin/python{s}"),
                f"/usr/bin/python{s}",
                f"/usr/local/bin/python{s}",
            ]
            if MACOS:  # Homebrew (Intel + Apple Silicon) ve python.org kurulumları
                adaylar += [
                    f"/opt/homebrew/bin/python{s}",
                    f"/opt/homebrew/opt/python@{s}/bin/python{s}",
                    f"/usr/local/opt/python@{s}/bin/python{s}",
                    f"/Library/Frameworks/Python.framework/Versions/{s}/bin/python{s}",
                ]

    gorulen: list[str] = []
    for aday in adaylar:
        if aday and aday not in gorulen:
            gorulen.append(aday)
    return gorulen


def _tkinterli_python_bul() -> str | None:
    """Tkinter'ı olan bir Python yorumlayıcısı ara; yoksa uv ile indirmeyi dene."""
    for aday in _python_adaylari():
        if not os.path.exists(aday):
            continue
        try:
            if (
                subprocess.run(
                    [aday, "-c", "import tkinter"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=90,
                    **_SESSIZ,
                ).returncode
                == 0
            ):
                return aday
        except (OSError, subprocess.SubprocessError):
            continue

    uv = _uv_bul()
    if uv:  # uv'nin taşınabilir Python'ları tkinter ile birlikte gelir
        _bildir("Uygun Python indiriliyor (tek seferlik)...")
        try:
            subprocess.run([uv, "python", "install", "3.12"], timeout=900, check=False, **_SESSIZ)
            cikti = subprocess.run(
                [uv, "python", "find", "3.12"],
                capture_output=True,
                text=True,
                timeout=120,
                **_SESSIZ,
            ).stdout.strip()
            if cikti and os.path.exists(cikti):
                return cikti
        except (OSError, subprocess.SubprocessError):
            pass
    return None


def _uv_bul() -> str | None:
    from shutil import which

    if WINDOWS:
        yollar = (
            os.path.expanduser("~\\.local\\bin\\uv.exe"),
            os.path.expanduser("~\\.cargo\\bin\\uv.exe"),
        )
    else:
        yollar = (
            os.path.expanduser("~/.local/bin/uv"),
            os.path.expanduser("~/.cargo/bin/uv"),
            "/opt/homebrew/bin/uv",
            "/usr/local/bin/uv",
        )
    return which("uv") or next((y for y in yollar if os.path.exists(y)), None)


_pencere = None
_etiket = None


def _bildir(mesaj: str):
    """Kurulum adımlarını hem konsola hem (mümkünse) küçük bir pencereye yazar."""
    global _pencere, _etiket
    print(f"[kurulum] {mesaj}", flush=True)
    try:
        import tkinter as _tk

        if _pencere is None:
            _pencere = _tk.Tk()
            _pencere.title("Poster Basım — ilk kurulum")
            _pencere.geometry("460x120")
            _etiket = _tk.Label(_pencere, text=mesaj, wraplength=420, justify="left", pady=20)
            _etiket.pack(expand=True, fill="both")
        _etiket.config(text=mesaj)
        _pencere.update()
    except Exception:  # arayüz yoksa sessizce konsola devam
        pass


def _kurulum_penceresini_kapat():
    global _pencere
    if _pencere is not None:
        try:
            _pencere.destroy()
        except Exception:
            pass
        _pencere = None


def _bagimliliklari_hazirla():
    """Eksikler varsa kurar ve programı hazır ortamla yeniden başlatır."""
    if PAKETLENMIS:  # paket zaten her şeyi içeriyor
        return
    try:  # her şey yerindeyse hiçbir şey yapma
        import tkinter  # noqa: F401
        import PIL  # noqa: F401
        import reportlab  # noqa: F401

        return
    except ImportError:
        pass

    if os.environ.get(YENIDEN_BASLATMA_ISARETI):  # sonsuz döngü koruması
        raise SystemExit(
            "Bağımlılıklar kurulmasına rağmen yüklenemedi.\n"
            f"Şu ortamı silip tekrar deneyin: {VENV_DIZINI}"
        )

    if _calisir_mi(_venv_python(VENV_DIZINI)):
        _yeniden_baslat(_venv_python(VENV_DIZINI))

    _bildir("İlk çalıştırma: gerekli bileşenler kuruluyor, lütfen bekleyin...")
    temel_python = _tkinterli_python_bul()
    if temel_python is None:
        _kurulum_penceresini_kapat()
        raise SystemExit(
            "Grafik arayüz için gereken 'tkinter' bulunamadı ve otomatik kurulamadı.\n"
            + _TKINTER_COZUMU
        )

    if not os.path.exists(_venv_python(VENV_DIZINI)):
        _bildir("Çalışma ortamı oluşturuluyor...")
        subprocess.run(
            [temel_python, "-m", "venv", VENV_DIZINI], check=False, timeout=600, **_SESSIZ
        )

    venv_py = _venv_python(VENV_DIZINI)
    if not os.path.exists(venv_py):
        _kurulum_penceresini_kapat()
        raise SystemExit(f"Çalışma ortamı oluşturulamadı: {VENV_DIZINI}")

    _bildir("Görüntü ve PDF bileşenleri indiriliyor (Pillow, ReportLab)...")
    uv = _uv_bul()
    komutlar = []
    if uv:
        komutlar.append([uv, "pip", "install", "--python", venv_py, *GEREKLI_PAKETLER])
    komutlar.append([venv_py, "-m", "pip", "install", "--quiet", *GEREKLI_PAKETLER])
    for komut in komutlar:
        try:
            subprocess.run(komut, check=False, timeout=1800, **_SESSIZ)
        except (OSError, subprocess.SubprocessError):
            continue
        if _calisir_mi(venv_py):
            break

    if not _calisir_mi(venv_py):
        _kurulum_penceresini_kapat()
        raise SystemExit(
            "Bileşenler kurulamadı. İnternet bağlantınızı kontrol edip tekrar deneyin.\n"
            f"Elle kurmak için:  {venv_py} -m pip install " + " ".join(GEREKLI_PAKETLER)
        )

    _bildir("Kurulum tamam, program başlatılıyor...")
    _yeniden_baslat(venv_py)


def _yeniden_baslat(python_yolu: str):
    _kurulum_penceresini_kapat()
    ortam = dict(os.environ, **{YENIDEN_BASLATMA_ISARETI: "1"})
    dosya = os.path.abspath(__file__)
    if WINDOWS:  # os.exec* Windows'ta pencereyi kaybettirir; alt süreç olarak başlat
        arayuz_py = _pencereli_python(python_yolu)
        raise SystemExit(subprocess.run([arayuz_py, dosya, *sys.argv[1:]], env=ortam).returncode)
    os.execve(python_yolu, [python_yolu, dosya, *sys.argv[1:]], ortam)


_bagimliliklari_hazirla()

# ---------------------------------------------------------------------------- program
import tkinter as tk  # noqa: E402
from datetime import datetime  # noqa: E402
from tkinter import filedialog, font as tkfont, messagebox, ttk  # noqa: E402

from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageStat, ImageTk  # noqa: E402
from reportlab.lib.pagesizes import A4, landscape  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

# Sürgüler oynatılırken tam çözünürlükte filtre uygulamak büyük resimlerde
# arayüzü kilitliyor; önizleme bu boyuta küçültülmüş kopya üzerinden yapılır.
ONIZLEME_CALISMA_BOYUTU = (1000, 1000)
ONIZLEME_GOSTERIM_BOYUTU = (760, 560)

# Tk, Xft desteği olmadan derlenmişse yalnızca çekirdek X11 fontları görünür ve
# Type1 aileleri "ı" harfini basamaz. Modern aileler varsa onlar, yoksa Türkçe
# harfleri doğru gösteren tek çekirdek font olan "fixed" kullanılır.
TURKCE_FONT_ADAYLARI = ("DejaVu Sans", "Noto Sans", "Liberation Sans", "Ubuntu")


def turkce_fontu_ayarla(root: tk.Misc) -> str:
    mevcut = set(tkfont.families(root))
    secilen = next((f for f in TURKCE_FONT_ADAYLARI if f in mevcut), "fixed")
    for ad in (
        "TkDefaultFont",
        "TkTextFont",
        "TkMenuFont",
        "TkHeadingFont",
        "TkTooltipFont",
        "TkCaptionFont",
        "TkSmallCaptionFont",
        "TkIconFont",
    ):
        try:
            tkfont.nametofont(ad, root=root).configure(family=secilen, size=10)
        except tk.TclError:
            pass
    return secilen


# Tk'nin kendi pencereleri (dosya seçme, uyarı kutuları) İngilizce gelir ve Tk
# Türkçe çeviri paketiyle dağıtılmaz; katalogu burada kendimiz dolduruyoruz.
# Baştaki "&" işareti klavye kısayolunu belirtir, ekranda görünmez.
TK_TURKCE_METINLER = {
    "&Cancel": "İ&ptal",
    "Cancel": "İptal",
    "&OK": "&Tamam",
    "OK": "Tamam",
    "&Open": "&Aç",
    "Open": "Aç",
    "&Save": "&Kaydet",
    "Save As": "Farklı Kaydet",
    "&Directory:": "&Klasör:",
    "&Selection:": "&Seçim:",
    "File &name:": "Dosya &adı:",
    "File &names:": "Dosya &adları:",
    "Files of &type:": "Dosya &türü:",
    "Show &Hidden Directories": "&Gizli klasörleri göster",
    "Show &Hidden Files and Directories": "&Gizli dosya ve klasörleri göster",
    "All Files": "Tüm Dosyalar",
    "&Yes": "&Evet",
    "Yes": "Evet",
    "&No": "&Hayır",
    "No": "Hayır",
    "&Abort": "&Durdur",
    "&Retry": "&Yeniden dene",
    "&Ignore": "&Yoksay",
    "Error": "Hata",
    "Warning": "Uyarı",
    "Directory \"%1$s\" does not exist.": "\"%1$s\" adlı klasör yok.",
    'File "%1$s" does not exist.': '"%1$s" adlı dosya yok.',
    'Invalid file name "%1$s".': '"%1$s" geçerli bir dosya adı değil.',
    'Cannot change to the directory "%1$s".\nPermission denied.': (
        '"%1$s" klasörüne girilemiyor.\nErişim izni yok.'
    ),
    'File "%1$s" already exists.\nDo you want to overwrite it?': (
        '"%1$s" adlı dosya zaten var.\nÜzerine yazılsın mı?'
    ),
}


def tk_pencerelerini_turkcelestir(root: tk.Misc):
    """Tk'nin hazır pencerelerindeki düğme ve etiketleri Türkçeye çevirir."""
    try:
        root.tk.eval("package require msgcat")
        for ingilizce, turkce in TK_TURKCE_METINLER.items():
            # Genel ad alanına yazılır; Tk'nin ::tk ad alanındaki aramaları buraya düşer.
            root.tk.call("::msgcat::mcset", "tr", ingilizce, turkce)
        root.tk.call("::msgcat::mclocale", "tr")
    except tk.TclError:  # msgcat yoksa arayüz İngilizce kalır, program çalışmaya devam eder
        pass


# --------------------------------------------------------------- desteklenen biçimler
# Illustrator'ın modern .ai dosyaları aslında PDF'tir; PDF motoruyla açılırlar.
PDF_UZANTILARI = (".pdf", ".ai")
HEIC_UZANTILARI = (".heic", ".heif")
RAW_UZANTILARI = (
    ".cr2", ".cr3", ".nef", ".arw", ".dng", ".orf", ".rw2", ".raf", ".srw", ".pef",
)
# Pillow'un kendi okuyucularıyla açılanlar (PSD dahil: birleştirilmiş görüntüyü verir).
PILLOW_UZANTILARI = (
    ".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff", ".psd", ".gif", ".ppm",
)
TUM_UZANTILAR = PILLOW_UZANTILARI + PDF_UZANTILARI + HEIC_UZANTILARI + RAW_UZANTILARI

PDF_DPI = 300  # afiş tasarımları vektörel olduğu için baskı çözünürlüğünde taranır
PDF_EN_BUYUK_KENAR = 12000  # devasa sayfalarda bellek taşmasın diye üst sınır


def pdfium_getir():
    """PDF okuma bileşenini getirir; yoksa Türkçe açıklamayla ImportError yükseltir."""
    try:
        import pypdfium2  # noqa: PLC0415 — yalnızca PDF açılırken gerekiyor
    except ImportError as hata:
        raise ImportError(
            "PDF okuma bileşeni (pypdfium2) kurulu değil.\n\n"
            "Kurmak için şu komutu bir kez çalıştırın:\n"
            f"{sys.executable} -m pip install {PDF_PAKETI}"
        ) from hata
    return pypdfium2


def pdf_sayfa_sayisi(yol: str) -> int:
    pdfium = pdfium_getir()
    try:
        belge = pdfium.PdfDocument(yol)
    except Exception as hata:  # pypdfium2 kendi hata tiplerini kullanır
        raise ValueError(f"PDF açılamadı:\n{hata}") from hata
    try:
        return len(belge)
    finally:
        belge.close()


def pdf_sayfasini_goruntuye_cevir(yol: str, sayfa_no: int = 1, dpi: int = PDF_DPI) -> Image.Image:
    """PDF'in bir sayfasını görüntüye çevirir (sayfa_no 1'den başlar).

    dpi düşürülerek hızlı önizleme de alınabilir; poster üretimi PDF_DPI kullanır.
    """
    pdfium = pdfium_getir()
    try:
        belge = pdfium.PdfDocument(yol)
    except Exception as hata:
        raise ValueError(f"PDF açılamadı:\n{hata}") from hata

    try:
        if not 1 <= sayfa_no <= len(belge):
            raise ValueError(f"PDF {len(belge)} sayfa; {sayfa_no}. sayfa yok.")
        sayfa = belge[sayfa_no - 1]
        genislik_punto, yukseklik_punto = sayfa.get_size()
        olcek = dpi / 72
        # Çok büyük sayfalarda (afiş boyu PDF) çözünürlüğü sınırla.
        en_buyuk = max(genislik_punto, yukseklik_punto) * olcek
        if en_buyuk > PDF_EN_BUYUK_KENAR:
            olcek *= PDF_EN_BUYUK_KENAR / en_buyuk
        try:
            goruntu = sayfa.render(scale=olcek).to_pil()
        except Exception as hata:
            raise ValueError(f"PDF sayfası görüntüye çevrilemedi:\n{hata}") from hata
        return goruntu.convert("RGB")
    finally:
        belge.close()


def rgb_yap(img: Image.Image) -> Image.Image:
    """Baskıya uygun RGB'ye çevirir (CMYK, 16-bit, gri ve paletli kaynaklar dahil)."""
    if img.mode == "RGB":
        return img
    if img.mode in ("RGBA", "LA", "PA") or (img.mode == "P" and "transparency" in img.info):
        img = img.convert("RGBA")
        zemin = Image.new("RGB", img.size, (255, 255, 255))
        zemin.paste(img, mask=img.split()[-1])
        return zemin
    if img.mode in ("I;16", "I;16B", "I", "F"):  # 16/32-bit tarama çıktıları
        return img.point(lambda d: d * (1 / 256)).convert("L").convert("RGB")
    return img.convert("RGB")  # CMYK, L, P ve diğerleri


def heic_goruntusu_ac(yol: str) -> Image.Image:
    """iPhone HEIC/HEIF dosyasını açar."""
    try:
        import pillow_heif  # noqa: PLC0415 — yalnızca HEIC açılırken gerekiyor
    except ImportError as hata:
        raise ValueError(
            "iPhone (HEIC) dosyaları için gereken bileşen kurulu değil.\n\n"
            "Ya şu komutu bir kez çalıştırın:\n"
            f"{sys.executable} -m pip install {HEIC_PAKETI}\n\n"
            "ya da fotoğrafı iPhone'dan “En Uyumlu / JPEG” olarak aktarın."
        ) from hata

    pillow_heif.register_heif_opener()
    try:
        img = Image.open(yol)
        img.load()
    except (OSError, ValueError) as hata:
        raise ValueError(f"HEIC dosyası açılamadı:\n{hata}") from hata
    return img


def raw_goruntusu_ac(yol: str) -> Image.Image:
    """Fotoğraf makinesi ham (RAW) dosyasını açar ve normal görüntüye çevirir."""
    try:
        import rawpy  # noqa: PLC0415 — yalnızca RAW açılırken gerekiyor
    except ImportError as hata:
        raise ValueError(
            "Ham (RAW) fotoğraf dosyaları için gereken bileşen kurulu değil.\n\n"
            "Ya şu komutu bir kez çalıştırın:\n"
            f"{sys.executable} -m pip install {RAW_PAKETI}\n\n"
            "ya da fotoğrafı JPEG/TIFF olarak dışa aktarın."
        ) from hata

    try:
        with rawpy.imread(yol) as ham:
            # use_camera_wb: fotoğraf makinesinin beyaz ayarı korunur, renkler doğru çıkar.
            dizi = ham.postprocess(use_camera_wb=True, output_bps=8)
    except Exception as hata:  # rawpy kendi hata tiplerini kullanır
        raise ValueError(f"RAW dosyası açılamadı:\n{hata}") from hata
    return Image.fromarray(dizi)


def kaynak_goruntusu_ac(yol: str) -> Image.Image:
    """Desteklenen her biçimi açıp baskıya hazır RGB görüntü döndürür (PDF hariç)."""
    uzanti = os.path.splitext(yol)[1].lower()
    if uzanti in HEIC_UZANTILARI:
        img = heic_goruntusu_ac(yol)
    elif uzanti in RAW_UZANTILARI:
        img = raw_goruntusu_ac(yol)
    else:
        try:
            img = Image.open(yol)
            img.load()
        except (OSError, ValueError) as hata:
            raise ValueError(f"Dosya açılamadı:\n{hata}") from hata
    img = ImageOps.exif_transpose(img)  # telefon fotoğraflarının yönünü düzeltir
    return rgb_yap(img)


EN_BUYUK_INDIRME = 60 * 1024 * 1024  # 60 MB; poster kaynağı için fazlasıyla yeterli
INDIRME_ZAMAN_ASIMI = 30


def linkten_resim_indir(baglanti: str, hedef_dizin: str) -> str:
    """Verilen web adresindeki resmi indirip yerel bir dosya yolu döndürür.

    Hata durumlarında kullanıcıya gösterilecek Türkçe açıklamayla ValueError atar.
    """
    import urllib.error
    import urllib.parse
    import urllib.request

    baglanti = baglanti.strip().strip("<>\"'")
    parcali = urllib.parse.urlparse(baglanti)
    if parcali.scheme not in ("http", "https") or not parcali.netloc:
        raise ValueError(
            "Bu bir web adresi değil.\n"
            "Adres http:// ya da https:// ile başlamalı.\n"
            "Örnek: https://ornek.com/resim.jpg"
        )

    # Bazı siteler tarayıcı dışı isteklere kapalıdır; sıradan bir tarayıcı gibi görünelim.
    istek = urllib.request.Request(
        baglanti,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; PosterBasim/1.0)",
            "Accept": "image/*,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(istek, timeout=INDIRME_ZAMAN_ASIMI) as yanit:
            tur = (yanit.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            bildirilen = yanit.headers.get("Content-Length")
            if bildirilen and bildirilen.isdigit() and int(bildirilen) > EN_BUYUK_INDIRME:
                raise ValueError(
                    f"Dosya çok büyük ({int(bildirilen) // 1048576} MB).\n"
                    f"En fazla {EN_BUYUK_INDIRME // 1048576} MB indirilebilir."
                )
            # Yalnızca açıkça web sayfası olanları burada eliyoruz. Pek çok site
            # (GitHub dahil) resim ve PDF'i "application/octet-stream" diye bildirir;
            # bu yüzden asıl karar, aşağıda dosyanın içeriğine bakılarak veriliyor.
            if tur.startswith("text/"):
                raise ValueError(
                    "Bu adres bir resim ya da PDF değil, web sayfası döndürüyor.\n"
                    "Görselin üzerine sağ tıklayıp “Resim adresini kopyala” deyin ve\n"
                    "kopyaladığınız adresi yapıştırın."
                )
            veri = yanit.read(EN_BUYUK_INDIRME + 1)
    except urllib.error.HTTPError as hata:
        raise ValueError(f"Adrese erişilemedi (sunucu {hata.code} döndürdü).") from hata
    except urllib.error.URLError as hata:
        raise ValueError(
            f"Bağlantı kurulamadı: {hata.reason}\nİnternet bağlantınızı kontrol edin."
        ) from hata
    except OSError as hata:
        raise ValueError(f"İndirme sırasında sorun çıktı:\n{hata}") from hata

    if len(veri) > EN_BUYUK_INDIRME:
        raise ValueError(f"Dosya {EN_BUYUK_INDIRME // 1048576} MB sınırını aşıyor.")
    if not veri:
        raise ValueError("Adres boş bir dosya döndürdü.")

    # İçeriği gerçekten açarak sınıyoruz; uzantıya ya da sunucunun bildirdiğine güvenmiyoruz.
    from io import BytesIO

    adres_uzantisi = os.path.splitext(urllib.parse.urlparse(baglanti).path)[1].lower()
    if veri[:5] == b"%PDF-":
        bicim = "pdf"
    elif adres_uzantisi in HEIC_UZANTILARI + RAW_UZANTILARI:
        # Bu biçimleri Pillow tanımaz; dosya kaydedilip kendi okuyucusuna bırakılır.
        bicim = adres_uzantisi.lstrip(".")
    else:
        try:
            with Image.open(BytesIO(veri)) as deneme:
                deneme.verify()
                bicim = (deneme.format or "img").lower()
        except (OSError, ValueError) as hata:
            raise ValueError(
                "İnen dosya açılabilir bir resim ya da PDF değil.\n"
                "Görselin doğrudan adresini kullandığınızdan emin olun."
            ) from hata

    ad = os.path.basename(urllib.parse.urlparse(baglanti).path) or f"linkten_resim.{bicim}"
    if "." not in ad:
        ad = f"{ad}.{bicim}"
    hedef = os.path.join(hedef_dizin, ad)
    with open(hedef, "wb") as dosya:
        dosya.write(veri)
    return hedef


def cikis_klasoru_hazirla(klasor_adi: str) -> str:
    """Yazılabilir bir çıktı klasörü oluşturur.

    macOS, uygulamaların Masaüstü ve Belgeler klasörlerine erişimini izne bağlar; izin
    verilmemişse yazma "Operation not permitted" ile düşer. O yüzden masaüstü tutmazsa
    sırayla Belgeler ve ev dizini denenir — kullanıcı üretimi kaybetmesin.
    """
    ev = os.path.expanduser("~")
    adaylar = [masaustu_yolu(), os.path.join(ev, "Documents"), os.path.join(ev, "Belgeler"), ev]
    ilk_hata: OSError | None = None

    gorulen = []
    for kok in adaylar:
        if not kok or kok in gorulen or not os.path.isdir(kok):
            continue
        gorulen.append(kok)
        yol = os.path.join(kok, "Poster_Parcalari", klasor_adi)
        try:
            os.makedirs(yol, exist_ok=True)
            # Klasörün açılması yazma izni demek değil; gerçekten yazarak sınıyoruz.
            deneme = os.path.join(yol, ".yazma_denemesi")
            with open(deneme, "w", encoding="utf-8") as dosya:
                dosya.write("x")
            os.remove(deneme)
            return yol
        except OSError as hata:
            if ilk_hata is None:
                ilk_hata = hata
            continue

    ek = ""
    if MACOS:
        ek = (
            "\n\nmacOS, programların Masaüstü klasörüne erişimini izne bağlar.\n"
            "Sistem Ayarları → Gizlilik ve Güvenlik → Dosyalar ve Klasörler yolundan\n"
            "Terminal'e (ya da Python'a) 'Masaüstü Klasörü' iznini verip tekrar deneyin."
        )
    raise OSError(f"Çıktı klasörü oluşturulamadı: {ilk_hata}{ek}")


def pencere_simgesini_ayarla(root: tk.Misc):
    """Program simgesini pencereye/görev çubuğuna uygular; referansı geri döndürür."""
    simge_yolu = os.path.join(KAYNAK_DIZINI, "simge.png")
    if not os.path.exists(simge_yolu):
        return None
    try:
        simge = ImageTk.PhotoImage(Image.open(simge_yolu))
        root.iconphoto(True, simge)  # referans tutulmazsa simge kaybolur
        return simge
    except Exception:
        # Simge tamamen görsel bir ayrıntıdır; hangi sebeple olursa olsun
        # (eksik dosya, Tk eklentisi bulunamadı, paketleme sorunu) programın
        # açılmasını engellememeli.
        return None


def masaustu_yolu() -> str:
    """Masaüstü klasörünü bul (işletim sistemi ve dil ayarından bağımsız)."""
    ev = os.path.expanduser("~")

    if WINDOWS:
        # Masaüstü OneDrive'a taşınmış ya da başka bir sürücüye alınmış olabilir;
        # doğru yol yalnızca kayıt defterindeki kullanıcı klasörü kaydında durur.
        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
            ) as anahtar:
                yol = os.path.expandvars(winreg.QueryValueEx(anahtar, "Desktop")[0])
            if os.path.isdir(yol):
                return yol
        except (ImportError, OSError):
            pass
    elif not MACOS:  # Linux: kullanıcının yerelleştirilmiş klasör adı
        try:
            yol = subprocess.run(
                ["xdg-user-dir", "DESKTOP"], capture_output=True, text=True, timeout=5
            ).stdout.strip()
            if yol and os.path.isdir(yol):
                return yol
        except (OSError, subprocess.SubprocessError):
            pass

    for aday in ("Desktop", "Masaüstü", "Escritorio", "Bureau", "Schreibtisch"):
        yol = os.path.join(ev, aday)
        if os.path.isdir(yol):
            return yol
    return ev


# ------------------------------------------------------------------ görüntü iyileştirme
A4_INC = (210 / 25.4, 297 / 25.4)  # A4'ün inç cinsinden kısa ve uzun kenarı
IYI_DPI = 200  # bu değerin üstü baskıda net görünür
KABUL_DPI = 120  # bunun altı yakından bakınca belirgin şekilde pikselli


# Kâğıt telafisi: mat kâğıt mürekkebi emer, renk ve kontrast söner; parlak kâğıt
# neredeyse ekrandaki gibi basar. (kontrast, doygunluk, parlaklık) çarpanları.
KAGIT_TELAFISI = {
    "Belirtme": (1.0, 1.0, 1.0),
    "Mat kâğıt": (1.12, 1.18, 1.03),
    "Parlak / fotoğraf kâğıdı": (1.0, 1.05, 1.0),
    "Düz fotokopi kâğıdı": (1.18, 1.25, 1.06),
}


def srgb_yap(img: Image.Image) -> tuple[Image.Image, str | None]:
    """Görselde gömülü ICC profili varsa sRGB'ye çevirir.

    Adobe RGB ya da ProPhoto profilli bir görsel profilsiz basılırsa renkler
    soluk ve kaymış çıkar. Dönüşüm bunu baştan önler.
    """
    profil = img.info.get("icc_profile")
    if not profil:
        return img, None
    try:
        from io import BytesIO  # noqa: PLC0415

        from PIL import ImageCms  # noqa: PLC0415

        kaynak = ImageCms.ImageCmsProfile(BytesIO(profil))
        ad = ImageCms.getProfileDescription(kaynak).strip()
        if "srgb" in ad.lower():
            return img, ad
        hedef = ImageCms.createProfile("sRGB")
        cevrilmis = ImageCms.profileToProfile(img, kaynak, hedef, outputMode="RGB")
        return (cevrilmis or img), ad
    except Exception:  # ImageCms kendi hata tiplerini kullanır; profil bozuksa dokunma
        return img, None


def doygunluk_riski(img: Image.Image) -> float:
    """Baskıda sönme riski taşıyan aşırı doygun piksellerin oranını kabaca ölçer.

    Gerçek gamut denetimi CMYK profili ister; burada yalnızca "bu renkler mürekkeple
    zor karşılanır" uyarısı için basit bir ölçüt kullanılıyor.
    """
    kucuk = img.convert("RGB")
    kucuk.thumbnail((400, 400))
    import statistics  # noqa: PLC0415

    pikseller = list(kucuk.getdata())
    if not pikseller:
        return 0.0
    riskli = sum(1 for r, g, b in pikseller if max(r, g, b) - min(r, g, b) > 200)
    return riskli / len(pikseller)


def otomatik_duzelt(img: Image.Image) -> Image.Image:
    """Seviye (kontrast) ve beyaz dengesini otomatik düzeltir.

    Telefon fotoğrafları ve taramalar çoğu zaman soluk ve renk sapmalıdır; bu iki
    düzeltme, elle sürgü oynatmadan en büyük kazancı sağlar.
    """
    duzeltilmis = ImageOps.autocontrast(img, cutoff=0.5)  # uçlardaki %0.5'i kırparak seviye

    # Gri-dünya varsayımı: sahnenin ortalaması nötr gri olmalı; kanal ortalamaları
    # buna göre eşitlenince mavi/sarı renk sapması kalkar.
    kanallar = duzeltilmis.split()
    if len(kanallar) < 3:
        return duzeltilmis
    ortalamalar = [ImageStat.Stat(k).mean[0] for k in kanallar[:3]]
    hedef = sum(ortalamalar) / 3
    if min(ortalamalar) < 1:  # neredeyse siyah görüntüde oran hesabı anlamsız
        return duzeltilmis
    olcekli = [
        k.point(lambda d, o=hedef / m: min(255, int(d * o))) for k, m in zip(kanallar, ortalamalar)
    ]
    return Image.merge("RGB", olcekli)


def gurultu_azalt(img: Image.Image, seviye: int) -> Image.Image:
    """Gürültüyü azaltır (0 kapalı, 1 hafif, 2 orta, 3 güçlü).

    Büyütülecek görsellerde şart: gürültü de büyür ve baskıda kum gibi görünür.
    """
    if seviye <= 0:
        return img
    pencere = 3 if seviye < 3 else 5
    suzulmus = img.filter(ImageFilter.MedianFilter(pencere))
    if seviye == 1:  # hafif: detayı korumak için yarı yarıya karıştırılır
        return Image.blend(img, suzulmus, 0.5)
    return suzulmus


def keskinlestir(img: Image.Image, yaricap: float, miktar: float, esik: float) -> Image.Image:
    """Unsharp mask — baskı için doğru keskinleştirme yöntemi.

    yaricap: etkilenen kenar kalınlığı (piksel), miktar: güç (%), esik: bu farkın
    altındaki değişimlere dokunulmaz (düz alanlardaki gürültü keskinleşmesin diye).
    """
    if miktar <= 0 or yaricap <= 0:
        return img
    return img.filter(
        ImageFilter.UnsharpMask(radius=yaricap, percent=int(miktar), threshold=int(esik))
    )


def poster_olculeri_inc(
    sutun: int, satir: int, dikey: bool, kenar_mm: float = 0.0
) -> tuple[float, float]:
    """Seçilen matrisin inç cinsinden poster ölçüsü.

    Yazıcının basamadığı kenar payı posterden düşülür; yoksa hesaplanan ölçü
    gerçekte elde edilenden büyük çıkar.
    """
    kisa, uzun = A4_INC
    sayfa_w, sayfa_h = (kisa, uzun) if dikey else (uzun, kisa)
    kenar_inc = kenar_mm / 25.4
    return sutun * max(0.1, sayfa_w - 2 * kenar_inc), satir * max(0.1, sayfa_h - 2 * kenar_inc)


def baski_cozunurlugu(
    img: Image.Image, sutun: int, satir: int, dikey: bool, kenar_mm: float = 0.0
) -> float:
    """Görselin bu matriste basıldığında ulaşacağı gerçek DPI değeri."""
    genislik_inc, yukseklik_inc = poster_olculeri_inc(sutun, satir, dikey, kenar_mm)
    if genislik_inc <= 0 or yukseklik_inc <= 0:
        return 0.0
    return min(img.width / genislik_inc, img.height / yukseklik_inc)


def akilli_buyut(
    img: Image.Image, hedef_dpi: int, sutun: int, satir: int, dikey: bool, kenar_mm: float = 0.0
):
    """Görseli hedef DPI'a ulaşacak şekilde büyütür (Lanczos + hafif keskinleştirme).

    Var olmayan detayı üretmez; pikselleri blok blok değil yumuşak geçişli gösterir.
    Aşırı büyütme kalite kazandırmadığı için en fazla 4 katla sınırlıdır.
    """
    mevcut = baski_cozunurlugu(img, sutun, satir, dikey, kenar_mm)
    if mevcut <= 0 or mevcut >= hedef_dpi:
        return img, 1.0
    kat = min(hedef_dpi / mevcut, 4.0)
    yeni = (max(1, round(img.width * kat)), max(1, round(img.height * kat)))
    buyutulmus = img.resize(yeni, Image.Resampling.LANCZOS)
    # Büyütme yumuşatır; hafif unsharp ile kenarlar geri toplanır.
    return keskinlestir(buyutulmus, yaricap=1.0, miktar=60, esik=3), kat


# ------------------------------------------------------------------- AI büyütme eklentisi
# Programla birlikte gelmez: hesaplama motoru ve model ~35 MB'dır ve bu özelliği
# kullanmayacak herkesin bunu indirmesi anlamsız olurdu. Kullanıcı isterse indirir.
AI_MODEL_ADRESI = (
    "https://huggingface.co/Xenova/swin2SR-classical-sr-x2-64/resolve/main/onnx/"
    "model_quantized.onnx"
)
AI_MODEL_DOSYASI = os.path.join(veri_dizini(), "eklentiler", "swin2sr_x2.onnx")
AI_MOTOR_PAKETI = "onnxruntime"
AI_MODEL_MB = 21
AI_MOTOR_MB = 15
AI_KARO = 128  # bellek ve süre dengesi; büyütülürken kare kare işlenir
AI_BINDIRME = 16  # karo eklerinde iz kalmasın diye örtüşme payı


def ai_eklentisi_hazir_mi() -> tuple[bool, bool]:
    """(hesaplama motoru var mı, model dosyası var mı) bilgisini döndürür."""
    try:
        import onnxruntime  # noqa: F401, PLC0415
        motor = True
    except ImportError:
        motor = False
    return motor, os.path.exists(AI_MODEL_DOSYASI)


def ai_eklentisini_kur(bildir) -> None:
    """Hesaplama motorunu ve modeli indirir. Hata durumunda Türkçe ValueError atar."""
    motor, model = ai_eklentisi_hazir_mi()

    if not motor and PAKETLENMIS:
        raise ValueError(
            "Bu sürümde AI hesaplama motoru bulunamadı.\n"
            "Programın kaynak koddan çalışan sürümünü kullanın ya da güncel paketi indirin."
        )

    if not motor:
        bildir("Hesaplama motoru indiriliyor (~15 MB)...")
        try:
            sonuc = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", AI_MOTOR_PAKETI],
                timeout=1800,
                **_SESSIZ,
            )
        except (OSError, subprocess.SubprocessError) as hata:
            raise ValueError(f"Hesaplama motoru kurulamadı:\n{hata}") from hata
        if sonuc.returncode != 0 or not ai_eklentisi_hazir_mi()[0]:
            raise ValueError(
                "Hesaplama motoru (onnxruntime) kurulamadı.\n"
                "İnternet bağlantınızı kontrol edip tekrar deneyin."
            )

    if not model:
        bildir(f"Büyütme modeli indiriliyor (~{AI_MODEL_MB} MB)...")
        import urllib.error
        import urllib.request

        os.makedirs(os.path.dirname(AI_MODEL_DOSYASI), exist_ok=True)
        gecici = AI_MODEL_DOSYASI + ".indiriliyor"
        try:
            istek = urllib.request.Request(
                AI_MODEL_ADRESI, headers={"User-Agent": "PosterBasim/1.0"}
            )
            with urllib.request.urlopen(istek, timeout=120) as yanit, open(gecici, "wb") as dosya:
                toplam = int(yanit.headers.get("Content-Length") or 0)
                inen = 0
                while parca := yanit.read(1024 * 256):
                    dosya.write(parca)
                    inen += len(parca)
                    if toplam:
                        bildir(f"Büyütme modeli indiriliyor... %{inen * 100 // toplam}")
            os.replace(gecici, AI_MODEL_DOSYASI)
        except (urllib.error.URLError, OSError) as hata:
            if os.path.exists(gecici):
                os.remove(gecici)
            raise ValueError(f"Model indirilemedi:\n{hata}") from hata


def _ai_oturumu():
    import onnxruntime  # noqa: PLC0415

    return onnxruntime.InferenceSession(
        AI_MODEL_DOSYASI, providers=["CPUExecutionProvider"]
    )


def ai_karo_suresi() -> float:
    """Tek bir karonun bu bilgisayarda kaç saniye sürdüğünü ölçer (kalibrasyon).

    Süre donanıma göre 20 kat değişebildiği için sabit bir tahmin yanıltıcı olurdu;
    kullanıcıya kendi makinesinde ölçülmüş süre gösterilir.
    """
    import numpy as np  # noqa: PLC0415

    import time  # noqa: PLC0415

    oturum = _ai_oturumu()
    ad = oturum.get_inputs()[0].name
    # Gerçek görüntüye benzesin diye rastgele veri; sıfır dolu girdi olduğundan hızlı ölçülür.
    ornek = np.random.rand(1, 3, AI_KARO, AI_KARO).astype(np.float32)
    oturum.run(None, {ad: ornek})  # ilk çağrı ısınma; ölçüme katılmaz
    basla = time.time()
    oturum.run(None, {ad: ornek})
    # Karo kırpma, dizi dönüşümü ve birleştirme payı (ölçümle ~1.3 kat çıkıyor).
    return (time.time() - basla) * 1.3


def ai_karo_sayisi(img: Image.Image) -> int:
    adim = AI_KARO - AI_BINDIRME
    return max(1, -(-img.width // adim)) * max(1, -(-img.height // adim))


def ai_ile_buyut(img: Image.Image, ilerleme=None, iptal=None) -> Image.Image:
    """Görseli AI modeliyle 2 kat büyütür (karo karo işlenir).

    ilerleme: (yapilan, toplam) alan geri çağırım. iptal: çağrıldığında True dönerse
    işlem yarıda bırakılır ve None döner.
    """
    import numpy as np  # noqa: PLC0415

    oturum = _ai_oturumu()
    ad = oturum.get_inputs()[0].name
    adim = AI_KARO - AI_BINDIRME
    yarim = AI_BINDIRME // 2
    sonuc = Image.new("RGB", (img.width * 2, img.height * 2))
    toplam = ai_karo_sayisi(img)
    yapilan = 0

    for ust in range(0, img.height, adim):
        for sol in range(0, img.width, adim):
            if iptal is not None and iptal():
                return None
            sag = min(sol + AI_KARO, img.width)
            alt = min(ust + AI_KARO, img.height)
            karo = img.crop((sol, ust, sag, alt))
            gercek_w, gercek_h = karo.size
            dizi = np.asarray(karo, dtype=np.float32)
            if (gercek_w, gercek_h) != (AI_KARO, AI_KARO):
                # Model sabit ölçüde girdi ister; kenar karoları kenar pikseli
                # tekrarlanarak tamamlanır, çıktıda bu dolgu geri kırpılır.
                dizi = np.pad(
                    dizi,
                    ((0, AI_KARO - gercek_h), (0, AI_KARO - gercek_w), (0, 0)),
                    mode="edge",
                )
            girdi = dizi.transpose(2, 0, 1)[None] / 255.0
            cikti = oturum.run(None, {ad: girdi})[0][0].transpose(1, 2, 0)
            buyuk = Image.fromarray((np.clip(cikti, 0, 1) * 255).astype(np.uint8))
            buyuk = buyuk.crop((0, 0, gercek_w * 2, gercek_h * 2))

            # Örtüşen kenarlardan yarım pay kırpılır; böylece karo ekleri görünmez.
            kirp_sol = 0 if sol == 0 else yarim * 2
            kirp_ust = 0 if ust == 0 else yarim * 2
            sonuc.paste(
                buyuk.crop((kirp_sol, kirp_ust, buyuk.width, buyuk.height)),
                (sol * 2 + kirp_sol, ust * 2 + kirp_ust),
            )
            yapilan += 1
            if ilerleme is not None:
                ilerleme(yapilan, toplam)
    return sonuc


# Hazır ayarlar: (yarıçap, miktar %, eşik, gürültü, otomatik düzelt)
ONAYARLAR = {
    "Fotoğraf": (1.2, 110, 3, "Kapalı", True),
    "Grafik / Afiş": (0.8, 150, 0, "Kapalı", False),
    "Tarama / Eski baskı": (1.5, 90, 4, "Orta", True),
    "Telefon fotoğrafı": (1.0, 120, 4, "Hafif", True),
    "Dokunma (ham)": (0.0, 0, 0, "Kapalı", False),
}


# --------------------------------------------------------- kesim ve montaj işaretleri
# PDF metinlerinde ASCII kullanılır: ReportLab'ın gömülü yazı tipleri "ı, ş, ğ"
# harflerini basamaz ve bu harfler çıktıda kaybolur.
def kesim_isaretleri_ciz(
    pdf_canvas, ciz_x, ciz_y, ciz_w, ciz_h, cakisma_pt, satir, sutun, toplam_satir, toplam_sutun
):
    """Sayfaya kesim çizgileri, köşe işaretleri, hizalama hedefleri ve komşuluk etiketi çizer.

    Kesim çizgisi, bindirme payının bittiği yerdedir: kullanıcı oradan keserse
    komşu sayfayla tam olarak örtüşen bir kenar elde eder.
    """
    sol_pay = cakisma_pt if sutun > 0 else 0
    sag_pay = cakisma_pt if sutun < toplam_sutun - 1 else 0
    alt_pay = cakisma_pt if satir < toplam_satir - 1 else 0
    ust_pay = cakisma_pt if satir > 0 else 0

    kesim_sol = ciz_x + sol_pay
    kesim_sag = ciz_x + ciz_w - sag_pay
    kesim_alt = ciz_y + alt_pay
    kesim_ust = ciz_y + ciz_h - ust_pay

    # Kesim çizgisi: ince, kesikli, açık gri — baskıda göze batmaz, makasa yol gösterir.
    pdf_canvas.saveState()
    pdf_canvas.setStrokeColorRGB(0.55, 0.55, 0.55)
    pdf_canvas.setLineWidth(0.4)
    pdf_canvas.setDash(3, 3)
    pdf_canvas.rect(kesim_sol, kesim_alt, kesim_sag - kesim_sol, kesim_ust - kesim_alt)
    pdf_canvas.setDash()

    # Köşe işaretleri: kesim köşelerini kâğıdın kenarına taşıyan kısa tam çizgiler.
    uzunluk = 12
    pdf_canvas.setStrokeColorRGB(0.2, 0.2, 0.2)
    pdf_canvas.setLineWidth(0.6)
    for x in (kesim_sol, kesim_sag):
        for y in (kesim_alt, kesim_ust):
            yon_x = -1 if x == kesim_sol else 1
            yon_y = -1 if y == kesim_alt else 1
            pdf_canvas.line(x, y, x + yon_x * uzunluk, y)
            pdf_canvas.line(x, y, x, y + yon_y * uzunluk)

    # Hizalama hedefleri: bindirme şeridinin ortasında artı işaretleri. İki sayfa
    # üst üste getirildiğinde bu artılar çakışır; hizalama gözle yapılabilir hale gelir.
    if cakisma_pt > 2:
        pdf_canvas.setStrokeColorRGB(0.85, 0.2, 0.2)
        pdf_canvas.setLineWidth(0.5)
        art = 5
        hedefler = []
        if sag_pay:
            hedefler.append((kesim_sag + cakisma_pt / 2, (kesim_alt + kesim_ust) / 2))
        if sol_pay:
            hedefler.append((kesim_sol - cakisma_pt / 2, (kesim_alt + kesim_ust) / 2))
        if alt_pay:
            hedefler.append(((kesim_sol + kesim_sag) / 2, kesim_alt - cakisma_pt / 2))
        if ust_pay:
            hedefler.append(((kesim_sol + kesim_sag) / 2, kesim_ust + cakisma_pt / 2))
        for hx, hy in hedefler:
            pdf_canvas.line(hx - art, hy, hx + art, hy)
            pdf_canvas.line(hx, hy - art, hx, hy + art)

    # Komşuluk etiketi: hangi parça olduğu ve sağına/altına hangisinin geleceği.
    komsular = []
    if sutun < toplam_sutun - 1:
        komsular.append(f"saginda {satir + 1}-{sutun + 2}")
    if satir < toplam_satir - 1:
        komsular.append(f"altinda {satir + 2}-{sutun + 1}")
    etiket = f"Parca {satir + 1}-{sutun + 1}  (satir {satir + 1} / sutun {sutun + 1})"
    if komsular:
        etiket += " · " + ", ".join(komsular)
    # Etiket kâğıdın en altına, beyaz zemin üzerine yazılır: görselin üstüne binerse
    # koyu alanlarda okunmaz.
    pdf_canvas.setFont("Helvetica", 7)
    genislik = pdf_canvas.stringWidth(etiket, "Helvetica", 7)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.rect(2, 2, genislik + 8, 11, stroke=0, fill=1)
    pdf_canvas.setFillColorRGB(0.35, 0.35, 0.35)
    pdf_canvas.drawString(6, 5, etiket)
    pdf_canvas.restoreState()


def montaj_haritasi_ciz(pdf_canvas, sayfa_w, sayfa_h, toplam_satir, toplam_sutun, olcu_metni):
    """PDF'in ilk sayfasına, parçaların nereye geleceğini gösteren harita basar."""
    pdf_canvas.saveState()
    pdf_canvas.setFillColorRGB(0.1, 0.1, 0.1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(50, sayfa_h - 60, "MONTAJ HARITASI")
    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.drawString(
        50, sayfa_h - 78, f"{toplam_satir} satir x {toplam_sutun} sutun = "
        f"{toplam_satir * toplam_sutun} sayfa   |   yaklasik {olcu_metni}"
    )

    # Harita alanı: sayfa oranını koruyan bir ızgara.
    ust_bosluk, yan_bosluk = 110, 50
    alan_w = sayfa_w - 2 * yan_bosluk
    alan_h = sayfa_h - ust_bosluk - 90
    hucre = min(alan_w / toplam_sutun, alan_h / toplam_satir)
    izgara_w, izgara_h = hucre * toplam_sutun, hucre * toplam_satir
    baslangic_x = (sayfa_w - izgara_w) / 2
    baslangic_y = sayfa_h - ust_bosluk - izgara_h

    pdf_canvas.setFont("Helvetica-Bold", 11)
    for satir in range(toplam_satir):
        for sutun in range(toplam_sutun):
            x = baslangic_x + sutun * hucre
            y = baslangic_y + (toplam_satir - 1 - satir) * hucre
            pdf_canvas.setStrokeColorRGB(0.3, 0.3, 0.3)
            pdf_canvas.setFillColorRGB(0.97, 0.97, 0.97)
            pdf_canvas.rect(x, y, hucre, hucre, stroke=1, fill=1)
            pdf_canvas.setFillColorRGB(0.1, 0.1, 0.1)
            pdf_canvas.drawCentredString(
                x + hucre / 2, y + hucre / 2 - 4, f"{satir + 1}-{sutun + 1}"
            )

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(0.25, 0.25, 0.25)
    satirlar = [
        "1. Sayfalari %100 / Gercek Boyut olcegiyle yazdirin (Sayfaya Sigdir KAPALI).",
        "2. Her sayfayi kesikli cizgiden kesin; koselerdeki isaretler kesim yerini gosterir.",
        "3. Yukaridaki haritaya gore diziniz: 1-1 sol ust kosedir.",
        "4. Kirmizi arti isaretlerini ust uste getirerek yapistirin.",
        "5. Bu harita sayfasini yazdirmaniz sart degildir; yalnizca yol gostericidir.",
    ]
    for sira, metin in enumerate(satirlar):
        pdf_canvas.drawString(50, 78 - sira * 13, metin)
    pdf_canvas.restoreState()
    pdf_canvas.showPage()


def dogal_anahtar(metin: str):
    """'resim2' < 'resim10' olacak şekilde sıralama anahtarı (sözlük sırası yanıltır)."""
    import re

    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", metin)]


def a4_piksel(dikey: bool, dpi: int = PDF_DPI) -> tuple[int, int]:
    """A4 sayfanın verilen çözünürlükteki piksel ölçüsü (210 x 297 mm)."""
    kisa, uzun = round(210 / 25.4 * dpi), round(297 / 25.4 * dpi)
    return (kisa, uzun) if dikey else (uzun, kisa)


def resimleri_sayfaya_diz(
    goruntuler: list[Image.Image],
    sutun: int,
    satir: int,
    dikey: bool,
    kenar_mm: float = 10,
    aralik_mm: float = 4,
    dpi: int = PDF_DPI,
) -> Image.Image:
    """Verilen görüntüleri tek bir A4 sayfaya ızgara halinde yerleştirir.

    Her görüntü hücresine oranı korunarak sığdırılır ve hücrede ortalanır; hiçbir
    görüntü kırpılmaz ya da gerilmez.
    """
    sayfa_w, sayfa_h = a4_piksel(dikey, dpi)
    kenar = round(kenar_mm / 25.4 * dpi)
    aralik = round(aralik_mm / 25.4 * dpi)

    kullanilabilir_w = sayfa_w - 2 * kenar - aralik * (sutun - 1)
    kullanilabilir_h = sayfa_h - 2 * kenar - aralik * (satir - 1)
    if kullanilabilir_w <= 0 or kullanilabilir_h <= 0:
        raise ValueError(
            "Kenar boşluğu ve aralık, sayfaya sığmayacak kadar büyük.\n"
            "Değerleri küçültün ya da satır/sütun sayısını azaltın."
        )
    hucre_w = kullanilabilir_w // sutun
    hucre_h = kullanilabilir_h // satir

    sayfa = Image.new("RGB", (sayfa_w, sayfa_h), (255, 255, 255))
    for sira, goruntu in enumerate(goruntuler[: sutun * satir]):
        parca = rgb_yap(goruntu).copy()
        parca.thumbnail((hucre_w, hucre_h), Image.Resampling.LANCZOS)  # oranı korur
        s, u = sira % sutun, sira // sutun
        hucre_x = kenar + s * (hucre_w + aralik)
        hucre_y = kenar + u * (hucre_h + aralik)
        sayfa.paste(  # hücre içinde ortala
            parca,
            (hucre_x + (hucre_w - parca.width) // 2, hucre_y + (hucre_h - parca.height) // 2),
        )
    return sayfa


def jpeg_uyumlu(img: Image.Image) -> Image.Image:
    """Alfa kanallı / paletli / CMYK resimleri beyaz zemine düzleştirip RGB'ye çevirir."""
    return rgb_yap(img)


class SunmesizBaskiApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Poster Basım — Sünmesiz & Oran Korumalı A4 PDF Poster Oluşturucu")
        self.root.geometry("1150x780")
        self.root.minsize(950, 640)
        self.font_ailesi = turkce_fontu_ayarla(self.root)
        self.pencere_simgesi = pencere_simgesini_ayarla(self.root)
        tk_pencerelerini_turkcelestir(self.root)

        self.orijinal_img: Image.Image | None = None
        self.onizleme_kaynak: Image.Image | None = None
        self.islenen_onizleme: Image.Image | None = None
        self.resim_yolu: str | None = None
        self.son_cikis_klasoru: str | None = None
        self._filtre_isi: str | None = None
        self._indirme_dizini: str | None = None  # linkten inen resimler için geçici klasör
        self.mod = tk.StringVar(value="poster")
        self.dizme_dosyalari: list[str] = []
        self.kaynak_profili: str | None = None

        self.arayuz_tasarla()

    # ------------------------------------------------------------------ arayüz
    def arayuz_tasarla(self):
        sol_panel = ttk.Frame(self.root, padding=(15, 15, 15, 12))
        sol_panel.pack(side=tk.LEFT, fill=tk.Y)

        # Üretim düğmeleri EN ÖNCE paketlenir. Tk, yer kalmadığında en son paketleneni
        # kırpar; macOS'ta widget'lar daha uzun olduğu için bu düğmeler ekran dışında
        # kalıyordu. Önce paketlenince yerleri her sistemde garanti altında olur.
        eylem = ttk.Frame(sol_panel)
        eylem.pack(side=tk.BOTTOM, fill=tk.X)

        denetim = ttk.Frame(eylem)
        denetim.pack(fill=tk.X, pady=(6, 0))
        ttk.Button(denetim, text="Baskı Raporu", command=self.baski_raporunu_goster).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 3)
        )
        ttk.Button(denetim, text="1:1 Önizleme", command=self.gercek_boyut_onizleme).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=(3, 0)
        )

        self.kaydet_btn = ttk.Button(
            eylem,
            text="Oranı Koru ve Hazır PDF Üret",
            command=self.parcala_ve_pdf_yap,
            state=tk.DISABLED,
        )
        self.kaydet_btn.pack(fill=tk.X, pady=(12, 6))

        self.klasor_btn = ttk.Button(
            eylem, text="Çıktı Klasörünü Aç", command=self.cikti_klasorunu_ac, state=tk.DISABLED
        )
        self.klasor_btn.pack(fill=tk.X)

        # Ayarlar kaydırılabilir bir alanda durur; yazı tipi büyük ya da ekran kısa olsa
        # bile hiçbir ayar erişilemez hale gelmez.
        ayarlar = self._kaydirilabilir_alan(sol_panel)

        ttk.Label(
            ayarlar, text="--- NE YAPMAK İSTİYORSUNUZ? ---", font=(self.font_ailesi, 11, "bold")
        ).pack(pady=(5, 6), anchor=tk.W)
        for deger, metin in (
            ("poster", "Tek görseli A4'lere böl (poster)"),
            ("dizme", "Çok resmi tek A4'e diz"),
        ):
            ttk.Radiobutton(
                ayarlar,
                text=metin,
                value=deger,
                variable=self.mod,
                command=self.modu_uygula,
            ).pack(anchor=tk.W)

        # Dizme moduna ait ayarlar; mod değişince gösterilip gizlenir.
        self.dizme_cercevesi = ttk.Frame(ayarlar)
        self._dizme_arayuzu(self.dizme_cercevesi)

        self.poster_cercevesi = ttk.Frame(ayarlar)
        ayarlar = self.poster_cercevesi  # aşağıdaki poster ayarları bu çerçeveye girer
        self.poster_cercevesi.pack(fill=tk.X)

        ttk.Label(ayarlar, text="--- 1. DOSYA SEÇİMİ ---", font=(self.font_ailesi, 11, "bold")).pack(
            pady=5, anchor=tk.W
        )
        self.dosya_btn = ttk.Button(ayarlar, text="Bilgisayardan Dosya Seç (Resim / PDF)", command=self.resim_sec)
        self.dosya_btn.pack(fill=tk.X, pady=(5, 3))
        self.link_btn = ttk.Button(ayarlar, text="İnternetten Link ile Al", command=self.linkten_al)
        self.link_btn.pack(fill=tk.X, pady=(0, 5))
        self.dosya_lbl = ttk.Label(
            ayarlar, text="Henüz dosya seçilmedi...", wraplength=220, foreground="gray"
        )
        self.dosya_lbl.pack(anchor=tk.W, pady=2)

        ttk.Label(
            ayarlar, text="--- 2. A4 POSTER AYARLARI ---", font=(self.font_ailesi, 11, "bold")
        ).pack(pady=15, anchor=tk.W)

        ttk.Label(ayarlar, text="Sütun Sayısı (Yatay - X):").pack(anchor=tk.W)
        self.sutun_spin = ttk.Spinbox(
            ayarlar, from_=1, to=20, width=10, command=self.cozunurlugu_degerlendir
        )
        self.sutun_spin.set(4)
        self.sutun_spin.pack(pady=5, anchor=tk.W)

        ttk.Label(ayarlar, text="Satır Sayısı (Dikey - Y):").pack(anchor=tk.W)
        self.satir_spin = ttk.Spinbox(
            ayarlar, from_=1, to=20, width=10, command=self.cozunurlugu_degerlendir
        )
        self.satir_spin.set(2)
        self.satir_spin.pack(pady=5, anchor=tk.W)

        ttk.Label(ayarlar, text="Yazıcı Sayfa Yönü:").pack(anchor=tk.W)
        self.yon_combo = ttk.Combobox(
            ayarlar, values=["Yatay (Landscape)", "Dikey (Portrait)"], state="readonly"
        )
        self.yon_combo.set("Yatay (Landscape)")
        self.yon_combo.pack(fill=tk.X, pady=5)
        self.yon_combo.bind("<<ComboboxSelected>>", self.cozunurlugu_degerlendir)

        for kutu in (self.sutun_spin, self.satir_spin):
            kutu.bind("<KeyRelease>", self.cozunurlugu_degerlendir)

        ttk.Label(ayarlar, text="Yazıcı Kenar Boşluğu (mm):").pack(anchor=tk.W)
        self.kenar_spin = ttk.Spinbox(
            ayarlar, from_=0, to=20, increment=1, width=10,
            command=self.cozunurlugu_degerlendir,
        )
        self.kenar_spin.set(5)
        self.kenar_spin.pack(pady=5, anchor=tk.W)
        self.kenar_spin.bind("<KeyRelease>", self.cozunurlugu_degerlendir)
        ttk.Label(
            ayarlar,
            text="Yazıcınızın basamadığı kenar payı. Kenarlıksız basabiliyorsa 0 yapın.",
            wraplength=220,
            foreground="gray",
        ).pack(anchor=tk.W, pady=(0, 6))

        self.isaret_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            ayarlar, text="Kesim ve hizalama işaretleri ekle", variable=self.isaret_var
        ).pack(anchor=tk.W)
        self.harita_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            ayarlar, text="PDF'e montaj haritası sayfası ekle", variable=self.harita_var
        ).pack(anchor=tk.W, pady=(0, 6))

        ttk.Label(ayarlar, text="Çakışma Payı (Piksel Bindirme):").pack(anchor=tk.W)
        self.cakisma_spin = ttk.Spinbox(ayarlar, from_=0, to=100, width=10)
        self.cakisma_spin.set(15)
        self.cakisma_spin.pack(pady=5, anchor=tk.W)

        ttk.Label(
            ayarlar, text="--- 3. BASKI İYİLEŞTİRME ---", font=(self.font_ailesi, 11, "bold")
        ).pack(pady=15, anchor=tk.W)

        self.cozunurluk_lbl = ttk.Label(ayarlar, text="", wraplength=220, foreground="gray")
        self.cozunurluk_lbl.pack(anchor=tk.W, pady=(0, 8))

        ttk.Label(ayarlar, text="Hazır Ayar:").pack(anchor=tk.W)
        self.onayar_combo = ttk.Combobox(
            ayarlar, values=list(ONAYARLAR), state="readonly"
        )
        self.onayar_combo.set("Fotoğraf")
        self.onayar_combo.pack(fill=tk.X, pady=5)
        self.onayar_combo.bind("<<ComboboxSelected>>", self.onayari_uygula)

        self.otomatik_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            ayarlar,
            text="Otomatik düzelt (seviye + beyaz dengesi)",
            variable=self.otomatik_var,
            command=self.filtre_planla,
        ).pack(anchor=tk.W, pady=(6, 2))

        self.buyut_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            ayarlar,
            text="Düşük çözünürlükte akıllı büyüt",
            variable=self.buyut_var,
            command=self.cozunurlugu_degerlendir,
        ).pack(anchor=tk.W, pady=(0, 6))

        ttk.Button(
            ayarlar, text="AI ile Büyüt (eklenti gerekir)", command=self.ai_ile_buyut_istegi
        ).pack(fill=tk.X, pady=(4, 2))
        self.ai_durum_lbl = ttk.Label(ayarlar, text="", wraplength=220, foreground="gray")
        self.ai_durum_lbl.pack(anchor=tk.W, pady=(0, 8))
        self.ai_durumunu_yaz()

        ttk.Label(ayarlar, text="Kâğıt Türü (renk telafisi):").pack(anchor=tk.W)
        self.kagit_combo = ttk.Combobox(
            ayarlar, values=list(KAGIT_TELAFISI), state="readonly"
        )
        self.kagit_combo.set("Belirtme")
        self.kagit_combo.pack(fill=tk.X, pady=5)
        self.kagit_combo.bind("<<ComboboxSelected>>", self.filtre_planla)

        ttk.Label(ayarlar, text="Gürültü Azaltma:").pack(anchor=tk.W)
        self.gurultu_combo = ttk.Combobox(
            ayarlar, values=["Kapalı", "Hafif", "Orta", "Güçlü"], state="readonly"
        )
        self.gurultu_combo.set("Kapalı")
        self.gurultu_combo.pack(fill=tk.X, pady=5)
        self.gurultu_combo.bind("<<ComboboxSelected>>", self.filtre_planla)

        ttk.Label(
            ayarlar, text="Keskinleştirme (unsharp mask):", font=(self.font_ailesi, 10, "bold")
        ).pack(anchor=tk.W, pady=(10, 2))
        self.yaricap_slider = self._surgu_ekle(ayarlar, "Yarıçap (piksel):", 0.0, 5.0, 1.2)
        self.miktar_slider = self._surgu_ekle(ayarlar, "Miktar (%):", 0.0, 300.0, 110.0)
        self.esik_slider = self._surgu_ekle(ayarlar, "Eşik (gürültüyü koru):", 0.0, 20.0, 3.0)

        ttk.Label(ayarlar, text="Renk ve ton:", font=(self.font_ailesi, 10, "bold")).pack(
            anchor=tk.W, pady=(10, 2)
        )
        self.kontrast_slider = self._surgu_ekle(ayarlar, "Kontrast:", 0.5, 2.5, 1.0)
        self.renk_slider = self._surgu_ekle(ayarlar, "Renk Canlılığı:", 0.5, 2.5, 1.0)
        self.parlaklik_slider = self._surgu_ekle(ayarlar, "Parlaklık:", 0.5, 2.0, 1.0)

        ttk.Button(ayarlar, text="Ayarları Sıfırla", command=self.ayarlari_sifirla).pack(
            fill=tk.X, pady=(8, 4)
        )

        self.sag_panel = ttk.Frame(self.root, padding="10", relief="groove")
        self.sag_panel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.onizleme_label = ttk.Label(
            self.sag_panel, text="Lütfen başlamak için bir resim ya da PDF seçin...", font=(self.font_ailesi, 12)
        )
        self.onizleme_label.pack(expand=True)

        self.durum_lbl = ttk.Label(self.sag_panel, text="", foreground="gray")
        self.durum_lbl.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Label(
            self.sag_panel, text="powered by Omer OZTURK", foreground="gray", anchor=tk.E
        ).pack(side=tk.BOTTOM, fill=tk.X)

    def _kaydirilabilir_alan(self, ust: ttk.Frame) -> ttk.Frame:
        """Dikey kaydırılabilir bir çerçeve döndürür; kaydırma çubuğu ancak gerekirse çıkar."""
        kutu = ttk.Frame(ust)
        kutu.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        tuval = tk.Canvas(kutu, highlightthickness=0, borderwidth=0)
        cubuk = ttk.Scrollbar(kutu, orient=tk.VERTICAL, command=tuval.yview)
        tuval.configure(yscrollcommand=cubuk.set)
        tuval.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        icerik = ttk.Frame(tuval)
        pencere = tuval.create_window((0, 0), window=icerik, anchor="nw")

        def cubugu_ayarla():
            # Yükseklikler ancak yerleşim oturduktan sonra doğru okunur; bu yüzden
            # karar boşta (after_idle) verilir, yoksa çubuk gereksizken de görünür.
            gerekli = icerik.winfo_reqheight() > tuval.winfo_height()
            if gerekli and not cubuk.winfo_ismapped():
                cubuk.pack(side=tk.RIGHT, fill=tk.Y)
            elif not gerekli and cubuk.winfo_ismapped():
                cubuk.pack_forget()

        def icerik_degisti(_olay=None):
            tuval.configure(scrollregion=tuval.bbox("all"))
            # Panel genişliği içeriğe göre belirlenir; metinler kırpılmasın.
            tuval.configure(width=icerik.winfo_reqwidth())
            tuval.after_idle(cubugu_ayarla)

        def tuval_degisti(olay):
            tuval.itemconfigure(pencere, width=olay.width)  # iç çerçeve genişliği takip etsin
            icerik_degisti()

        icerik.bind("<Configure>", icerik_degisti)
        tuval.bind("<Configure>", tuval_degisti)

        def kaydir(olay):
            if icerik.winfo_reqheight() <= tuval.winfo_height():
                return
            # Windows/macOS <MouseWheel> delta gönderir, X11 Button-4/5 üretir.
            adim = -1 if getattr(olay, "num", None) == 4 or getattr(olay, "delta", 0) > 0 else 1
            tuval.yview_scroll(adim, "units")

        tekerlek = ("<MouseWheel>", "<Button-4>", "<Button-5>")

        def tekerlegi_bagla(_olay=None):  # panelin üzerindeyken alt widget'lar da kaydırsın
            for dizi in tekerlek:
                tuval.bind_all(dizi, kaydir)

        def tekerlegi_birak(_olay=None):
            for dizi in tekerlek:
                tuval.unbind_all(dizi)

        kutu.bind("<Enter>", tekerlegi_bagla)
        kutu.bind("<Leave>", tekerlegi_birak)

        return icerik

    def _dizme_arayuzu(self, ust: ttk.Frame):
        """'Çok resmi tek A4'e diz' modunun ayarları."""
        ttk.Label(
            ust, text="--- 1. RESİMLERİ SEÇİN ---", font=(self.font_ailesi, 11, "bold")
        ).pack(pady=5, anchor=tk.W)
        ttk.Button(ust, text="Resimleri Seç (çoklu)", command=self.dizme_resimleri_sec).pack(
            fill=tk.X, pady=(5, 3)
        )
        ttk.Button(ust, text="Klasördeki Tüm Resimler", command=self.dizme_klasor_sec).pack(
            fill=tk.X, pady=(0, 3)
        )
        ttk.Button(ust, text="Listeyi Temizle", command=self.dizme_temizle).pack(
            fill=tk.X, pady=(0, 5)
        )
        self.dizme_lbl = ttk.Label(
            ust, text="Henüz resim seçilmedi...", wraplength=220, foreground="gray"
        )
        self.dizme_lbl.pack(anchor=tk.W, pady=2)

        ttk.Label(
            ust, text="--- 2. SAYFA DÜZENİ ---", font=(self.font_ailesi, 11, "bold")
        ).pack(pady=15, anchor=tk.W)

        ttk.Label(ust, text="Sütun Sayısı (yan yana):").pack(anchor=tk.W)
        self.dizme_sutun = ttk.Spinbox(ust, from_=1, to=10, width=10, command=self.dizme_onizle)
        self.dizme_sutun.set(3)
        self.dizme_sutun.pack(pady=5, anchor=tk.W)

        ttk.Label(ust, text="Satır Sayısı (alt alta):").pack(anchor=tk.W)
        self.dizme_satir = ttk.Spinbox(ust, from_=1, to=10, width=10, command=self.dizme_onizle)
        self.dizme_satir.set(4)
        self.dizme_satir.pack(pady=5, anchor=tk.W)

        ttk.Label(ust, text="Sayfa Yönü:").pack(anchor=tk.W)
        self.dizme_yon = ttk.Combobox(
            ust, values=["Dikey (Portrait)", "Yatay (Landscape)"], state="readonly"
        )
        self.dizme_yon.set("Dikey (Portrait)")
        self.dizme_yon.pack(fill=tk.X, pady=5)
        self.dizme_yon.bind("<<ComboboxSelected>>", lambda _o: self.dizme_onizle())

        ttk.Label(ust, text="Kenar Boşluğu (mm):").pack(anchor=tk.W)
        self.dizme_kenar = ttk.Spinbox(ust, from_=0, to=40, width=10, command=self.dizme_onizle)
        self.dizme_kenar.set(10)
        self.dizme_kenar.pack(pady=5, anchor=tk.W)

        ttk.Label(ust, text="Resimler Arası Boşluk (mm):").pack(anchor=tk.W)
        self.dizme_aralik = ttk.Spinbox(ust, from_=0, to=30, width=10, command=self.dizme_onizle)
        self.dizme_aralik.set(4)
        self.dizme_aralik.pack(pady=5, anchor=tk.W)

        self.dizme_bilgi = ttk.Label(ust, text="", wraplength=220, foreground="gray")
        self.dizme_bilgi.pack(anchor=tk.W, pady=(10, 4))

    def modu_uygula(self):
        """Seçilen moda göre ayar panelini ve üretim düğmesini değiştirir."""
        dizme = self.mod.get() == "dizme"
        if dizme:
            self.poster_cercevesi.pack_forget()
            self.dizme_cercevesi.pack(fill=tk.X)
            self.kaydet_btn.config(text="Resimleri A4 Sayfalara Diz")
            self.kaydet_btn.config(state=tk.NORMAL if self.dizme_dosyalari else tk.DISABLED)
            self.onizleme_label.config(
                text="Resimleri seçin; ilk sayfanın önizlemesi burada görünecek..."
                if not self.dizme_dosyalari
                else ""
            )
            self.dizme_onizle()
        else:
            self.dizme_cercevesi.pack_forget()
            self.poster_cercevesi.pack(fill=tk.X)
            self.kaydet_btn.config(text="Oranı Koru ve Hazır PDF Üret")
            self.kaydet_btn.config(state=tk.NORMAL if self.orijinal_img else tk.DISABLED)
            if self.orijinal_img is None:
                self.onizleme_label.config(
                    image="", text="Lütfen başlamak için bir resim ya da PDF seçin..."
                )
            else:
                self.onizlemeyi_guncelle()

    def _surgu_ekle(
        self,
        ust: ttk.Frame,
        etiket: str,
        alt_sinir: float,
        ust_sinir: float,
        baslangic: float = 1.0,
    ):
        satir = ttk.Frame(ust)
        satir.pack(fill=tk.X)
        ttk.Label(satir, text=etiket).pack(side=tk.LEFT, anchor=tk.W)
        deger_lbl = ttk.Label(satir, text="", foreground="gray", width=6, anchor=tk.E)
        deger_lbl.pack(side=tk.RIGHT)

        def degisti(_deger=None):
            deger_lbl.config(text=f"{surgu.get():.1f}")
            self.filtre_planla()

        surgu = ttk.Scale(ust, from_=alt_sinir, to=ust_sinir, orient=tk.HORIZONTAL, command=degisti)
        surgu.set(baslangic)
        surgu.pack(fill=tk.X, pady=(0, 6))
        deger_lbl.config(text=f"{baslangic:.1f}")
        return surgu

    # ------------------------------------------------------------------ eylemler
    def resim_sec(self):
        def kalip(uzantilar) -> str:
            return " ".join(f"*{u}" for u in uzantilar)

        dosya_tipleri = [
            ("Desteklenen tüm dosyalar", kalip(TUM_UZANTILAR)),
            ("Resim dosyaları", kalip(PILLOW_UZANTILARI)),
            ("PDF ve Illustrator", kalip(PDF_UZANTILARI)),
            ("iPhone fotoğrafları (HEIC)", kalip(HEIC_UZANTILARI)),
            ("Ham fotoğraf (RAW)", kalip(RAW_UZANTILARI)),
            ("Tüm Dosyalar", "*.*"),
        ]
        secilen_yol = filedialog.askopenfilename(
            title="Bir Resim, PDF ya da Tasarım Dosyası Seçin", filetypes=dosya_tipleri
        )
        if not secilen_yol:
            return
        self.resmi_yukle(secilen_yol)

    def linkten_al(self):
        """Kullanıcıdan bir resim adresi alıp indirir; indirme arayüzü kilitlemez."""
        baglanti = self._link_penceresi()
        if not baglanti:
            return

        import queue
        import tempfile
        import threading

        if self._indirme_dizini is None:
            self._indirme_dizini = tempfile.mkdtemp(prefix="poster_basim_")

        self.dosya_btn.config(state=tk.DISABLED)
        self.link_btn.config(state=tk.DISABLED)
        self.durum_lbl.config(text="Resim indiriliyor...")

        # Tkinter iş parçacığı güvenli değildir: indirme iş parçacığı arayüze doğrudan
        # dokunamaz, sonucu kuyruğa bırakır; arayüzü yalnızca ana iş parçacığı günceller.
        kuyruk: queue.Queue[tuple[str, str]] = queue.Queue()

        def indir():
            try:
                kuyruk.put(("tamam", linkten_resim_indir(baglanti, self._indirme_dizini)))
            except ValueError as hata:
                kuyruk.put(("hata", str(hata)))
            except Exception as hata:  # beklenmedik durumda da kullanıcı bilgilendirilsin
                kuyruk.put(("hata", f"İndirme sırasında beklenmedik bir sorun çıktı:\n{hata}"))

        def yokla():
            try:
                durum, deger = kuyruk.get_nowait()
            except queue.Empty:
                self.root.after(120, yokla)
                return
            self.dosya_btn.config(state=tk.NORMAL)
            self.link_btn.config(state=tk.NORMAL)
            if durum == "hata":
                self.durum_lbl.config(text="İndirme başarısız.")
                messagebox.showerror("Link ile alma", deger)
                return
            self.resmi_yukle(deger)

        threading.Thread(target=indir, daemon=True).start()
        self.root.after(120, yokla)

    # -------------------------------------------------------- çok resmi tek sayfaya dizme
    def dizme_resimleri_sec(self):
        yollar = filedialog.askopenfilenames(
            title="Dizilecek Resimleri Seçin (birden çok seçebilirsiniz)",
            filetypes=[
                ("Resim dosyaları", " ".join(f"*{u}" for u in PILLOW_UZANTILARI + HEIC_UZANTILARI)),
                ("Tüm Dosyalar", "*.*"),
            ],
        )
        if yollar:
            self._dizme_dosyalari_ekle(list(yollar))

    def dizme_klasor_sec(self):
        klasor = filedialog.askdirectory(title="Resimlerin Bulunduğu Klasörü Seçin")
        if not klasor:
            return
        kabul = PILLOW_UZANTILARI + HEIC_UZANTILARI + RAW_UZANTILARI
        bulunan = [
            os.path.join(klasor, ad)
            for ad in os.listdir(klasor)
            if os.path.splitext(ad)[1].lower() in kabul
        ]
        if not bulunan:
            messagebox.showinfo("Klasör", "Bu klasörde desteklenen resim bulunamadı.")
            return
        self._dizme_dosyalari_ekle(bulunan)

    def _dizme_dosyalari_ekle(self, yollar: list[str]):
        # Dosya adındaki sayılar sayısal karşılaştırılır: resim2, resim10'dan önce gelir.
        self.dizme_dosyalari = sorted(set(yollar), key=lambda y: dogal_anahtar(os.path.basename(y)))
        self.dizme_lbl.config(
            text=f"{len(self.dizme_dosyalari)} resim seçildi "
            f"({os.path.basename(self.dizme_dosyalari[0])} ...)",
            foreground="black",
        )
        self.kaydet_btn.config(state=tk.NORMAL)
        self.dizme_onizle()

    def dizme_temizle(self):
        self.dizme_dosyalari = []
        self.dizme_lbl.config(text="Henüz resim seçilmedi...", foreground="gray")
        self.dizme_bilgi.config(text="")
        self.kaydet_btn.config(state=tk.DISABLED)
        self.onizleme_label.config(
            image="", text="Resimleri seçin; ilk sayfanın önizlemesi burada görünecek..."
        )

    def _dizme_ayarlari(self) -> tuple[int, int, bool, float, float]:
        sutun = max(1, min(int(self.dizme_sutun.get() or 1), 10))
        satir = max(1, min(int(self.dizme_satir.get() or 1), 10))
        dikey = "Dikey" in self.dizme_yon.get()
        kenar = max(0.0, min(float(self.dizme_kenar.get() or 0), 40))
        aralik = max(0.0, min(float(self.dizme_aralik.get() or 0), 30))
        return sutun, satir, dikey, kenar, aralik

    def dizme_onizle(self, *_):
        """İlk sayfanın nasıl görüneceğini düşük çözünürlükte gösterir."""
        if self.mod.get() != "dizme" or not self.dizme_dosyalari:
            return
        try:
            sutun, satir, dikey, kenar, aralik = self._dizme_ayarlari()
        except ValueError:
            return

        sayfa_basina = sutun * satir
        toplam_sayfa = (len(self.dizme_dosyalari) + sayfa_basina - 1) // sayfa_basina
        self.dizme_bilgi.config(
            text=f"Sayfa başına {sayfa_basina} resim → toplam {toplam_sayfa} A4 sayfa "
            f"({len(self.dizme_dosyalari)} resim)"
        )

        try:  # önizleme düşük çözünürlükte üretilir, hızlı olsun
            goruntuler = [
                kaynak_goruntusu_ac(y) for y in self.dizme_dosyalari[:sayfa_basina]
            ]
            sayfa = resimleri_sayfaya_diz(goruntuler, sutun, satir, dikey, kenar, aralik, dpi=72)
        except (ValueError, MemoryError, OSError) as hata:
            self.onizleme_label.config(image="", text=f"Önizleme alınamadı:\n{hata}")
            return
        sayfa.thumbnail(ONIZLEME_GOSTERIM_BOYUTU, Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(sayfa)
        self.onizleme_label.config(image=self.tk_img, text="")

    def dizme_uret(self):
        """Seçilen resimleri A4 sayfalara dizip PDF ve JPEG olarak kaydeder."""
        try:
            sutun, satir, dikey, kenar, aralik = self._dizme_ayarlari()
        except ValueError:
            messagebox.showerror("Hata", "Sayfa düzeni değerleri sayı olmalı.")
            return

        sayfa_basina = sutun * satir
        toplam_sayfa = (len(self.dizme_dosyalari) + sayfa_basina - 1) // sayfa_basina
        zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
        cikis_klasoru = cikis_klasoru_hazirla(f"Dizilmis_Sayfalar_{zaman_damgasi}")
        pdf_yolu = os.path.join(cikis_klasoru, f"Dizilmis_Sayfalar_{zaman_damgasi}.pdf")

        sayfa_boyutu = A4 if dikey else landscape(A4)
        pdf_canvas = canvas.Canvas(pdf_yolu, pagesize=sayfa_boyutu)
        sayfa_w, sayfa_h = sayfa_boyutu

        for sayfa_no in range(toplam_sayfa):
            self.durum_lbl.config(text=f"Sayfa hazırlanıyor: {sayfa_no + 1} / {toplam_sayfa}")
            self.root.update_idletasks()

            dilim = self.dizme_dosyalari[sayfa_no * sayfa_basina : (sayfa_no + 1) * sayfa_basina]
            goruntuler = []
            for yol in dilim:
                try:
                    goruntuler.append(kaynak_goruntusu_ac(yol))
                except (ValueError, MemoryError) as hata:  # tek bozuk dosya işi durdurmasın
                    print(f"[atlandı] {os.path.basename(yol)}: {hata}", flush=True)
            if not goruntuler:
                continue

            sayfa = resimleri_sayfaya_diz(goruntuler, sutun, satir, dikey, kenar, aralik)
            jpeg_yolu = os.path.join(cikis_klasoru, f"sayfa_{sayfa_no + 1:02d}.jpg")
            sayfa.save(jpeg_yolu, "JPEG", quality=95, subsampling=0, dpi=(PDF_DPI, PDF_DPI))
            pdf_canvas.drawImage(jpeg_yolu, 0, 0, width=sayfa_w, height=sayfa_h)
            pdf_canvas.showPage()

        pdf_canvas.save()
        self.son_cikis_klasoru = cikis_klasoru
        self.klasor_btn.config(state=tk.NORMAL)
        nerede = os.path.basename(os.path.dirname(os.path.dirname(cikis_klasoru)))
        self.durum_lbl.config(
            text=f"Tamamlandı: {toplam_sayfa} sayfa → {os.path.basename(pdf_yolu)} ({nerede})"
        )
        messagebox.showinfo(
            "Hazır",
            f"{len(self.dizme_dosyalari)} resim {toplam_sayfa} A4 sayfaya dizildi.\n\n"
            f"Klasör:\n{cikis_klasoru}\n\n"
            "Yazdırırken ölçeklendirmeyi '%100 / Gerçek Boyut' seçin.",
        )

    def _pdf_yukle(self, yol: str) -> Image.Image | None:
        """PDF'i (gerekirse sayfa sordurarak) baskı çözünürlüğünde görüntüye çevirir."""
        try:
            toplam = pdf_sayfa_sayisi(yol)
        except ImportError as hata:
            messagebox.showerror("PDF desteği", str(hata))
            return None
        except ValueError as hata:
            messagebox.showerror("Hata", str(hata))
            return None

        sayfa_no = 1
        if toplam > 1:
            sayfa_no = self._sayfa_penceresi(yol, toplam)
            if sayfa_no is None:
                return None

        onceki = self.durum_lbl["text"]
        self.durum_lbl.config(text=f"PDF taranıyor ({PDF_DPI} DPI)...")
        self.root.update_idletasks()
        try:
            return pdf_sayfasini_goruntuye_cevir(yol, sayfa_no)
        except (ValueError, ImportError, MemoryError) as hata:
            self.durum_lbl.config(text=onceki)
            messagebox.showerror("Hata", str(hata))
            return None

    def _sayfa_penceresi(self, yol: str, toplam: int) -> int | None:
        """Çok sayfalı PDF'te hangi sayfanın poster olacağını, önizleme göstererek sorar."""
        pencere = tk.Toplevel(self.root)
        pencere.title("PDF sayfası seçin")
        pencere.transient(self.root)
        pencere.resizable(False, False)
        cerceve = ttk.Frame(pencere, padding=15)
        cerceve.pack(fill=tk.BOTH, expand=True)

        ttk.Label(cerceve, text=f"Bu PDF {toplam} sayfadan oluşuyor.").pack(anchor=tk.W)
        ttk.Label(
            cerceve,
            text="Sayfalar arasında gezinip postere dönüştüreceğinizi seçin:",
            foreground="gray",
        ).pack(anchor=tk.W, pady=(2, 8))

        # Sabit ölçülü kutu: sayfalar arasında gezinirken pencere boyutu oynamasın.
        kutu = ttk.Frame(cerceve, width=320, height=320)
        kutu.pack_propagate(False)
        kutu.pack(pady=(0, 10))
        onizleme = ttk.Label(kutu, relief="groove", anchor=tk.CENTER)
        onizleme.pack(fill=tk.BOTH, expand=True)
        onbellek: dict[int, ImageTk.PhotoImage] = {}

        gezinme = ttk.Frame(cerceve)
        gezinme.pack(anchor=tk.W)
        geri_btn = ttk.Button(gezinme, text="◀", width=3)
        geri_btn.pack(side=tk.LEFT)
        secim = ttk.Spinbox(gezinme, from_=1, to=toplam, width=6, justify=tk.CENTER)
        secim.set(1)
        secim.pack(side=tk.LEFT, padx=6)
        ileri_btn = ttk.Button(gezinme, text="▶", width=3)
        ileri_btn.pack(side=tk.LEFT)
        ttk.Label(gezinme, text=f"/ {toplam}", foreground="gray").pack(side=tk.LEFT, padx=(6, 0))

        def gecerli_sayfa() -> int:
            try:
                return min(max(int(secim.get()), 1), toplam)
            except ValueError:
                return 1

        def onizlemeyi_goster(*_):
            no = gecerli_sayfa()
            if no not in onbellek:
                onizleme.config(text="yükleniyor...", image="")
                pencere.update_idletasks()
                try:  # önizleme için düşük çözünürlük yeter, hızlı olsun
                    kucuk = pdf_sayfasini_goruntuye_cevir(yol, no, dpi=40)
                except (ValueError, ImportError):
                    onizleme.config(text="(önizleme alınamadı)", image="")
                    return
                kucuk.thumbnail((300, 300), Image.Resampling.LANCZOS)
                onbellek[no] = ImageTk.PhotoImage(kucuk)
            onizleme.config(image=onbellek[no], text="")

        def kaydir(adim: int):
            secim.set(min(max(gecerli_sayfa() + adim, 1), toplam))
            onizlemeyi_goster()

        geri_btn.config(command=lambda: kaydir(-1))
        ileri_btn.config(command=lambda: kaydir(1))
        secim.config(command=onizlemeyi_goster)
        secim.bind("<KeyRelease>", onizlemeyi_goster)
        pencere.bind("<Left>", lambda _o: kaydir(-1))
        pencere.bind("<Right>", lambda _o: kaydir(1))

        sonuc: dict[str, int | None] = {"sayfa": None}

        def onayla(_olay=None):
            sonuc["sayfa"] = gecerli_sayfa()
            pencere.destroy()

        dugmeler = ttk.Frame(cerceve)
        dugmeler.pack(fill=tk.X, pady=(12, 0))
        ttk.Button(dugmeler, text="İptal", command=pencere.destroy).pack(side=tk.RIGHT)
        ttk.Button(dugmeler, text="Bu Sayfayı Kullan", command=onayla).pack(
            side=tk.RIGHT, padx=(0, 8)
        )

        pencere.bind("<Return>", onayla)
        pencere.bind("<Escape>", lambda _o: pencere.destroy())
        onizlemeyi_goster()
        pencere.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - pencere.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - pencere.winfo_height()) // 3
        pencere.geometry(f"+{max(0, x)}+{max(0, y)}")
        pencere.grab_set()
        self.root.wait_window(pencere)
        return sonuc["sayfa"]

    def _link_penceresi(self) -> str | None:
        """Adres soran küçük pencere. Tk'nin hazır giriş penceresi İngilizce olduğu için
        kendi penceremizi kuruyoruz."""
        pencere = tk.Toplevel(self.root)
        pencere.title("İnternetten Link ile Al")
        pencere.transient(self.root)
        pencere.resizable(False, False)
        cerceve = ttk.Frame(pencere, padding=15)
        cerceve.pack(fill=tk.BOTH, expand=True)

        ttk.Label(cerceve, text="Resmin ya da PDF'in web adresini yapıştırın:").pack(anchor=tk.W)
        ttk.Label(
            cerceve,
            text="Tarayıcıda görsele sağ tıklayıp “Resim adresini kopyala” diyebilirsiniz. "
                 "PDF afişlerde adres çubuğundaki .pdf ile biten adresi kullanın.",
            foreground="gray",
            wraplength=430,
        ).pack(anchor=tk.W, pady=(2, 8))

        giris = ttk.Entry(cerceve, width=64)
        giris.pack(fill=tk.X)
        try:  # panoda adres varsa hazır gelsin
            pano = self.root.clipboard_get()
            if pano.strip().startswith(("http://", "https://")):
                giris.insert(0, pano.strip())
                giris.select_range(0, tk.END)
        except tk.TclError:
            pass
        giris.focus_set()

        sonuc: dict[str, str | None] = {"adres": None}

        def onayla(_olay=None):
            sonuc["adres"] = giris.get().strip()
            pencere.destroy()

        dugmeler = ttk.Frame(cerceve)
        dugmeler.pack(fill=tk.X, pady=(12, 0))
        ttk.Button(dugmeler, text="İptal", command=pencere.destroy).pack(side=tk.RIGHT)
        ttk.Button(dugmeler, text="Resmi Al", command=onayla).pack(side=tk.RIGHT, padx=(0, 8))

        pencere.bind("<Return>", onayla)
        pencere.bind("<Escape>", lambda _o: pencere.destroy())
        pencere.update_idletasks()
        # Ana pencerenin ortasına yerleştir.
        x = self.root.winfo_rootx() + (self.root.winfo_width() - pencere.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - pencere.winfo_height()) // 3
        pencere.geometry(f"+{max(0, x)}+{max(0, y)}")
        pencere.grab_set()
        self.root.wait_window(pencere)
        return sonuc["adres"] or None

    def resmi_yukle(self, secilen_yol: str):
        uzanti = os.path.splitext(secilen_yol)[1].lower()
        if uzanti in PDF_UZANTILARI:
            img = self._pdf_yukle(secilen_yol)
            if img is None:
                return
        else:
            onceki = self.durum_lbl["text"]
            if uzanti in RAW_UZANTILARI:  # ham dosyanın işlenmesi birkaç saniye sürer
                self.durum_lbl.config(text="Ham (RAW) dosya işleniyor...")
                self.root.update_idletasks()
            try:
                img = kaynak_goruntusu_ac(secilen_yol)
            except (ValueError, MemoryError) as hata:
                self.durum_lbl.config(text=onceki)
                messagebox.showerror("Hata", str(hata))
                return

        img, profil_adi = srgb_yap(img)
        self.kaynak_profili = profil_adi
        self.resim_yolu = secilen_yol
        self.orijinal_img = img
        self.onizleme_kaynak = img.copy()
        self.onizleme_kaynak.thumbnail(ONIZLEME_CALISMA_BOYUTU, Image.Resampling.LANCZOS)

        self.dosya_lbl.config(text=os.path.basename(secilen_yol), foreground="black")
        self.durum_lbl.config(text=f"Kaynak çözünürlük: {img.width} x {img.height} piksel")
        self.ayarlari_sifirla()
        self.cozunurlugu_degerlendir()
        self.kaydet_btn.config(state=tk.NORMAL)

    def ayarlari_sifirla(self):
        for surgu in (self.kontrast_slider, self.renk_slider, self.parlaklik_slider):
            surgu.set(1.0)
        self.onayar_combo.set("Fotoğraf")
        self.onayari_uygula()

    def filtre_planla(self, _event=None):
        """Sürgü hareketini geciktirerek uygular (her pikselde yeniden işlemeyi önler)."""
        if self.onizleme_kaynak is None:
            return
        if self._filtre_isi is not None:
            self.root.after_cancel(self._filtre_isi)
        self._filtre_isi = self.root.after(60, self.onizlemeyi_guncelle)

    # ------------------------------------------------------------------ AI büyütme
    def ai_durumunu_yaz(self):
        motor, model = ai_eklentisi_hazir_mi()
        if motor and model:
            self.ai_durum_lbl.config(
                text="AI eklentisi hazır — düşük çözünürlüklü görsellerde kullanabilirsiniz.",
                foreground="#15803d",
            )
        else:
            self.ai_durum_lbl.config(
                text="AI eklentisi kurulu değil; AI büyütme yapılamaz. "
                "Klasik akıllı büyütme çalışmaya devam ediyor.",
                foreground="gray",
            )

    def ai_ile_buyut_istegi(self):
        if self.orijinal_img is None:
            messagebox.showinfo("AI ile Büyüt", "Önce bir görsel açın.")
            return

        motor, model = ai_eklentisi_hazir_mi()
        if not (motor and model):
            if not self._ai_eklentisini_sor():
                return
            if not all(ai_eklentisi_hazir_mi()):
                return

        # Süre donanıma göre 20 kata kadar değişiyor; bu bilgisayarda ölçüp soruyoruz.
        self.durum_lbl.config(text="Bilgisayarınızın hızı ölçülüyor...")
        self.root.update_idletasks()
        try:
            karo_suresi = ai_karo_suresi()
        except Exception as hata:  # onnxruntime kendi hata tiplerini kullanır
            messagebox.showerror("AI ile Büyüt", f"Hesaplama motoru çalıştırılamadı:\n{hata}")
            self.durum_lbl.config(text="")
            return

        toplam_karo = ai_karo_sayisi(self.orijinal_img)
        tahmin_sn = karo_suresi * toplam_karo
        dakika = tahmin_sn / 60
        sure_metni = f"{tahmin_sn:.0f} saniye" if tahmin_sn < 90 else f"{dakika:.0f} dakika"
        self.durum_lbl.config(text="")

        if not messagebox.askyesno(
            "AI ile Büyüt",
            f"Görsel: {self.orijinal_img.width} × {self.orijinal_img.height} piksel\n"
            f"Sonuç: {self.orijinal_img.width * 2} × {self.orijinal_img.height * 2} piksel "
            "(2 kat)\n\n"
            f"Bu bilgisayarda ölçülen tahmini süre: {sure_metni}\n"
            f"({toplam_karo} parça hâlinde işlenecek; istediğiniz an durdurabilirsiniz.)\n\n"
            "İşlem sırasında program bekleyecek. Devam edilsin mi?",
        ):
            return

        self._ai_buyutmeyi_calistir(toplam_karo)

    def _ai_eklentisini_sor(self) -> bool:
        """Eklentinin ne olduğunu, niçin ayrı olduğunu anlatır ve indirme izni ister."""
        onay = messagebox.askyesno(
            "AI ile Büyütme — bilmeniz gerekenler",
            "BU NEDİR?\n"
            "Yapay zekâ ile büyütme, küçük bir görseli büyütürken kaybolan detayı tahmin\n"
            "ederek yeniden üretir. Klasik büyütme yalnızca pikselleri yumuşatır.\n\n"
            "NEDEN AYRI EKLENTİ?\n"
            f"Bu iş için hesaplama motoru (~{AI_MOTOR_MB} MB) ve model dosyası "
            f"(~{AI_MODEL_MB} MB) gerekir.\n"
            "Programın içine konsaydı, bu özelliği hiç kullanmayacak herkes de indirmek\n"
            "zorunda kalırdı. EKLENTİ KURULMADAN AI BÜYÜTME YAPILAMAZ.\n\n"
            "NE ZAMAN İŞE YARAR?\n"
            "Görseliniz seçtiğiniz poster boyu için küçükse (kırmızı uyarı) gözle görülür\n"
            "fark yaratır. Zaten yeterli çözünürlükteki görsellerde gereksizdir.\n\n"
            "NEYE DİKKAT?\n"
            "AI, var olmayan detayı uydurur: küçük yazılar, yüz hatları ve logolar\n"
            "olduğundan farklı çıkabilir. Belge ve metin ağırlıklı işlerde klasik büyütme\n"
            "daha güvenlidir.\n\n"
            f"İNDİRİLECEK: toplam ~{AI_MOTOR_MB + AI_MODEL_MB} MB, yalnızca bir kez.\n"
            "KAYNAK: huggingface.co/Xenova/swin2SR-classical-sr-x2-64 (Apache-2.0, açık kaynak)\n\n"
            "İndirmezseniz program aynen çalışır; klasik akıllı büyütme devrede kalır.\n\n"
            "Eklenti şimdi indirilsin mi?",
        )
        if not onay:
            return False

        import queue
        import threading

        kuyruk: queue.Queue = queue.Queue()
        pencere, etiket = self._islem_penceresi("AI eklentisi kuruluyor", iptal_komutu=None)

        def kur():
            try:
                ai_eklentisini_kur(lambda m: kuyruk.put(("bilgi", m)))
                kuyruk.put(("bitti", ""))
            except ValueError as hata:
                kuyruk.put(("hata", str(hata)))

        threading.Thread(target=kur, daemon=True).start()
        sonuc = {"durum": None}

        def yokla():
            try:
                durum, deger = kuyruk.get_nowait()
            except queue.Empty:
                pencere.after(150, yokla)
                return
            if durum == "bilgi":
                etiket.config(text=deger)
                pencere.after(150, yokla)
                return
            sonuc["durum"] = durum
            sonuc["mesaj"] = deger
            pencere.destroy()

        pencere.after(150, yokla)
        self.root.wait_window(pencere)
        self.ai_durumunu_yaz()

        if sonuc["durum"] == "hata":
            messagebox.showerror("AI eklentisi", sonuc["mesaj"])
            return False
        return sonuc["durum"] == "bitti"

    def _islem_penceresi(self, baslik: str, iptal_komutu):
        """Ortada duran küçük ilerleme penceresi döndürür (pencere, etiket)."""
        pencere = tk.Toplevel(self.root)
        pencere.title(baslik)
        pencere.transient(self.root)
        pencere.resizable(False, False)
        pencere.protocol("WM_DELETE_WINDOW", lambda: None)  # yanlışlıkla kapatılmasın
        cerceve = ttk.Frame(pencere, padding=20)
        cerceve.pack(fill=tk.BOTH, expand=True)
        etiket = ttk.Label(cerceve, text="Hazırlanıyor...", width=48)
        etiket.pack(anchor=tk.W)
        if iptal_komutu is not None:
            ttk.Button(cerceve, text="Durdur", command=iptal_komutu).pack(pady=(12, 0))
        pencere.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - pencere.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - pencere.winfo_height()) // 3
        pencere.geometry(f"+{max(0, x)}+{max(0, y)}")
        pencere.grab_set()
        return pencere, etiket

    def _ai_buyutmeyi_calistir(self, toplam_karo: int):
        import queue
        import threading
        import time

        kuyruk: queue.Queue = queue.Queue()
        durduruldu = {"evet": False}
        pencere, etiket = self._islem_penceresi(
            "AI ile büyütülüyor", lambda: durduruldu.__setitem__("evet", True)
        )

        def calis():
            try:
                sonuc = ai_ile_buyut(
                    self.orijinal_img,
                    ilerleme=lambda y, t: kuyruk.put(("ilerleme", (y, t))),
                    iptal=lambda: durduruldu["evet"],
                )
                kuyruk.put(("iptal" if sonuc is None else "bitti", sonuc))
            except Exception as hata:
                kuyruk.put(("hata", str(hata)))

        baslangic = time.time()
        threading.Thread(target=calis, daemon=True).start()

        def yokla():
            try:
                durum, deger = kuyruk.get_nowait()
            except queue.Empty:
                pencere.after(120, yokla)
                return
            if durum == "ilerleme":
                yapilan, toplam = deger
                # Kalan süre gerçek hıza göre güncellenir; baştaki tahmin şaşarsa kendini düzeltir.
                gecen = time.time() - baslangic
                kalan = (gecen / yapilan) * (toplam - yapilan) if yapilan else 0
                kalan_metni = (
                    f"{kalan:.0f} saniye" if kalan < 90 else f"{kalan / 60:.0f} dakika"
                )
                etiket.config(
                    text=f"İşleniyor: {yapilan} / {toplam} parça  (%{yapilan * 100 // toplam})"
                    f"\nTahmini kalan süre: {kalan_metni}"
                )
                pencere.after(120, yokla)
                return

            pencere.destroy()
            if durum == "hata":
                messagebox.showerror("AI ile Büyüt", f"Büyütme başarısız:\n{deger}")
                return
            if durum == "iptal":
                self.durum_lbl.config(text="AI büyütme durduruldu.")
                return
            self.orijinal_img = deger
            self.onizleme_kaynak = deger.copy()
            self.onizleme_kaynak.thumbnail(ONIZLEME_CALISMA_BOYUTU, Image.Resampling.LANCZOS)
            self.durum_lbl.config(
                text=f"AI ile büyütüldü: {deger.width} x {deger.height} piksel"
            )
            self.cozunurlugu_degerlendir()
            self.onizlemeyi_guncelle()

        pencere.after(120, yokla)

    def onayari_uygula(self, _olay=None):
        """Hazır ayar seçilince sürgüleri ve kutucukları doldurur."""
        ayar = ONAYARLAR.get(self.onayar_combo.get())
        if not ayar:
            return
        yaricap, miktar, esik, gurultu, otomatik = ayar
        self.yaricap_slider.set(yaricap)
        self.miktar_slider.set(miktar)
        self.esik_slider.set(esik)
        self.gurultu_combo.set(gurultu)
        self.otomatik_var.set(otomatik)
        self.filtre_planla()

    def cozunurlugu_degerlendir(self, *_):
        """Seçilen matriste görselin kaç DPI'da basılacağını hesaplayıp uyarır."""
        if self.orijinal_img is None or self.mod.get() != "poster":
            self.cozunurluk_lbl.config(text="")
            return
        try:
            sutun = int(self.sutun_spin.get())
            satir = int(self.satir_spin.get())
        except (ValueError, tk.TclError):
            return
        dikey = "Dikey" in self.yon_combo.get()
        kenar = self._kenar_boslugu_mm()
        dpi = baski_cozunurlugu(self.orijinal_img, sutun, satir, dikey, kenar)
        en, boy = poster_olculeri_inc(sutun, satir, dikey, kenar)
        olcu = f"{en * 2.54:.0f} × {boy * 2.54:.0f} cm"

        if dpi >= IYI_DPI:
            self.cozunurluk_lbl.config(
                text=f"Poster {olcu} · baskı {dpi:.0f} DPI — çözünürlük yeterli.",
                foreground="#15803d",
            )
        elif dpi >= KABUL_DPI:
            self.cozunurluk_lbl.config(
                text=f"Poster {olcu} · baskı {dpi:.0f} DPI — kabul edilebilir; "
                "birkaç adım uzaktan bakıldığında sorun görünmez.",
                foreground="#b45309",
            )
        else:
            ek = " Akıllı büyütme açık." if self.buyut_var.get() else ""
            self.cozunurluk_lbl.config(
                text=f"Poster {olcu} · baskı {dpi:.0f} DPI — DÜŞÜK. Yakından bakınca "
                f"pikselli görünür. Sayfa sayısını azaltın ya da daha büyük bir görsel "
                f"kullanın.{ek}",
                foreground="#b91c1c",
            )

    # ------------------------------------------------------- baskı raporu ve 1:1 önizleme
    def baski_raporu_metni(self) -> str:
        """Üretimden önce her şeyi tek ekranda özetleyen rapor."""
        if self.orijinal_img is None:
            return "Henüz bir görsel açılmadı."
        try:
            sutun, satir = int(self.sutun_spin.get()), int(self.satir_spin.get())
            cakisma = int(self.cakisma_spin.get())
        except (ValueError, tk.TclError):
            return "Sütun, satır ve çakışma payı sayı olmalı."

        dikey = "Dikey" in self.yon_combo.get()
        kenar = self._kenar_boslugu_mm()
        en_cm, boy_cm = self.poster_olcusu_cm()
        dpi = baski_cozunurlugu(self.orijinal_img, sutun, satir, dikey, kenar)
        sayfa = sutun * satir

        # Kesim uzunluğu: her sayfanın kesilecek kenarları (dış kenarlar kesilmez).
        sayfa_en = en_cm / sutun
        sayfa_boy = boy_cm / satir
        kesim_cm = 0.0
        for i in range(satir):
            for j in range(sutun):
                kesim_cm += (sayfa_boy if j < sutun - 1 else 0) + (sayfa_en if i < satir - 1 else 0)

        if dpi >= IYI_DPI:
            deger = "yeterli"
        elif dpi >= KABUL_DPI:
            deger = "kabul edilebilir"
        else:
            deger = "DÜŞÜK"

        satirlar = [
            "BASKI RAPORU",
            "=" * 46,
            "",
            "KAYNAK",
            f"  Dosya           : {os.path.basename(self.resim_yolu or '-')}",
            f"  Çözünürlük      : {self.orijinal_img.width} x {self.orijinal_img.height} piksel",
            "",
            "POSTER",
            f"  Matris          : {sutun} sütun x {satir} satır = {sayfa} sayfa A4",
            f"  Sayfa yönü      : {self.yon_combo.get()}",
            f"  Yazıcı kenarı   : {kenar:.0f} mm (basılamayan pay)",
            f"  Poster ölçüsü   : {en_cm:.1f} x {boy_cm:.1f} cm",
            f"  Tek sayfa alanı : {sayfa_en:.1f} x {sayfa_boy:.1f} cm",
            "",
            "BASKI KALİTESİ",
            f"  Baskı çözünürlüğü: {dpi:.0f} DPI ({deger})",
            f"  Çakışma payı     : {cakisma} piksel",
            f"  Kesim işaretleri : {'var' if self.isaret_var.get() else 'yok'}",
            f"  Montaj haritası  : {'var' if self.harita_var.get() else 'yok'}",
            f"  Kesilecek uzunluk: yaklaşık {kesim_cm / 100:.1f} metre",
            "",
            "İYİLEŞTİRME",
            f"  Hazır ayar      : {self.onayar_combo.get()}",
            f"  Otomatik düzelt : {'açık' if self.otomatik_var.get() else 'kapalı'}",
            f"  Gürültü azaltma : {self.gurultu_combo.get()}",
            f"  Keskinleştirme  : yarıçap {self.yaricap_slider.get():.1f}, "
            f"miktar %{self.miktar_slider.get():.0f}, eşik {self.esik_slider.get():.0f}",
            f"  Akıllı büyütme  : {'açık' if self.buyut_var.get() else 'kapalı'}",
            f"  Kâğıt telafisi  : {self.kagit_combo.get()}",
        ]

        uyarilar = []
        if dpi < KABUL_DPI:
            uyarilar.append(
                f"Baskı {dpi:.0f} DPI — yakından bakınca pikselli görünecek. "
                "Sayfa sayısını azaltmayı ya da daha büyük bir görsel kullanmayı düşünün."
            )
        if kenar == 0:
            uyarilar.append(
                "Kenar boşluğu 0 mm. Yazıcınız kenarlıksız basamıyorsa her sayfadan "
                "birkaç milimetre kırpılır ve parçalar tam tutmaz."
            )
        if cakisma == 0 and sayfa > 1:
            uyarilar.append(
                "Çakışma payı yok. Kesip yapıştırırken hiç tolerans kalmaz; 15-30 piksel önerilir."
            )
        if sayfa > 12:
            uyarilar.append(f"{sayfa} sayfa basılacak; kâğıt ve mürekkep tüketimi yüksek olacak.")
        if uyarilar:
            satirlar += ["", "UYARILAR"]
            satirlar += [f"  ! {u}" for u in uyarilar]
        satirlar += [
            "",
            "YAZDIRMA",
            "  Ölçek: %100 / Gerçek Boyut  (Sayfaya Sığdır KAPALI olmalı)",
            "  Kâğıt: A4",
        ]
        return "\n".join(satirlar)

    def baski_raporunu_goster(self):
        self.cozunurlugu_degerlendir()  # panel uyarısı raporla aynı değerleri göstersin
        rapor = self.baski_raporu_metni()
        pencere = tk.Toplevel(self.root)
        pencere.title("Baskı Raporu")
        pencere.transient(self.root)
        cerceve = ttk.Frame(pencere, padding=12)
        cerceve.pack(fill=tk.BOTH, expand=True)
        kutu = tk.Text(cerceve, width=52, height=28, wrap=tk.WORD, font=("monospace", 9))
        kutu.insert("1.0", rapor)
        kutu.config(state=tk.DISABLED)
        kutu.pack(fill=tk.BOTH, expand=True)
        ttk.Button(cerceve, text="Kapat", command=pencere.destroy).pack(pady=(10, 0))
        pencere.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - pencere.winfo_width()) // 2
        pencere.geometry(f"+{max(0, x)}+{self.root.winfo_rooty() + 40}")

    def gercek_boyut_onizleme(self):
        """Görselin küçük bir bölgesini gerçek baskı ölçeğinde gösterir."""
        if self.orijinal_img is None:
            messagebox.showinfo("Gerçek Boyut Önizleme", "Önce bir görsel açın.")
            return
        try:
            sutun, satir = int(self.sutun_spin.get()), int(self.satir_spin.get())
        except (ValueError, tk.TclError):
            return
        dikey = "Dikey" in self.yon_combo.get()
        baski_dpi = baski_cozunurlugu(
            self.orijinal_img, sutun, satir, dikey, self._kenar_boslugu_mm()
        )
        if baski_dpi <= 0:
            return

        pencere = tk.Toplevel(self.root)
        pencere.title("Gerçek Boyut Önizleme (1:1)")
        pencere.transient(self.root)
        cerceve = ttk.Frame(pencere, padding=10)
        cerceve.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            cerceve,
            text="Bu pencere, posterin küçük bir bölgesini kâğıttaki gerçek ölçüsünde gösterir.\n"
            "Sürükleyerek gezinebilirsiniz. Ekranınızdaki cetvel ölçüsü tutmuyorsa "
            "aşağıdaki ekran DPI değerini düzeltin.",
            wraplength=560,
            foreground="gray",
        ).pack(anchor=tk.W, pady=(0, 8))

        # Ekranın gerçek DPI'ı: Tk bunu bildirir ama bazı sistemlerde yanlış olur;
        # kullanıcı cetvelle kontrol edip düzeltebilsin diye ayar bırakıldı.
        ekran_dpi = tk.DoubleVar(value=round(self.root.winfo_fpixels("1i"), 1))
        ekran_w = min(760, int(self.root.winfo_screenwidth() * 0.7))
        ekran_h = min(460, int(self.root.winfo_screenheight() * 0.5))
        tuval = tk.Canvas(cerceve, width=ekran_w, height=ekran_h, background="#e5e5e5")
        tuval.pack()

        durum = {"x": self.orijinal_img.width // 2, "y": self.orijinal_img.height // 2}
        tutamak = {"img": None}

        def cetvel_ciz():
            """Üst kenara santimetre cetveli çizer: gerçek bir cetvelle karşılaştırıp
            ekran DPI'ını doğrulamak için."""
            piksel_cm = ekran_dpi.get() / 2.54
            if piksel_cm <= 4:
                return
            # Şerit düz beyaz olmalı: yarı saydam bırakılınca koyu görsellerde
            # çizgiler ve rakamlar okunmuyor.
            tuval.create_rectangle(0, 0, ekran_w, 26, fill="#ffffff", outline="#bbbbbb")
            cm = 0
            while cm * piksel_cm < ekran_w:
                x = cm * piksel_cm
                tuval.create_line(x, 0, x, 14, fill="#111111", width=1)
                if cm:
                    tuval.create_text(x + 2, 18, text=str(cm), anchor="w", font=("", 7))
                yarim = x + piksel_cm / 2
                if yarim < ekran_w:
                    tuval.create_line(yarim, 0, yarim, 8, fill="#444444")
                cm += 1
            tuval.create_text(
                ekran_w - 4, 18, text="cm", anchor="e", font=("", 7), fill="#444444"
            )

        def ciz(*_):
            oran = ekran_dpi.get() / baski_dpi  # 1 görüntü pikseli kaç ekran pikseli
            if oran <= 0:
                return
            # Yalnızca görünen bölge kırpılır; dev görüntülerde bellek şişmesin.
            gorunen_w = max(8, int(ekran_w / oran))
            gorunen_h = max(8, int(ekran_h / oran))
            sol = max(0, min(durum["x"] - gorunen_w // 2, self.orijinal_img.width - gorunen_w))
            ust = max(0, min(durum["y"] - gorunen_h // 2, self.orijinal_img.height - gorunen_h))
            parca = self.orijinal_img.crop((sol, ust, sol + gorunen_w, ust + gorunen_h))
            parca = self.keskinlestirmeyi_uygula(self.renk_ve_gurultu(parca))
            parca = parca.resize(
                (ekran_w, ekran_h),
                Image.Resampling.LANCZOS if oran < 1 else Image.Resampling.NEAREST,
            )
            tutamak["img"] = ImageTk.PhotoImage(parca)
            tuval.delete("all")
            tuval.create_image(0, 0, anchor="nw", image=tutamak["img"])
            cetvel_ciz()
            olcu_cm = ekran_w / ekran_dpi.get() * 2.54
            bilgi.config(
                text=f"Baskı çözünürlüğü {baski_dpi:.0f} DPI · gösterilen genişlik "
                f"yaklaşık {olcu_cm:.1f} cm"
            )

        bilgi = ttk.Label(cerceve, text="", foreground="gray")
        bilgi.pack(anchor=tk.W, pady=(6, 0))

        surukle = {"x": 0, "y": 0}

        def basildi(olay):
            surukle.update(x=olay.x, y=olay.y)

        def suruklendi(olay):
            oran = ekran_dpi.get() / baski_dpi
            durum["x"] -= int((olay.x - surukle["x"]) / max(oran, 0.01))
            durum["y"] -= int((olay.y - surukle["y"]) / max(oran, 0.01))
            surukle.update(x=olay.x, y=olay.y)
            ciz()

        tuval.bind("<Button-1>", basildi)
        tuval.bind("<B1-Motion>", suruklendi)

        alt = ttk.Frame(cerceve)
        alt.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(alt, text="Ekran DPI:").pack(side=tk.LEFT)
        ttk.Spinbox(
            alt, from_=60, to=400, width=6, textvariable=ekran_dpi, command=ciz
        ).pack(side=tk.LEFT, padx=6)
        ttk.Button(alt, text="Kapat", command=pencere.destroy).pack(side=tk.RIGHT)
        ciz()

    def _kenar_boslugu_mm(self) -> float:
        try:
            return max(0.0, min(float(self.kenar_spin.get()), 20.0))
        except (ValueError, tk.TclError):
            return 5.0

    def poster_olcusu_cm(self) -> tuple[float, float]:
        """Seçili ayarlarla ortaya çıkacak posterin santimetre ölçüsü."""
        try:
            sutun, satir = int(self.sutun_spin.get()), int(self.satir_spin.get())
        except (ValueError, tk.TclError):
            sutun, satir = 1, 1
        dikey = "Dikey" in self.yon_combo.get()
        en, boy = poster_olculeri_inc(sutun, satir, dikey, self._kenar_boslugu_mm())
        return en * 2.54, boy * 2.54

    def _gurultu_seviyesi(self) -> int:
        return {"Kapalı": 0, "Hafif": 1, "Orta": 2, "Güçlü": 3}.get(self.gurultu_combo.get(), 0)

    def renk_ve_gurultu(self, img: Image.Image) -> Image.Image:
        """Keskinleştirme dışındaki düzeltmeler (keskinleştirme en sona bırakılır)."""
        if self.otomatik_var.get():
            img = otomatik_duzelt(img)
        img = gurultu_azalt(img, self._gurultu_seviyesi())
        # Kâğıt telafisi, kullanıcı sürgülerinin üstüne çarpan olarak biner.
        k_kontrast, k_renk, k_parlak = KAGIT_TELAFISI.get(self.kagit_combo.get(), (1.0, 1.0, 1.0))
        img = ImageEnhance.Contrast(img).enhance(self.kontrast_slider.get() * k_kontrast)
        img = ImageEnhance.Color(img).enhance(self.renk_slider.get() * k_renk)
        return ImageEnhance.Brightness(img).enhance(self.parlaklik_slider.get() * k_parlak)

    def keskinlestirmeyi_uygula(self, img: Image.Image, olcek: float = 1.0) -> Image.Image:
        """Unsharp mask uygular. olcek, önizleme küçültmesini telafi eder."""
        yaricap = self.yaricap_slider.get() * olcek
        if yaricap < 0.3:  # bu kadar küçük yarıçap görünür bir etki yapmaz
            return img
        return keskinlestir(img, yaricap, self.miktar_slider.get(), self.esik_slider.get())

    def filtreleri_uygula(self, img: Image.Image) -> Image.Image:
        """Geriye dönük tek adımlık uygulama (kaynak çözünürlükte)."""
        return self.keskinlestirmeyi_uygula(self.renk_ve_gurultu(img))

    def onizlemeyi_guncelle(self):
        self._filtre_isi = None
        if self.onizleme_kaynak is None:
            return
        gecici = self.renk_ve_gurultu(self.onizleme_kaynak.copy())
        gecici.thumbnail(ONIZLEME_GOSTERIM_BOYUTU, Image.Resampling.LANCZOS)
        # Önizleme küçültülmüş olduğu için aynı yarıçap orantılı küçültülür; yoksa
        # ekranda gerçekte olduğundan çok daha keskin görünür ve yanıltır.
        if self.orijinal_img is not None and self.orijinal_img.width:
            olcek = max(0.15, gecici.width / self.orijinal_img.width)
        else:
            olcek = 1.0
        gecici = self.keskinlestirmeyi_uygula(gecici, olcek)
        self.tk_img = ImageTk.PhotoImage(gecici)  # referans tutulmazsa görüntü kaybolur
        self.onizleme_label.config(image=self.tk_img, text="")

    def cikti_klasorunu_ac(self):
        if not (self.son_cikis_klasoru and os.path.isdir(self.son_cikis_klasoru)):
            return
        try:
            if WINDOWS:
                os.startfile(self.son_cikis_klasoru)  # noqa: S606 — sadece Windows'ta var
            elif MACOS:
                subprocess.Popen(["open", self.son_cikis_klasoru])
            else:
                subprocess.Popen(["xdg-open", self.son_cikis_klasoru])
        except (OSError, AttributeError):
            messagebox.showinfo("Klasör", f"Dosya yöneticisi açılamadı.\n\n{self.son_cikis_klasoru}")

    # ------------------------------------------------------------------ üretim
    def parcala_ve_pdf_yap(self):
        if self.mod.get() == "dizme":
            if not self.dizme_dosyalari:
                return
            self.kaydet_btn.config(state=tk.DISABLED)
            try:
                self.dizme_uret()
            except (OSError, ValueError, MemoryError) as hata:
                messagebox.showerror("Hata", f"Sayfalar üretilirken sorun çıktı:\n{hata}")
                self.durum_lbl.config(text="İşlem başarısız.")
            finally:
                self.kaydet_btn.config(state=tk.NORMAL)
            return

        if self.orijinal_img is None:
            return
        try:
            sutun_sayisi = int(self.sutun_spin.get())
            satir_sayisi = int(self.satir_spin.get())
            cakisma = int(self.cakisma_spin.get())
        except ValueError:
            messagebox.showerror("Hata", "Sütun, satır ve çakışma payı tam sayı olmalı.")
            return
        if not (1 <= sutun_sayisi <= 20 and 1 <= satir_sayisi <= 20):
            messagebox.showerror("Hata", "Sütun ve satır sayısı 1 ile 20 arasında olmalı.")
            return
        if cakisma < 0:
            messagebox.showerror("Hata", "Çakışma payı negatif olamaz.")
            return

        self.kaydet_btn.config(state=tk.DISABLED)
        try:
            self._uret(sutun_sayisi, satir_sayisi, cakisma)
        except (OSError, ValueError, MemoryError) as hata:
            messagebox.showerror("Hata", f"PDF üretilirken sorun çıktı:\n{hata}")
            self.durum_lbl.config(text="İşlem başarısız.")
        finally:
            self.kaydet_btn.config(state=tk.NORMAL)

    def _uret(self, sutun_sayisi: int, satir_sayisi: int, cakisma: int):
        toplam = sutun_sayisi * satir_sayisi
        self.durum_lbl.config(text="Tam çözünürlükte iyileştirme uygulanıyor...")
        self.root.update_idletasks()

        # Sıra önemlidir: renk/gürültü düzeltmesi -> (gerekiyorsa) büyütme -> keskinleştirme.
        # Keskinleştirme en sona bırakılmazsa büyütme onu yumuşatır ve etkisi kaybolur.
        islenen = jpeg_uyumlu(self.renk_ve_gurultu(self.orijinal_img.copy()))

        dikey = "Dikey" in self.yon_combo.get()
        if self.buyut_var.get():
            kenar_mm = self._kenar_boslugu_mm()
            onceki_dpi = baski_cozunurlugu(
                islenen, sutun_sayisi, satir_sayisi, dikey, kenar_mm
            )
            if onceki_dpi < KABUL_DPI:
                self.durum_lbl.config(text="Düşük çözünürlük: akıllı büyütme uygulanıyor...")
                self.root.update_idletasks()
                islenen, kat = akilli_buyut(
                    islenen, IYI_DPI, sutun_sayisi, satir_sayisi, dikey, kenar_mm
                )
                if kat > 1.0:
                    print(f"[büyütme] {kat:.2f} kat -> {islenen.width}x{islenen.height}", flush=True)

        islenen = self.keskinlestirmeyi_uygula(islenen)

        zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
        klasor_adi = f"Poster_OranKorumali_{zaman_damgasi}"
        cikis_klasoru = cikis_klasoru_hazirla(klasor_adi)
        pdf_yolu = os.path.join(cikis_klasoru, f"Oran_Korumali_Baski_{zaman_damgasi}.pdf")

        sayfa_boyutu = landscape(A4) if "Yatay" in self.yon_combo.get() else A4
        sayfa_w, sayfa_h = sayfa_boyutu
        pdf_canvas = canvas.Canvas(pdf_yolu, pagesize=sayfa_boyutu)

        # Yazıcıların çoğu kâğıdın en kenarına basamaz. Bu paya saygı gösterilmezse
        # her sayfadan birkaç milimetre kırpılır ve parçalar birleştiğinde tutmaz.
        kenar_pt = self._kenar_boslugu_mm() * 72 / 25.4
        kullanilabilir_w = sayfa_w - 2 * kenar_pt
        kullanilabilir_h = sayfa_h - 2 * kenar_pt
        if kullanilabilir_w <= 0 or kullanilabilir_h <= 0:
            raise ValueError("Yazıcı kenar boşluğu sayfadan büyük; değeri küçültün.")

        # Hedef matris, basılabilir alanın oranını birebir korur; resim bu alana oranı
        # bozulmadan oturtulur, artan yerler beyaz kalır.
        olcek = max(1.0, min(islenen.width / (kullanilabilir_w * sutun_sayisi), 4.0))
        hedef_w = int(kullanilabilir_w * sutun_sayisi * olcek)
        hedef_h = int(kullanilabilir_h * satir_sayisi * olcek)
        img_oranti_korumali = ImageOps.pad(
            islenen,
            (hedef_w, hedef_h),
            method=Image.Resampling.LANCZOS,
            color=(255, 255, 255),
        )

        genislik, yukseklik = img_oranti_korumali.size
        parca_genislik = genislik // sutun_sayisi
        parca_yukseklik = yukseklik // satir_sayisi

        # Her parça, çakışma payı dahil AYNI piksel boyutunda üretilir (kenar
        # parçalarında eksik kalan pay beyazla tamamlanır). Böylece bütün sayfalar
        # tek ve aynı ölçekle basılır; aksi halde sayfalar arasında ölçek farkı
        # oluşur ve parçalar yapıştırılırken tutmaz.
        kare_genislik = parca_genislik + 2 * cakisma
        kare_yukseklik = parca_yukseklik + 2 * cakisma
        pdf_olcek = min(kullanilabilir_w / kare_genislik, kullanilabilir_h / kare_yukseklik)
        ciz_w = kare_genislik * pdf_olcek
        ciz_h = kare_yukseklik * pdf_olcek
        ciz_x = kenar_pt + (kullanilabilir_w - ciz_w) / 2
        ciz_y = kenar_pt + (kullanilabilir_h - ciz_h) / 2
        cakisma_pt = cakisma * pdf_olcek  # işaretler için: bindirme şeridinin PDF ölçüsü

        if self.harita_var.get():
            en_cm, boy_cm = self.poster_olcusu_cm()
            montaj_haritasi_ciz(
                pdf_canvas, sayfa_w, sayfa_h, satir_sayisi, sutun_sayisi,
                f"{en_cm:.0f} x {boy_cm:.0f} cm",
            )

        sayac = 0
        for i in range(satir_sayisi):
            for j in range(sutun_sayisi):
                sayac += 1
                self.durum_lbl.config(text=f"Parça üretiliyor: {sayac} / {toplam}")
                self.root.update_idletasks()

                istenen_sol = j * parca_genislik - cakisma
                istenen_ust = i * parca_yukseklik - cakisma
                sol = max(0, istenen_sol)
                ust = max(0, istenen_ust)
                sag = min(genislik, (j + 1) * parca_genislik + cakisma)
                alt = min(yukseklik, (i + 1) * parca_yukseklik + cakisma)

                kirpik = img_oranti_korumali.crop((sol, ust, sag, alt))
                parca = Image.new("RGB", (kare_genislik, kare_yukseklik), (255, 255, 255))
                parca.paste(kirpik, (sol - istenen_sol, ust - istenen_ust))

                t_yolu = os.path.join(cikis_klasoru, f"parca_satir{i + 1}_sutun{j + 1}.jpg")
                parca.save(t_yolu, "JPEG", quality=95, subsampling=0, dpi=(300, 300))

                pdf_canvas.drawImage(t_yolu, ciz_x, ciz_y, width=ciz_w, height=ciz_h)
                if self.isaret_var.get():
                    kesim_isaretleri_ciz(
                        pdf_canvas, ciz_x, ciz_y, ciz_w, ciz_h, cakisma_pt,
                        i, j, satir_sayisi, sutun_sayisi,
                    )
                pdf_canvas.showPage()

        pdf_canvas.save()
        try:  # rapor çıktının yanında dursun; sonradan "hangi ayarla basmıştım" sorusu kalmasın
            with open(
                os.path.join(cikis_klasoru, "baski_raporu.txt"), "w", encoding="utf-8"
            ) as rapor_dosyasi:
                rapor_dosyasi.write(self.baski_raporu_metni())
        except OSError:
            pass
        self.son_cikis_klasoru = cikis_klasoru
        self.klasor_btn.config(state=tk.NORMAL)
        # Masaüstü yazılamazsa çıktı başka klasöre düşebilir; nereye gittiği yazsın.
        nerede = os.path.basename(os.path.dirname(os.path.dirname(cikis_klasoru)))
        self.durum_lbl.config(
            text=f"Tamamlandı: {toplam} sayfa → {os.path.basename(pdf_yolu)} ({nerede})"
        )
        messagebox.showinfo(
            "Hazır",
            f"{toplam} sayfalık PDF oluşturuldu.\n\n"
            f"Klasör:\n{cikis_klasoru}\n\n"
            "Yazdırırken ölçeklendirmeyi '%100 / Gerçek Boyut' seçin.",
        )


def main() -> int:
    try:
        root = tk.Tk()
    except tk.TclError as hata:
        print(f"Grafik arayüz başlatılamadı: {hata}", file=sys.stderr)
        return 1
    SunmesizBaskiApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# powered by Omer OZTURK

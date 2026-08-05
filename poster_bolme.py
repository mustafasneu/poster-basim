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
GEREKLI_PAKETLER = ("pillow>=10", "reportlab>=4", "pypdfium2>=4")
# PDF okuma bileşeni programın açılması için şart değildir; yoksa yalnızca PDF
# kaynak kullanılamaz, o yüzden başlangıç denetiminde aranmaz (bkz. _calisir_mi).
PDF_PAKETI = "pypdfium2>=4"
PROJE_DIZINI = os.path.dirname(os.path.abspath(__file__))
VENV_DIZINI = os.path.join(PROJE_DIZINI, ".venv")
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

from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageTk  # noqa: E402
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


def pdf_sayfasini_goruntuye_cevir(yol: str, sayfa_no: int = 1) -> Image.Image:
    """PDF'in bir sayfasını baskı çözünürlüğünde görüntüye çevirir (sayfa_no 1'den başlar)."""
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
        olcek = PDF_DPI / 72
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

    if veri[:5] == b"%PDF-":
        bicim = "pdf"
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
    simge_yolu = os.path.join(PROJE_DIZINI, "simge.png")
    if not os.path.exists(simge_yolu):
        return None
    try:
        simge = ImageTk.PhotoImage(Image.open(simge_yolu))
        root.iconphoto(True, simge)  # referans tutulmazsa simge kaybolur
        return simge
    except (OSError, tk.TclError):
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


def jpeg_uyumlu(img: Image.Image) -> Image.Image:
    """Alfa kanallı / paletli resimleri beyaz zemine düzleştirip RGB'ye çevirir."""
    if img.mode == "RGB":
        return img
    if img.mode in ("RGBA", "LA", "PA") or (img.mode == "P" and "transparency" in img.info):
        img = img.convert("RGBA")
        zemin = Image.new("RGB", img.size, (255, 255, 255))
        zemin.paste(img, mask=img.split()[-1])
        return zemin
    return img.convert("RGB")


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
        self.sutun_spin = ttk.Spinbox(ayarlar, from_=1, to=20, width=10)
        self.sutun_spin.set(4)
        self.sutun_spin.pack(pady=5, anchor=tk.W)

        ttk.Label(ayarlar, text="Satır Sayısı (Dikey - Y):").pack(anchor=tk.W)
        self.satir_spin = ttk.Spinbox(ayarlar, from_=1, to=20, width=10)
        self.satir_spin.set(2)
        self.satir_spin.pack(pady=5, anchor=tk.W)

        ttk.Label(ayarlar, text="Yazıcı Sayfa Yönü:").pack(anchor=tk.W)
        self.yon_combo = ttk.Combobox(
            ayarlar, values=["Yatay (Landscape)", "Dikey (Portrait)"], state="readonly"
        )
        self.yon_combo.set("Yatay (Landscape)")
        self.yon_combo.pack(fill=tk.X, pady=5)

        ttk.Label(ayarlar, text="Çakışma Payı (Piksel Bindirme):").pack(anchor=tk.W)
        self.cakisma_spin = ttk.Spinbox(ayarlar, from_=0, to=100, width=10)
        self.cakisma_spin.set(15)
        self.cakisma_spin.pack(pady=5, anchor=tk.W)

        ttk.Label(
            ayarlar, text="--- 3. DETAYLI İYİLEŞTİRME ---", font=(self.font_ailesi, 11, "bold")
        ).pack(pady=15, anchor=tk.W)

        self.keskinlik_slider = self._surgu_ekle(ayarlar, "Detay Netliği (Keskinlik):", 1.0, 4.0)
        self.kontrast_slider = self._surgu_ekle(ayarlar, "Dinamik Kontrast:", 0.5, 2.5)
        self.renk_slider = self._surgu_ekle(ayarlar, "Renk Canlılığı (Saturasyon):", 0.5, 2.5)
        self.parlaklik_slider = self._surgu_ekle(ayarlar, "Genel Parlaklık:", 0.5, 2.0)

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

    def _surgu_ekle(self, ust: ttk.Frame, etiket: str, alt_sinir: float, ust_sinir: float):
        ttk.Label(ust, text=etiket).pack(anchor=tk.W)
        surgu = ttk.Scale(
            ust, from_=alt_sinir, to=ust_sinir, orient=tk.HORIZONTAL, command=self.filtre_planla
        )
        surgu.set(1.0)
        surgu.pack(fill=tk.X, pady=5)
        return surgu

    # ------------------------------------------------------------------ eylemler
    def resim_sec(self):
        dosya_tipleri = [
            ("Resim ve PDF", "*.jpg *.jpeg *.png *.bmp *.webp *.tif *.tiff *.pdf"),
            ("Resim Dosyaları", "*.jpg *.jpeg *.png *.bmp *.webp *.tif *.tiff"),
            ("PDF Dosyaları", "*.pdf"),
            ("Tüm Dosyalar", "*.*"),
        ]
        secilen_yol = filedialog.askopenfilename(
            title="Bir Resim ya da PDF Seçin", filetypes=dosya_tipleri
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
            sayfa_no = self._sayfa_penceresi(toplam)
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

    def _sayfa_penceresi(self, toplam: int) -> int | None:
        """Çok sayfalı PDF'te hangi sayfanın poster olacağını sorar."""
        pencere = tk.Toplevel(self.root)
        pencere.title("PDF sayfası seçin")
        pencere.transient(self.root)
        pencere.resizable(False, False)
        cerceve = ttk.Frame(pencere, padding=15)
        cerceve.pack(fill=tk.BOTH, expand=True)

        ttk.Label(cerceve, text=f"Bu PDF {toplam} sayfadan oluşuyor.").pack(anchor=tk.W)
        ttk.Label(
            cerceve,
            text="Postere dönüştürülecek sayfayı seçin:",
            foreground="gray",
        ).pack(anchor=tk.W, pady=(2, 8))

        secim = ttk.Spinbox(cerceve, from_=1, to=toplam, width=8)
        secim.set(1)
        secim.pack(anchor=tk.W)

        sonuc: dict[str, int | None] = {"sayfa": None}

        def onayla(_olay=None):
            try:
                deger = int(secim.get())
            except ValueError:
                return
            if 1 <= deger <= toplam:
                sonuc["sayfa"] = deger
                pencere.destroy()

        dugmeler = ttk.Frame(cerceve)
        dugmeler.pack(fill=tk.X, pady=(12, 0))
        ttk.Button(dugmeler, text="İptal", command=pencere.destroy).pack(side=tk.RIGHT)
        ttk.Button(dugmeler, text="Bu Sayfayı Kullan", command=onayla).pack(
            side=tk.RIGHT, padx=(0, 8)
        )

        pencere.bind("<Return>", onayla)
        pencere.bind("<Escape>", lambda _o: pencere.destroy())
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
        if secilen_yol.lower().endswith(".pdf"):
            img = self._pdf_yukle(secilen_yol)
            if img is None:
                return
        else:
            try:
                img = Image.open(secilen_yol)
                img.load()
                img = ImageOps.exif_transpose(img)  # telefon fotoğraflarının yönünü düzeltir
            except (OSError, ValueError) as hata:
                messagebox.showerror("Hata", f"Resim açılamadı:\n{hata}")
                return

        self.resim_yolu = secilen_yol
        self.orijinal_img = img
        self.onizleme_kaynak = img.copy()
        self.onizleme_kaynak.thumbnail(ONIZLEME_CALISMA_BOYUTU, Image.Resampling.LANCZOS)

        self.dosya_lbl.config(text=os.path.basename(secilen_yol), foreground="black")
        self.durum_lbl.config(text=f"Kaynak çözünürlük: {img.width} x {img.height} piksel")
        self.ayarlari_sifirla()
        self.kaydet_btn.config(state=tk.NORMAL)

    def ayarlari_sifirla(self):
        for surgu in (
            self.keskinlik_slider,
            self.kontrast_slider,
            self.renk_slider,
            self.parlaklik_slider,
        ):
            surgu.set(1.0)
        self.filtre_planla()

    def filtre_planla(self, _event=None):
        """Sürgü hareketini geciktirerek uygular (her pikselde yeniden işlemeyi önler)."""
        if self.onizleme_kaynak is None:
            return
        if self._filtre_isi is not None:
            self.root.after_cancel(self._filtre_isi)
        self._filtre_isi = self.root.after(60, self.onizlemeyi_guncelle)

    def filtreleri_uygula(self, img: Image.Image) -> Image.Image:
        if self.keskinlik_slider.get() > 1.0:
            img = ImageEnhance.Sharpness(img).enhance(self.keskinlik_slider.get())
            img = img.filter(ImageFilter.DETAIL)
        img = ImageEnhance.Contrast(img).enhance(self.kontrast_slider.get())
        img = ImageEnhance.Color(img).enhance(self.renk_slider.get())
        img = ImageEnhance.Brightness(img).enhance(self.parlaklik_slider.get())
        return img

    def onizlemeyi_guncelle(self):
        self._filtre_isi = None
        if self.onizleme_kaynak is None:
            return
        gecici = self.filtreleri_uygula(self.onizleme_kaynak.copy())
        gecici.thumbnail(ONIZLEME_GOSTERIM_BOYUTU, Image.Resampling.LANCZOS)
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

        islenen = jpeg_uyumlu(self.filtreleri_uygula(self.orijinal_img.copy()))

        zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
        klasor_adi = f"Poster_OranKorumali_{zaman_damgasi}"
        cikis_klasoru = cikis_klasoru_hazirla(klasor_adi)
        pdf_yolu = os.path.join(cikis_klasoru, f"Oran_Korumali_Baski_{zaman_damgasi}.pdf")

        sayfa_boyutu = landscape(A4) if "Yatay" in self.yon_combo.get() else A4
        sayfa_w, sayfa_h = sayfa_boyutu
        pdf_canvas = canvas.Canvas(pdf_yolu, pagesize=sayfa_boyutu)

        # Hedef matris, sayfa oranını birebir korur; resim bu alana oranı bozulmadan
        # oturtulur, artan yerler beyaz kalır (baskıda mürekkep yemesin diye).
        olcek = max(1.0, min(islenen.width / (sayfa_w * sutun_sayisi), 4.0))
        hedef_w = int(sayfa_w * sutun_sayisi * olcek)
        hedef_h = int(sayfa_h * satir_sayisi * olcek)
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
        pdf_olcek = min(sayfa_w / kare_genislik, sayfa_h / kare_yukseklik)
        ciz_w = kare_genislik * pdf_olcek
        ciz_h = kare_yukseklik * pdf_olcek
        ciz_x = (sayfa_w - ciz_w) / 2
        ciz_y = (sayfa_h - ciz_h) / 2

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
                pdf_canvas.showPage()

        pdf_canvas.save()
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

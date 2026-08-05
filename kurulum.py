#!/usr/bin/env python3
"""Masaüstü kısayolu oluşturur — Windows, Linux ve macOS.

Kullanım:  python3 kurulum.py        (kısayolu oluşturur)
           python3 kurulum.py --kaldir  (kısayolu siler)

Programın kendisi zaten kendi bağımlılıklarını kuruyor; bu dosya yalnızca
"çift tıklayınca açılsın" kısayolunu ilgili işletim sisteminin usulüne göre
yerleştirir.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys

PROJE_DIZINI = os.path.dirname(os.path.abspath(__file__))
PROGRAM = os.path.join(PROJE_DIZINI, "poster_bolme.py")
SIMGE_PNG = os.path.join(PROJE_DIZINI, "simge.png")
SIMGE_ICO = os.path.join(PROJE_DIZINI, "simge.ico")
AD = "Poster Bölücü"
ACIKLAMA = "Resmi A4 sayfalara bölüp baskıya hazır PDF üretir"

WINDOWS = os.name == "nt"
MACOS = sys.platform == "darwin"


# --------------------------------------------------------------------- ortak
def masaustu_yolu() -> str:
    """Masaüstü klasörünü bul (işletim sistemi ve dil ayarından bağımsız)."""
    ev = os.path.expanduser("~")
    if WINDOWS:
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
    elif not MACOS:
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


def _pencereli_python() -> str:
    """Arayüzü konsol penceresi açmadan başlatan yorumlayıcı."""
    if WINDOWS:
        aday = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
        if os.path.exists(aday):
            return aday
    return sys.executable


# ------------------------------------------------------------------ Windows
def _windows_kisayol_yolu() -> str:
    return os.path.join(masaustu_yolu(), f"{AD}.lnk")


def windows_olustur() -> str:
    hedef = _pencereli_python()
    kisayol = _windows_kisayol_yolu()
    simge = SIMGE_ICO if os.path.exists(SIMGE_ICO) else hedef
    betik = (
        "$s = (New-Object -ComObject WScript.Shell).CreateShortcut({kisayol});"
        "$s.TargetPath = {hedef};"
        "$s.Arguments = {arg};"
        "$s.WorkingDirectory = {calisma};"
        "$s.IconLocation = {simge};"
        "$s.Description = {aciklama};"
        "$s.Save()"
    ).format(
        kisayol=_ps_metin(kisayol),
        hedef=_ps_metin(hedef),
        arg=_ps_metin(f'"{PROGRAM}"'),
        calisma=_ps_metin(PROJE_DIZINI),
        simge=_ps_metin(simge),
        aciklama=_ps_metin(ACIKLAMA),
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", betik],
        check=True,
        timeout=120,
    )
    return kisayol


def _ps_metin(deger: str) -> str:
    """PowerShell tek tırnaklı dizgesi (içerdeki tırnak ikilenir)."""
    return "'" + deger.replace("'", "''") + "'"


# -------------------------------------------------------------------- macOS
def _macos_kisayol_yolu() -> str:
    return os.path.join(masaustu_yolu(), f"{AD}.command")


def macos_olustur() -> str:
    kisayol = _macos_kisayol_yolu()
    with open(kisayol, "w", encoding="utf-8") as dosya:
        dosya.write(
            "#!/bin/bash\n"
            f'cd "{PROJE_DIZINI}" || exit 1\n'
            f'exec "{sys.executable}" "{PROGRAM}"\n'
        )
    os.chmod(kisayol, 0o755)
    return kisayol


# -------------------------------------------------------------------- Linux
def _linux_desktop_dosyalari() -> list[str]:
    menu = os.path.join(
        os.path.expanduser("~/.local/share/applications"), "poster-bolucu.desktop"
    )
    return [menu, os.path.join(masaustu_yolu(), f"{AD}.desktop")]


def linux_olustur() -> str:
    simge = _linux_simgeyi_kur()
    icerik = (
        "[Desktop Entry]\n"
        "Type=Application\n"
        f"Name={AD}\n"
        f"Comment={ACIKLAMA}\n"
        f'Exec="{sys.executable}" "{PROGRAM}"\n'
        f"Path={PROJE_DIZINI}\n"
        f"Icon={simge}\n"
        "Terminal=false\n"
        "Categories=Graphics;Photography;\n"
        "StartupNotify=true\n"
    )
    for yol in _linux_desktop_dosyalari():
        os.makedirs(os.path.dirname(yol), exist_ok=True)
        with open(yol, "w", encoding="utf-8") as dosya:
            dosya.write(icerik)
        os.chmod(yol, 0o755)

    # GNOME 42+ masaüstündeki başlatıcıya "güvenilir" damgası ister.
    gio = shutil.which("gio")
    if gio:
        subprocess.run(
            [gio, "set", _linux_desktop_dosyalari()[1], "metadata::trusted", "true"],
            check=False,
            timeout=30,
        )
    guncelle = shutil.which("update-desktop-database")
    if guncelle:
        subprocess.run(
            [guncelle, os.path.dirname(_linux_desktop_dosyalari()[0])], check=False, timeout=60
        )
    return _linux_desktop_dosyalari()[1]


def _linux_simgeyi_kur() -> str:
    """Simgeyi kullanıcı tema klasörüne kopyalar; olmazsa dosya yolunu kullanır."""
    if not os.path.exists(SIMGE_PNG):
        return "image-x-generic"
    hedef_dizin = os.path.expanduser("~/.local/share/icons/hicolor/256x256/apps")
    try:
        os.makedirs(hedef_dizin, exist_ok=True)
        hedef = os.path.join(hedef_dizin, "poster-bolucu.png")
        shutil.copyfile(SIMGE_PNG, hedef)
        return hedef
    except OSError:
        return SIMGE_PNG


# --------------------------------------------------------------------- akış
def kisayol_yollari() -> list[str]:
    if WINDOWS:
        return [_windows_kisayol_yolu()]
    if MACOS:
        return [_macos_kisayol_yolu()]
    return _linux_desktop_dosyalari()


def kaldir() -> int:
    silinen = 0
    for yol in kisayol_yollari():
        if os.path.exists(yol):
            try:
                os.remove(yol)
                silinen += 1
                print(f"Silindi: {yol}")
            except OSError as hata:
                print(f"Silinemedi: {yol} ({hata})", file=sys.stderr)
    if not silinen:
        print("Silinecek kısayol bulunamadı.")
    return 0


def main() -> int:
    if not os.path.exists(PROGRAM):
        print(f"Program dosyası bulunamadı: {PROGRAM}", file=sys.stderr)
        return 1
    if "--kaldir" in sys.argv:
        return kaldir()

    try:
        if WINDOWS:
            kisayol = windows_olustur()
        elif MACOS:
            kisayol = macos_olustur()
        else:
            kisayol = linux_olustur()
    except (OSError, subprocess.SubprocessError) as hata:
        print(f"Kısayol oluşturulamadı: {hata}", file=sys.stderr)
        return 1

    print(f"Kısayol hazır: {kisayol}")
    print("Masaüstündeki simgeye çift tıklayarak programı başlatabilirsiniz.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# powered by Omer OZTURK

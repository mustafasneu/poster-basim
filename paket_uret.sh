#!/usr/bin/env bash
# Tek dosyalık paket üretir (Windows .exe, macOS .app, Linux çalıştırılabilir).
# GitHub Actions bu betiği çağırır; derleme ayarları burada durur ki iş akışı
# dosyasına dokunmadan güncellenebilsin.
set -euo pipefail

# PyInstaller'ın --add-data ayracı Windows'ta ";", diğerlerinde ":" olur.
if [[ "${RUNNER_OS:-$(uname -s)}" == "Windows" ]]; then
    AYIRAC=";"
    SIMGE="simge.ico"
else
    AYIRAC=":"
    SIMGE="simge.png"
fi

pyinstaller --noconfirm --clean --onefile --windowed \
    --name "Poster Basim" \
    --icon "$SIMGE" \
    --add-data "simge.png${AYIRAC}." \
    --collect-all PIL \
    --hidden-import PIL._tkinter_finder \
    --collect-all pypdfium2 \
    --collect-all tkinterdnd2 \
    --collect-all rawpy \
    --collect-all pillow_heif \
    --collect-all onnxruntime \
    poster_bolme.py

# Çıktı adına platform eklenir: indiren kişi hangi sürüm olduğunu görsün.
# Boşluk yerine tire, çünkü GitHub Releases boşlukları noktaya çeviriyor.
case "${RUNNER_OS:-$(uname -s)}" in
    Windows)
        mv "dist/Poster Basim.exe" "dist/Poster-Basim-Windows.exe"
        ;;
    macOS | Darwin)
        # .app bir klasördür; yapı bozulmasın diye zip'lenir.
        ( cd dist && zip -qry "Poster-Basim-macOS.zip" "Poster Basim.app" && rm -rf "Poster Basim.app" )
        ;;
    *)
        mv "dist/Poster Basim" "dist/Poster-Basim-Linux"
        ;;
esac

# Kılavuz paketin yanında dursun.
cp KULLANIM_KILAVUZU.pdf dist/ 2>/dev/null || true

echo "--- üretilen dosyalar ---"
ls -la dist/

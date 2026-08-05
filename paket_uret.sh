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
    --collect-all rawpy \
    --collect-all pillow_heif \
    --collect-all onnxruntime \
    poster_bolme.py

# macOS'ta .app bir klasördür; yapı bozulmasın diye zip'lenir.
if [[ "${RUNNER_OS:-}" == "macOS" ]]; then
    ( cd dist && zip -qry "Poster Basim-macOS.zip" "Poster Basim.app" && rm -rf "Poster Basim.app" )
fi

# Kılavuz paketin yanında dursun.
cp KULLANIM_KILAVUZU.pdf dist/ 2>/dev/null || true

echo "--- üretilen dosyalar ---"
ls -la dist/

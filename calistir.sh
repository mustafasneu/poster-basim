#!/usr/bin/env bash
# Poster Basım — Linux ve macOS başlatıcısı. Çift tıklayın ya da ./calistir.sh
# Eksik bileşenleri programın kendisi kurar; burada yalnızca uygun Python seçilir.
set -euo pipefail
PROJE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJE"

# "--kisayol" ile çağrılırsa programı değil, masaüstü kısayolu oluşturucuyu açar.
HEDEF="poster_bolme.py"
if [ "${1:-}" = "--kisayol" ]; then
    HEDEF="kurulum.py"
    shift
fi

hazir_mi() { [ -x "$1" ] && "$1" -c "import tkinter, PIL, reportlab" >/dev/null 2>&1; }
tkinterli_mi() { [ -x "$1" ] && "$1" -c "import tkinter" >/dev/null 2>&1; }

# 1) Daha önce hazırlanmış ortam varsa doğrudan onunla aç (en hızlı yol).
for py in "$PROJE/.venv/bin/python" "$PROJE/.venv-sistem/bin/python"; do
    if hazir_mi "$py"; then
        exec "$py" "$HEDEF" "$@"
    fi
done

# 2) Sistemde tkinter'ı olan bir Python ara; bulunursa program kalan bileşenleri
#    kendi .venv klasörüne kendisi kurar.
ADAYLAR=(python3 python3.13 python3.12 python3.11 python3.10 python)
if [ "$(uname -s)" = "Darwin" ]; then
    ADAYLAR+=(
        /opt/homebrew/bin/python3
        /usr/local/bin/python3
        /Library/Frameworks/Python.framework/Versions/Current/bin/python3
    )
fi

for aday in "${ADAYLAR[@]}"; do
    yol="$(command -v "$aday" 2>/dev/null || true)"
    if [ -z "$yol" ] && [ -x "$aday" ]; then
        yol="$aday"
    fi
    if [ -n "$yol" ] && tkinterli_mi "$yol"; then
        exec "$yol" "$HEDEF" "$@"
    fi
done

# 3) Hiçbiri olmadı: program kendi kurulum yolunu denesin, olmazsa açıklayıcı hata versin.
if command -v python3 >/dev/null 2>&1; then
    exec python3 "$HEDEF" "$@"
fi

echo "Python 3 bulunamadı."
echo "  Linux : sudo apt install -y python3 python3-tk"
echo "  macOS : brew install python python-tk   (ya da python.org kurulumu)"
exit 1

# powered by Omer OZTURK

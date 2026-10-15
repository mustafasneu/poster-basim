#!/bin/bash
# Masaüstüne "Poster Basım" kısayolu koyar. Çift tıklayın, bir kez yeterli.
# macOS "geliştirici doğrulanamadı" derse: sağ tık → Aç → Aç.
cd "$(dirname "$0")" || exit 1
./calistir.sh --kisayol
echo
echo "Bu pencereyi kapatabilirsiniz."

# powered by Ömer ÖZTÜRK & Mustafa ŞEKER

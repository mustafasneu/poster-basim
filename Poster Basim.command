#!/bin/bash
# Poster Basım — macOS başlatıcısı. Finder'da çift tıklayın.
# İlk açılışta macOS "geliştirici doğrulanamadı" derse: sağ tık → Aç → Aç.
cd "$(dirname "$0")" || exit 1
exec ./calistir.sh "$@"

# powered by Omer OZTURK

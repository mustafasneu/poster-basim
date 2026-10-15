#!/usr/bin/env bash
# Masaüstüne "Poster Basım" kısayolu koyar. Çift tıklayın (Çalıştır deyin),
# ya da terminalden: ./kisayol-olustur.sh — bir kez çalıştırmak yeterlidir.
cd "$(dirname "$0")" || exit 1
exec ./calistir.sh --kisayol

# powered by Ömer ÖZTÜRK & Mustafa ŞEKER

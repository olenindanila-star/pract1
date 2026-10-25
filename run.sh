#!/bin/sh
# Запуск эмулятора командной оболочки.
cd "$(dirname "$0")" || exit 1
python3 src/main.py "$@"

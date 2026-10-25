#!/bin/sh
# Запуск эмулятора с параметром --vfs (загрузка VFS, имя попадёт в заголовок окна).
cd "$(dirname "$0")/.." || exit 1
python3 src/main.py --vfs vfs/deep.json

#!/bin/sh
# Запуск эмулятора с параметром --vfs (имя VFS попадёт в заголовок окна).
cd "$(dirname "$0")/.." || exit 1
python3 src/main.py --vfs /home/user/my_vfs

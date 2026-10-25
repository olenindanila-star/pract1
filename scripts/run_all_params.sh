#!/bin/sh
# Запуск эмулятора со всеми параметрами одновременно.
cd "$(dirname "$0")/.." || exit 1
python3 src/main.py --vfs /home/user/my_vfs --script examples/startup_stage2.txt

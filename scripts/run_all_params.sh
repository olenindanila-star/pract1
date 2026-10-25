#!/bin/sh
# Запуск эмулятора со всеми параметрами одновременно.
cd "$(dirname "$0")/.." || exit 1
python3 src/main.py --vfs vfs/deep.json --script examples/startup_stage3.txt

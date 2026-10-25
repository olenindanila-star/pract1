#!/bin/sh
# Тест: минимальная VFS (пустой корневой каталог).
cd "$(dirname "$0")/.." || exit 1
python3 src/main.py --vfs vfs/minimal.json --script examples/startup_stage3.txt

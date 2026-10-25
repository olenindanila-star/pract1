#!/bin/sh
# Тест: VFS с несколькими файлами (текст и base64).
cd "$(dirname "$0")/.." || exit 1
python3 src/main.py --vfs vfs/several_files.json --script examples/startup_stage3.txt

#!/bin/sh
# Запуск эмулятора с параметром --script (выполнение стартового скрипта).
cd "$(dirname "$0")/.." || exit 1
python3 src/main.py --script examples/startup_stage2.txt

#!/bin/sh
# Запуск с несуществующим стартовым скриптом (проверка обработки ошибки).
cd "$(dirname "$0")/.." || exit 1
python3 src/main.py --script examples/no_such_script.txt

#!/bin/sh
# Тест: ошибки загрузки VFS. Окна открываются по очереди:
# закройте окно (команда exit), чтобы перейти к следующему тесту.
cd "$(dirname "$0")/.." || exit 1
echo "1) Файл VFS не найден"
python3 src/main.py --vfs vfs/no_such_file.json
echo "2) Неверный формат JSON"
python3 src/main.py --vfs vfs/broken.json
echo "3) Неверная структура VFS (неизвестный тип узла)"
python3 src/main.py --vfs vfs/bad_format.json

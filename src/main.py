"""Точка входа: запуск эмулятора командной оболочки с GUI."""

import sys

from config import format_config, parse_args
from gui import EmulatorWindow
from shell import Shell
from vfs import Vfs, VfsError, count_nodes, load_vfs


def prepare_vfs(path):
    """Загрузить VFS и подготовить строки отладочного вывода.

    При ошибке загрузки используется пустая VFS, а ошибка выводится.

    :param path: путь к JSON-файлу VFS или None
    :return: кортеж (объект Vfs, список строк для вывода)
    """
    if not path:
        return Vfs(), ["[DEBUG] VFS не задана, используется пустая VFS"]
    try:
        vfs = load_vfs(path)
    except VfsError as error:
        return Vfs(), [str(error), "[DEBUG] Используется пустая VFS"]
    dirs, files = count_nodes(vfs.root)
    return vfs, [f"[DEBUG] VFS '{vfs.name}' загружена: "
                 f"каталогов {dirs}, файлов {files}"]


def main(argv=None):
    """Разобрать параметры, загрузить VFS и открыть окно эмулятора.

    :param argv: параметры командной строки (None — взять из sys.argv)
    """
    config = parse_args(argv)
    vfs, vfs_lines = prepare_vfs(config.vfs_path)
    debug_lines = format_config(config) + vfs_lines
    for line in debug_lines:
        print(line)
    window = EmulatorWindow(Shell(vfs))
    for line in debug_lines:
        window.write(line)
    if config.script_path:
        window.run_script(config.script_path)
    window.start()


if __name__ == "__main__":
    main(sys.argv[1:])

"""Параметры командной строки эмулятора."""

import argparse
from dataclasses import dataclass


@dataclass
class Config:
    """Настройки эмулятора, заданные при запуске.

    :ivar vfs_path: путь к физическому расположению VFS (или None)
    :ivar script_path: путь к стартовому скрипту (или None)
    """

    vfs_path: str = None
    script_path: str = None


def parse_args(argv=None):
    """Разобрать параметры командной строки.

    :param argv: список параметров (None — взять из sys.argv)
    :return: объект Config
    """
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки UNIX с GUI")
    parser.add_argument("--vfs", dest="vfs_path",
                        help="путь к JSON-файлу VFS")
    parser.add_argument("--script", dest="script_path",
                        help="путь к стартовому скрипту")
    args = parser.parse_args(argv)
    return Config(vfs_path=args.vfs_path, script_path=args.script_path)


def format_config(config):
    """Сформировать отладочный вывод заданных параметров.

    :param config: объект Config
    :return: список строк для вывода
    """
    return [
        "[DEBUG] Параметры запуска:",
        f"[DEBUG]   --vfs    = {config.vfs_path}",
        f"[DEBUG]   --script = {config.script_path}",
    ]

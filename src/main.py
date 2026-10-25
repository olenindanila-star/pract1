"""Точка входа: запуск эмулятора командной оболочки с GUI."""

import sys

from config import format_config, parse_args
from gui import EmulatorWindow
from shell import Shell


def main(argv=None):
    """Разобрать параметры, создать оболочку и открыть окно эмулятора.

    :param argv: параметры командной строки (None — взять из sys.argv)
    """
    config = parse_args(argv)
    debug_lines = format_config(config)
    for line in debug_lines:
        print(line)
    shell = Shell(vfs_name=config.vfs_name())
    window = EmulatorWindow(shell)
    for line in debug_lines:
        window.write(line)
    if config.script_path:
        window.run_script(config.script_path)
    window.start()


if __name__ == "__main__":
    main(sys.argv[1:])

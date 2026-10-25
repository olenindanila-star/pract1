"""Точка входа: запуск эмулятора командной оболочки с GUI."""

from gui import EmulatorWindow
from shell import Shell


def main():
    """Создать оболочку и открыть окно эмулятора."""
    shell = Shell()
    EmulatorWindow(shell).start()


if __name__ == "__main__":
    main()

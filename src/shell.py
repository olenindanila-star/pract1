"""Логика эмулятора командной оболочки (без графического интерфейса)."""

from dataclasses import dataclass

from shell_parser import ParseError, parse_command
from vfs import Vfs, count_nodes, tree_lines


@dataclass
class CommandResult:
    """Результат выполнения одной команды.

    :ivar output: текст, который нужно показать пользователю
    :ivar should_exit: True, если эмулятор нужно закрыть
    """

    output: str = ""
    should_exit: bool = False


class Shell:
    """Эмулятор командной оболочки: принимает строку и выполняет её."""

    def __init__(self, vfs=None):
        """Создать оболочку.

        :param vfs: загруженная VFS (None — пустая VFS по умолчанию)
        """
        self.vfs = vfs if vfs is not None else Vfs()
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
            "vfs-info": self.cmd_vfs_info,
        }

    @property
    def vfs_name(self):
        """Имя текущей VFS."""
        return self.vfs.name

    def prompt(self):
        """Вернуть строку приглашения к вводу, например ``vfs:~$ ``."""
        return f"{self.vfs_name}:~$ "

    def execute(self, line):
        """Разобрать и выполнить строку команды.

        :param line: строка, введённая пользователем
        :return: объект CommandResult с выводом команды
        """
        try:
            words = parse_command(line)
        except ParseError as error:
            return CommandResult(output=str(error))
        if not words:
            return CommandResult()
        name, args = words[0], words[1:]
        handler = self.commands.get(name)
        if handler is None:
            return CommandResult(output=f"{name}: команда не найдена")
        return handler(args)

    def cmd_ls(self, args):
        """Заглушка команды ls: вывести имя команды и аргументы."""
        return CommandResult(output=format_stub("ls", args))

    def cmd_cd(self, args):
        """Заглушка команды cd: вывести имя команды и аргументы."""
        return CommandResult(output=format_stub("cd", args))

    def cmd_vfs_info(self, args):
        """Служебная команда: показать имя, размер и дерево VFS."""
        if args:
            return CommandResult(output="vfs-info: лишние аргументы")
        dirs, files = count_nodes(self.vfs.root)
        lines = [f"VFS: {self.vfs.name}",
                 f"Каталогов: {dirs}, файлов: {files}", "/"]
        lines.extend(tree_lines(self.vfs.root))
        return CommandResult(output="\n".join(lines))

    def cmd_exit(self, args):
        """Завершить работу эмулятора."""
        if args:
            return CommandResult(output="exit: лишние аргументы")
        return CommandResult(output="Выход из эмулятора", should_exit=True)


def format_stub(name, args):
    """Сформировать вывод команды-заглушки.

    :param name: имя команды
    :param args: список аргументов
    :return: строка вида ``ls: аргументы ['a', 'b c']``
    """
    return f"{name}: аргументы {args}"

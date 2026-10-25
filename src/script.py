"""Загрузка стартового скрипта эмулятора."""

COMMENT_CHAR = "#"


class ScriptError(Exception):
    """Ошибка загрузки стартового скрипта."""


def strip_comment(line):
    """Удалить комментарий из строки скрипта.

    Комментарий начинается с символа ``#`` (как в Python), если этот символ
    стоит вне кавычек.

    :param line: строка скрипта
    :return: строка без комментария и без пробелов по краям
    """
    quote = None
    for index, char in enumerate(line):
        if quote:
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
        elif char == COMMENT_CHAR:
            return line[:index].strip()
    return line.strip()


def load_script(path):
    """Прочитать стартовый скрипт и вернуть список команд.

    Пустые строки и строки-комментарии пропускаются.

    :param path: путь к файлу скрипта
    :return: список строк-команд
    :raises ScriptError: если файл не найден или не читается
    """
    try:
        with open(path, encoding="utf-8") as file:
            lines = file.read().splitlines()
    except OSError as error:
        raise ScriptError(
            f"ошибка: не удалось открыть скрипт {path}: {error.strerror}"
        ) from error
    commands = [strip_comment(line) for line in lines]
    return [command for command in commands if command]

"""Тесты разбора строки команды."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from shell_parser import ParseError, parse_command  # noqa: E402


class ParseCommandTest(unittest.TestCase):
    """Проверка функции parse_command."""

    def test_simple_words(self):
        """Слова разделяются пробелами."""
        self.assertEqual(parse_command("ls -l /home"), ["ls", "-l", "/home"])

    def test_double_quotes(self):
        """Аргумент в двойных кавычках — одно слово."""
        self.assertEqual(parse_command('cd "My Folder"'), ["cd", "My Folder"])

    def test_single_quotes(self):
        """Аргумент в одинарных кавычках — одно слово."""
        self.assertEqual(parse_command("ls 'a b' c"), ["ls", "a b", "c"])

    def test_empty_line(self):
        """Пустая строка даёт пустой список."""
        self.assertEqual(parse_command("   "), [])

    def test_unclosed_quote(self):
        """Незакрытая кавычка вызывает ParseError."""
        with self.assertRaises(ParseError):
            parse_command('cd "My Folder')


if __name__ == "__main__":
    unittest.main()

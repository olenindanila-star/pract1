"""Тесты логики эмулятора."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from shell import Shell  # noqa: E402


class ShellTest(unittest.TestCase):
    """Проверка выполнения команд в классе Shell."""

    def setUp(self):
        """Создать новую оболочку перед каждым тестом."""
        self.shell = Shell()

    def test_ls_stub(self):
        """ls выводит своё имя и аргументы."""
        result = self.shell.execute('ls -l "my dir"')
        self.assertEqual(result.output, "ls: аргументы ['-l', 'my dir']")

    def test_cd_stub(self):
        """cd выводит своё имя и аргументы."""
        result = self.shell.execute("cd /home")
        self.assertEqual(result.output, "cd: аргументы ['/home']")

    def test_unknown_command(self):
        """Неизвестная команда даёт сообщение об ошибке."""
        result = self.shell.execute("foo")
        self.assertEqual(result.output, "foo: команда не найдена")

    def test_parse_error(self):
        """Ошибка разбора выводится пользователю."""
        result = self.shell.execute('cd "abc')
        self.assertIn("ошибка разбора", result.output)

    def test_exit(self):
        """exit завершает работу эмулятора."""
        self.assertTrue(self.shell.execute("exit").should_exit)

    def test_exit_with_args(self):
        """exit с аргументами — ошибка, эмулятор не закрывается."""
        result = self.shell.execute("exit 1")
        self.assertFalse(result.should_exit)

    def test_empty_line(self):
        """Пустая строка ничего не выводит."""
        self.assertEqual(self.shell.execute("").output, "")


if __name__ == "__main__":
    unittest.main()

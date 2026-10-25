"""Тесты загрузки стартового скрипта."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from script import ScriptError, load_script, strip_comment  # noqa: E402


class ScriptTest(unittest.TestCase):
    """Проверка strip_comment и load_script."""

    def test_strip_full_line_comment(self):
        """Строка-комментарий становится пустой."""
        self.assertEqual(strip_comment("# comment"), "")

    def test_strip_inline_comment(self):
        """Комментарий в конце строки удаляется."""
        self.assertEqual(strip_comment("ls -l   # list"), "ls -l")

    def test_hash_in_quotes(self):
        """Символ # внутри кавычек не считается комментарием."""
        self.assertEqual(strip_comment('cd "#dir" # c'), 'cd "#dir"')

    def test_load_script(self):
        """Пустые строки и комментарии пропускаются."""
        text = "# header\n\nls\ncd a  # go\n"
        with tempfile.NamedTemporaryFile("w", delete=False,
                                         encoding="utf-8") as file:
            file.write(text)
        try:
            self.assertEqual(load_script(file.name), ["ls", "cd a"])
        finally:
            os.remove(file.name)

    def test_missing_script(self):
        """Несуществующий файл вызывает ScriptError."""
        with self.assertRaises(ScriptError):
            load_script("/no/such/script.txt")


if __name__ == "__main__":
    unittest.main()

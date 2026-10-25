"""Тесты разбора параметров командной строки."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config import format_config, parse_args  # noqa: E402


class ConfigTest(unittest.TestCase):
    """Проверка parse_args и format_config."""

    def test_no_params(self):
        """Без параметров оба пути равны None."""
        config = parse_args([])
        self.assertIsNone(config.vfs_path)
        self.assertIsNone(config.script_path)

    def test_all_params(self):
        """Оба параметра читаются из командной строки."""
        config = parse_args(["--vfs", "/data/my_vfs.json",
                             "--script", "start.txt"])
        self.assertEqual(config.vfs_path, "/data/my_vfs.json")
        self.assertEqual(config.script_path, "start.txt")

    def test_format_config(self):
        """Отладочный вывод содержит оба параметра."""
        lines = format_config(parse_args(["--script", "s.txt"]))
        self.assertIn("[DEBUG]   --script = s.txt", lines)
        self.assertIn("[DEBUG]   --vfs    = None", lines)


if __name__ == "__main__":
    unittest.main()

"""Тесты загрузки виртуальной файловой системы."""

import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))

from vfs import VfsDir, VfsError, count_nodes, load_vfs  # noqa: E402


def vfs_path(name):
    """Вернуть путь к файлу из папки vfs."""
    return os.path.join(ROOT, "vfs", name)


class VfsTest(unittest.TestCase):
    """Проверка load_vfs и count_nodes."""

    def write_temp(self, data):
        """Записать данные во временный JSON-файл и вернуть его путь."""
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                         encoding="utf-8") as file:
            json.dump(data, file)
        self.addCleanup(os.remove, file.name)
        return file.name

    def test_minimal(self):
        """Минимальная VFS: пустой корень."""
        vfs = load_vfs(vfs_path("minimal.json"))
        self.assertEqual(vfs.name, "minimal")
        self.assertEqual(count_nodes(vfs.root), (0, 0))

    def test_several_files(self):
        """Текстовые и base64-файлы загружаются в байты."""
        vfs = load_vfs(vfs_path("several_files.json"))
        files = vfs.root.children
        self.assertEqual(files["readme.txt"].data, b"Hello from VFS!\n")
        self.assertEqual(files["data.bin"].data, bytes(range(8)))

    def test_deep(self):
        """VFS с вложенностью не менее 3 уровней."""
        vfs = load_vfs(vfs_path("deep.json"))
        docs = vfs.root.children["home"].children["user"]
        self.assertIsInstance(docs.children["My Documents"], VfsDir)
        self.assertEqual(count_nodes(vfs.root), (5, 5))

    def test_missing_file(self):
        """Несуществующий файл — ошибка «не найден»."""
        with self.assertRaisesRegex(VfsError, "не найден"):
            load_vfs(vfs_path("no_such_file.json"))

    def test_broken_json(self):
        """Повреждённый JSON — ошибка формата."""
        with self.assertRaisesRegex(VfsError, "неверный формат JSON"):
            load_vfs(vfs_path("broken.json"))

    def test_unknown_node_type(self):
        """Неизвестный тип узла — ошибка."""
        with self.assertRaisesRegex(VfsError, "неизвестный тип"):
            load_vfs(vfs_path("bad_format.json"))

    def test_no_root(self):
        """JSON без root — ошибка."""
        with self.assertRaisesRegex(VfsError, "root"):
            load_vfs(self.write_temp({"name": "x"}))

    def test_bad_base64(self):
        """Неверный base64 — ошибка."""
        data = {"root": {"type": "dir", "children": {
            "a.bin": {"type": "file", "encoding": "base64",
                      "content": "%%%"}}}}
        with self.assertRaisesRegex(VfsError, "base64"):
            load_vfs(self.write_temp(data))

    def test_name_from_file(self):
        """Если имени нет в JSON, берётся имя файла."""
        path = self.write_temp({"root": {"type": "dir"}})
        expected = os.path.splitext(os.path.basename(path))[0]
        self.assertEqual(load_vfs(path).name, expected)

    def test_file_not_modified(self):
        """Загрузка VFS не изменяет исходный файл."""
        path = vfs_path("deep.json")
        with open(path, encoding="utf-8") as file:
            before = file.read()
        load_vfs(path)
        with open(path, encoding="utf-8") as file:
            self.assertEqual(file.read(), before)


if __name__ == "__main__":
    unittest.main()

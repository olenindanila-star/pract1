"""Виртуальная файловая система (VFS), загружаемая из JSON-файла.

Формат JSON::

    {
      "name": "my_vfs",
      "root": {
        "type": "dir",
        "children": {
          "readme.txt": {"type": "file", "content": "текст"},
          "logo.bin": {"type": "file", "encoding": "base64",
                       "content": "AAEC"},
          "docs": {"type": "dir", "children": {}}
        }
      }
    }

Вся VFS хранится только в памяти, исходный файл не изменяется.
"""

import base64
import binascii
import json
import os
from dataclasses import dataclass, field

DEFAULT_VFS_NAME = "vfs"
INDENT = "  "


class VfsError(Exception):
    """Ошибка загрузки VFS."""


@dataclass
class VfsFile:
    """Файл VFS.

    :ivar name: имя файла
    :ivar data: содержимое файла в байтах
    """

    name: str
    data: bytes = b""


@dataclass
class VfsDir:
    """Каталог VFS.

    :ivar name: имя каталога
    :ivar children: словарь «имя → VfsFile или VfsDir»
    """

    name: str
    children: dict = field(default_factory=dict)


@dataclass
class Vfs:
    """Загруженная виртуальная файловая система.

    :ivar name: имя VFS (показывается в заголовке окна)
    :ivar root: корневой каталог
    """

    name: str = DEFAULT_VFS_NAME
    root: VfsDir = field(default_factory=lambda: VfsDir("/"))


def decode_file(name, data):
    """Создать VfsFile из описания в JSON.

    :param name: имя файла
    :param data: словарь с ключами content и (необязательно) encoding
    :return: объект VfsFile
    :raises VfsError: если содержимое имеет неверный формат
    """
    content = data.get("content", "")
    if not isinstance(content, str):
        raise VfsError(f"файл {name}: content должен быть строкой")
    encoding = data.get("encoding", "text")
    if encoding == "text":
        return VfsFile(name, content.encode("utf-8"))
    if encoding == "base64":
        try:
            return VfsFile(name, base64.b64decode(content, validate=True))
        except binascii.Error as error:
            raise VfsError(f"файл {name}: неверный base64") from error
    raise VfsError(f"файл {name}: неизвестная кодировка {encoding}")


def build_node(name, data):
    """Рекурсивно построить узел VFS (файл или каталог) из JSON.

    :param name: имя узла
    :param data: словарь с описанием узла
    :return: объект VfsFile или VfsDir
    :raises VfsError: если описание узла имеет неверный формат
    """
    if not isinstance(data, dict):
        raise VfsError(f"{name}: узел должен быть объектом JSON")
    node_type = data.get("type")
    if node_type == "file":
        return decode_file(name, data)
    if node_type != "dir":
        raise VfsError(f"{name}: неизвестный тип узла {node_type!r}")
    children = data.get("children", {})
    if not isinstance(children, dict):
        raise VfsError(f"{name}: children должен быть объектом JSON")
    directory = VfsDir(name)
    for child_name, child_data in children.items():
        directory.children[child_name] = build_node(child_name, child_data)
    return directory


def read_json(path):
    """Прочитать JSON-файл.

    :param path: путь к файлу
    :return: разобранные данные
    :raises VfsError: если файл не найден или не является JSON
    """
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise VfsError(f"ошибка загрузки VFS: файл {path} не найден") \
            from error
    except json.JSONDecodeError as error:
        raise VfsError(
            f"ошибка загрузки VFS: неверный формат JSON "
            f"(строка {error.lineno})"
        ) from error
    except OSError as error:
        raise VfsError(f"ошибка загрузки VFS: {error.strerror}") from error


def load_vfs(path):
    """Загрузить VFS из JSON-файла в память.

    :param path: путь к JSON-файлу
    :return: объект Vfs
    :raises VfsError: если файл не найден или имеет неверный формат
    """
    data = read_json(path)
    if not isinstance(data, dict) or "root" not in data:
        raise VfsError("ошибка загрузки VFS: нет корневого узла root")
    default_name = os.path.splitext(os.path.basename(path))[0]
    name = data.get("name", default_name)
    try:
        root = build_node("/", data["root"])
    except VfsError as error:
        raise VfsError(f"ошибка загрузки VFS: {error}") from error
    if not isinstance(root, VfsDir):
        raise VfsError("ошибка загрузки VFS: root должен быть каталогом")
    return Vfs(name=str(name), root=root)


def count_nodes(directory):
    """Посчитать каталоги и файлы внутри каталога (рекурсивно).

    :param directory: объект VfsDir
    :return: кортеж (число каталогов, число файлов)
    """
    dirs, files = 0, 0
    for child in directory.children.values():
        if isinstance(child, VfsDir):
            sub_dirs, sub_files = count_nodes(child)
            dirs, files = dirs + 1 + sub_dirs, files + sub_files
        else:
            files += 1
    return dirs, files


def tree_lines(directory, level=1):
    """Сформировать строки дерева каталогов для вывода.

    :param directory: объект VfsDir
    :param level: уровень вложенности (для отступа)
    :return: список строк
    """
    lines = []
    for name in sorted(directory.children):
        child = directory.children[name]
        prefix = INDENT * level
        if isinstance(child, VfsDir):
            lines.append(f"{prefix}{name}/")
            lines.extend(tree_lines(child, level + 1))
        else:
            lines.append(f"{prefix}{name} ({len(child.data)} байт)")
    return lines

"""Графический интерфейс эмулятора на tkinter."""

import tkinter as tk

from script import ScriptError, load_script

WINDOW_SIZE = "800x500"
FONT = ("Courier", 11)
SCRIPT_STEP_MS = 300
CLOSE_DELAY_MS = 500


class EmulatorWindow:
    """Окно эмулятора: область вывода и строка ввода команд."""

    def __init__(self, shell):
        """Создать окно для заданной оболочки.

        :param shell: объект Shell, который выполняет команды
        """
        self.shell = shell
        self.root = tk.Tk()
        self.root.title(f"Эмулятор оболочки — {shell.vfs_name}")
        self.root.geometry(WINDOW_SIZE)
        self.output = tk.Text(self.root, font=FONT, state="disabled",
                              bg="black", fg="white")
        self.output.pack(fill="both", expand=True)
        self.entry = tk.Entry(self.root, font=FONT)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

    def write(self, text):
        """Добавить текст в область вывода."""
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")

    def run_line(self, line):
        """Показать введённую команду, выполнить её и вывести результат.

        :param line: строка команды
        :return: True, если после команды нужно закрыть эмулятор
        """
        self.write(self.shell.prompt() + line)
        result = self.shell.execute(line)
        if result.output:
            self.write(result.output)
        return result.should_exit

    def on_enter(self, _event):
        """Обработать нажатие Enter в строке ввода."""
        line = self.entry.get()
        self.entry.delete(0, "end")
        if self.run_line(line):
            self.close()

    def close(self):
        """Закрыть окно эмулятора с небольшой задержкой."""
        self.root.after(CLOSE_DELAY_MS, self.root.destroy)

    def run_script(self, path):
        """Загрузить стартовый скрипт и выполнить его команды по очереди.

        Каждая команда показывается в окне вместе с выводом, как будто её
        ввёл пользователь.

        :param path: путь к стартовому скрипту
        """
        try:
            commands = load_script(path)
        except ScriptError as error:
            self.write(str(error))
            return
        self.write(f"[DEBUG] Выполнение скрипта {path}")
        self.root.after(SCRIPT_STEP_MS, self.run_next, commands)

    def run_next(self, commands):
        """Выполнить первую команду из списка и запланировать следующую.

        :param commands: оставшиеся команды скрипта
        """
        if not commands:
            self.write("[DEBUG] Скрипт выполнен")
            return
        if self.run_line(commands[0]):
            self.close()
            return
        self.root.after(SCRIPT_STEP_MS, self.run_next, commands[1:])

    def start(self):
        """Запустить главный цикл окна."""
        self.root.mainloop()

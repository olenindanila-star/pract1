"""Графический интерфейс эмулятора на tkinter."""

import tkinter as tk

WINDOW_SIZE = "800x500"
FONT = ("Courier", 11)


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
            self.root.after(500, self.root.destroy)

    def start(self):
        """Запустить главный цикл окна."""
        self.root.mainloop()

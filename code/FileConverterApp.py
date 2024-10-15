import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Listbox
import os


class FileConverterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Converter")

        self.files = []
        self.output_format = "text"
        self.merge_mode = False

        # Кнопка добавления файлов
        self.add_files_button = tk.Button(master, text="Добавить файлы", command=self.add_files)
        self.add_files_button.pack(pady=10)

        # Список выбранных файлов
        self.file_listbox = Listbox(master, width=50, height=10)
        self.file_listbox.pack(pady=10)

        # Кнопка очистки списка файлов
        self.clear_files_button = tk.Button(master, text="Очистить", command=self.clear_files)
        self.clear_files_button.pack(pady=5)

        # Поле для ввода названия выходного файла
        self.output_filename_label = tk.Label(master, text="Введите название выходного файла:")
        self.output_filename_label.pack(pady=5)

        self.output_filename_entry = tk.Entry(master)
        self.output_filename_entry.pack(pady=5)

        # Кнопка выбора формата
        self.format_button = tk.Button(master, text="Выбрать формат", command=self.select_format)
        self.format_button.pack(pady=10)

        # Кнопка выгрузки файлов
        self.output_dir_button = tk.Button(master, text="Выгрузить файлы", command=self.select_output_directory)
        self.output_dir_button.pack(pady=10)

        # Кнопка выбора настроек
        self.settings_button = tk.Button(master, text="Выбрать настройки", command=self.select_settings)
        self.settings_button.pack(pady=10)

        # Кнопка конвертации
        self.convert_button = tk.Button(master, text="Конвертировать", command=self.convert_files)
        self.convert_button.pack(pady=10)

        self.output_directory = ""

    def add_files(self):
        files = filedialog.askopenfilenames(title="Выберите файлы",
                                            filetypes=[("Java files", "*.java"), ("XML files", "*.xml")])
        self.files.extend(files)
        self.update_file_list()

    def clear_files(self):
        self.files.clear()
        self.update_file_list()

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)  # Очистка списка
        for file in self.files:
            self.file_listbox.insert(tk.END, file)  # Добавление файлов в список

    def select_format(self):
        self.output_format = simpledialog.askstring("Выбор формата", "Введите формат файла (например, text):")
        messagebox.showinfo("Формат выбран", f"Выбран формат: {self.output_format}")

    def select_output_directory(self):
        self.output_directory = filedialog.askdirectory(title="Выберите директорию для выгрузки")
        messagebox.showinfo("Директория выбрана", f"Выбрана директория: {self.output_directory}")

    def select_settings(self):
        self.merge_mode = messagebox.askyesno("Настройки", "Объединить текст всех файлов в один файл?")

    def convert_files(self):
        if not self.files or not self.output_directory:
            messagebox.showwarning("Ошибка", "Пожалуйста, добавьте файлы и выберите директорию для выгрузки.")
            return

        output_filename = self.output_filename_entry.get().strip()
        if self.merge_mode and output_filename == "":
            messagebox.showwarning("Ошибка", "Пожалуйста, введите название выходного файла.")
            return

        output_file_path = os.path.join(self.output_directory,
                                        f"{output_filename}.{self.output_format}") if self.merge_mode else os.path.join(
            self.output_directory, f"output.{self.output_format}")

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for file_path in self.files:
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    content = input_file.read()
                    file_name = os.path.basename(file_path)
                    output_file.write(f"{file_name}:\n\n---\n\n{content}\n\n---\n\n")

        messagebox.showinfo("Конвертация завершена", f"Файлы успешно конвертированы в {output_file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()
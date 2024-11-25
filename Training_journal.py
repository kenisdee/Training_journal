"""
Модуль для ведения дневника тренировок с использованием графического интерфейса на основе Tkinter.
"""

import json
import tkinter as tk
from datetime import datetime
from tkinter import ttk, Toplevel, messagebox
from tkcalendar import DateEntry  # Импорт виджета календаря

# Файл для сохранения данных о тренировках
data_file = 'training_log.json'


def load_data():
    """
    Загрузка данных о тренировках из файла.

    Returns:
        list: Список словарей с данными о тренировках.
    """
    try:
        # Попытка открыть файл с данными о тренировках для чтения
        with open(data_file, 'r') as file:
            # Загрузка данных из файла в формате JSON
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не найден или данные в файле некорректны, возвращаем пустой список
        return []


def save_data(data):
    """
    Сохранение данных о тренировках в файл.

    Args:
        data (list): Список словарей с данными о тренировках.
    """
    # Открываем файл для записи данных о тренировках
    with open(data_file, 'w') as file:
        # Сериализуем данные в формат JSON и записываем их в файл с отступами для лучшей читаемости
        json.dump(data, file, indent=4)


class TrainingLogApp:
    """
    Класс для создания графического интерфейса приложения для ведения дневника тренировок.
    """

    def __init__(self, root):
        """
        Инициализация приложения.

        Args:
            root (tk.Tk): Основное окно приложения.
        """
        # Привязка основного окна приложения к атрибуту класса
        self.root = root
        # Установка заголовка окна
        root.title("Дневник тренировок")
        # Создание виджетов для ввода и отображения данных
        self.create_widgets()

    def create_widgets(self):
        """
        Создание виджетов для ввода и отображения данных.
        """
        # Виджеты для ввода данных
        self.exercise_label = ttk.Label(self.root, text="Упражнение:")  # Создание метки для поля "Упражнение"
        self.exercise_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)  # Размещение метки в сетке

        self.exercise_entry = ttk.Entry(self.root)  # Создание поля ввода для "Упражнение"
        self.exercise_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)  # Размещение поля ввода в сетке

        self.weight_label = ttk.Label(self.root, text="Вес:")  # Создание метки для поля "Вес"
        self.weight_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)  # Размещение метки в сетке

        self.weight_entry = ttk.Entry(self.root)  # Создание поля ввода для "Вес"
        self.weight_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)  # Размещение поля ввода в сетке

        self.repetitions_label = ttk.Label(self.root, text="Повторения:")  # Создание метки для поля "Повторения"
        self.repetitions_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)  # Размещение метки в сетке

        self.repetitions_entry = ttk.Entry(self.root)  # Создание поля ввода для "Повторения"
        self.repetitions_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)  # Размещение поля ввода в сетке

        self.add_button = ttk.Button(self.root, text="Добавить запись",
                                     command=self.add_entry)  # Создание кнопки для добавления записи
        self.add_button.grid(column=0, row=3, columnspan=2, pady=10)  # Размещение кнопки в сетке

        self.view_button = ttk.Button(self.root, text="Просмотреть записи",
                                      command=self.view_records)  # Создание кнопки для просмотра записей
        self.view_button.grid(column=0, row=4, columnspan=2, pady=10)  # Размещение кнопки в сетке

        # Виджеты для фильтрации по дате с использованием календаря
        self.start_date_label = ttk.Label(self.root, text="Начальная дата:")
        self.start_date_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)

        self.start_date_entry = DateEntry(self.root, width=12, background='darkblue',
                                          foreground='white', borderwidth=2)  # Создание виджета календаря для начальной даты
        self.start_date_entry.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)  # Размещение виджета календаря в сетке

        self.end_date_label = ttk.Label(self.root, text="Конечная дата:")
        self.end_date_label.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)

        self.end_date_entry = DateEntry(self.root, width=12, background='darkblue',
                                        foreground='white', borderwidth=2)  # Создание виджета календаря для конечной даты
        self.end_date_entry.grid(column=1, row=6, sticky=tk.EW, padx=5, pady=5)  # Размещение виджета календаря в сетке

        self.filter_button = ttk.Button(self.root, text="Применить фильтр",
                                        command=self.view_filtered_records)  # Создание кнопки для применения фильтра
        self.filter_button.grid(column=0, row=7, columnspan=2, pady=10)  # Размещение кнопки в сетке

    def add_entry(self):
        """
        Добавление новой записи о тренировке.
        """
        # Получение текущей даты и времени в формате строки
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Получение значения из поля ввода упражнения
        exercise = self.exercise_entry.get()

        # Получение значения из поля ввода веса
        weight = self.weight_entry.get()

        # Получение значения из поля ввода повторений
        repetitions = self.repetitions_entry.get()

        # Проверка, что все поля заполнены
        if not (exercise and weight and repetitions):
            # Вывод сообщения об ошибке, если хотя бы одно поле не заполнено
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        # Создание словаря с данными о тренировке
        entry = {
            'date': date,
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }

        # Загрузка существующих данных о тренировках
        data = load_data()

        # Добавление новой записи в список данных
        data.append(entry)

        # Сохранение обновленных данных в файл
        save_data(data)

        # Очистка полей ввода после добавления записи
        self.exercise_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)

        # Вывод сообщения об успешном добавлении записи
        messagebox.showinfo("Успешно", "Запись успешно добавлена!")

    def view_records(self):
        """
        Просмотр всех записей о тренировках.
        """
        # Загрузка данных о тренировках
        data = load_data()

        # Создание нового окна для отображения записей
        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")

        # Создание таблицы для отображения данных
        tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")

        # Установка заголовков столбцов
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")

        # Заполнение таблицы данными из загруженных записей
        for entry in data:
            tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))

        # Размещение таблицы в окне с растягиванием на всю доступную область
        tree.pack(expand=True, fill=tk.BOTH)

    def view_filtered_records(self):
        """
        Просмотр записей о тренировках с применением фильтра по дате.
        """
        # Получение значений из полей ввода дат
        start_date_str = self.start_date_entry.get_date().strftime('%Y-%m-%d')
        end_date_str = self.end_date_entry.get_date().strftime('%Y-%m-%d')

        try:
            # Преобразование строк дат в объекты datetime
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте формат гггг-мм-дд.")
            return

        # Загрузка данных о тренировках
        data = load_data()

        # Фильтрация записей по дате
        filtered_data = [entry for entry in data if start_date.date() <= datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S').date() <= end_date.date()]

        # Создание нового окна для отображения отфильтрованных записей
        records_window = Toplevel(self.root)
        records_window.title("Отфильтрованные записи тренировок")

        # Создание таблицы для отображения данных
        tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")

        # Установка заголовков столбцов
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")

        # Заполнение таблицы данными из отфильтрованных записей
        for entry in filtered_data:
            tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))

        # Размещение таблицы в окне с растягиванием на всю доступную область
        tree.pack(expand=True, fill=tk.BOTH)


def main():
    """
    Основная функция для запуска приложения.
    """
    # Создание основного окна приложения
    root = tk.Tk()

    # Создание экземпляра класса TrainingLogApp с передачей ему основного окна
    app = TrainingLogApp(root)

    # Запуск главного цикла обработки событий Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
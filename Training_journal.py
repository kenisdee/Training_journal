"""
Модуль для ведения дневника тренировок с использованием графического интерфейса на основе Tkinter.
"""

import csv
import json
import tkinter as tk
from datetime import datetime
from tkinter import ttk, Toplevel, messagebox, filedialog

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
    with open(data_file, 'w', encoding='utf-8') as file:
        # Сериализуем данные в формат JSON и записываем их в файл с отступами для лучшей читаемости
        json.dump(data, file, indent=4, ensure_ascii=False)


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
        self.add_button.grid(column=0, row=3, pady=10)  # Размещение кнопки в сетке

        self.view_button = ttk.Button(self.root, text="Просмотреть записи",
                                      command=self.view_records)  # Создание кнопки для просмотра записей
        self.view_button.grid(column=1, row=3, pady=10)  # Размещение кнопки в сетке

        # Кнопки для экспорта и импорта данных
        self.export_button = ttk.Button(self.root, text="Экспорт в CSV",
                                        command=self.export_to_csv)  # Создание кнопки для экспорта данных в CSV
        self.export_button.grid(column=0, row=4)  # Размещение кнопки в сетке

        self.import_button = ttk.Button(self.root, text="Импорт из CSV",
                                        command=self.import_from_csv)  # Создание кнопки для импорта данных из CSV
        self.import_button.grid(column=1, row=4)  # Размещение кнопки в сетке

        # Виджеты для фильтрации по дате с использованием календаря
        self.start_date_label = ttk.Label(self.root, text="Начальная дата:")
        self.start_date_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)

        self.start_date_entry = DateEntry(self.root, width=12, background='darkblue',
                                          foreground='white',
                                          borderwidth=2)  # Создание виджета календаря для начальной даты
        self.start_date_entry.grid(column=1, row=5, sticky=tk.EW, padx=5,
                                   pady=5)  # Размещение виджета календаря в сетке

        self.end_date_label = ttk.Label(self.root, text="Конечная дата:")
        self.end_date_label.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)

        self.end_date_entry = DateEntry(self.root, width=12, background='darkblue',
                                        foreground='white',
                                        borderwidth=2)  # Создание виджета календаря для конечной даты
        self.end_date_entry.grid(column=1, row=6, sticky=tk.EW, padx=5, pady=5)  # Размещение виджета календаря в сетке

        # Виджеты для фильтрации по упражнению
        self.exercise_filter_label = ttk.Label(self.root, text="Фильтр по упражнению:")
        self.exercise_filter_label.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)

        self.exercise_filter_entry = ttk.Entry(self.root)  # Создание поля ввода для фильтра по упражнению
        self.exercise_filter_entry.grid(column=1, row=7, sticky=tk.EW, padx=5, pady=5)  # Размещение поля ввода в сетке

        self.filter_button = ttk.Button(self.root, text="Применить фильтр",
                                        command=self.apply_filters)  # Создание кнопки для применения фильтра
        self.filter_button.grid(column=0, row=8, columnspan=2, pady=10)  # Размещение кнопки в сетке

    def add_entry(self):
        """
        Добавление новой записи о тренировке.
        """
        # Получение текущей даты и времени в формате строки
        date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

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

        # Добавление кнопок для редактирования и удаления записей
        edit_button = ttk.Button(records_window, text="Редактировать", command=lambda: self.edit_entry(tree))
        edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = ttk.Button(records_window, text="Удалить", command=lambda: self.delete_entry(tree))
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

    def apply_filters(self):
        """
        Применение фильтров по дате и упражнению.
        """
        # Получение значений из полей ввода дат
        start_date_str = self.start_date_entry.get_date().strftime('%d.%m.%Y')
        end_date_str = self.end_date_entry.get_date().strftime('%d.%m.%Y')

        # Получение значения из поля ввода фильтра по упражнению
        exercise_filter = self.exercise_filter_entry.get()

        # Проверка, что оба поля даты заполнены
        if not (start_date_str and end_date_str):
            messagebox.showerror("Ошибка", "Введите начальную и конечную дату!")
            return

        try:
            # Преобразование строк дат в объекты datetime
            start_date = datetime.strptime(start_date_str, '%d.%m.%Y')
            end_date = datetime.strptime(end_date_str, '%d.%m.%Y')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте формат дд.мм.гггг.")
            return

        # Проверка, что начальная дата не позже конечной даты
        if start_date > end_date:
            messagebox.showerror("Ошибка", "Начальная дата не может быть позже конечной даты!")
            return

        # Загрузка данных о тренировках
        data = load_data()

        # Фильтрация записей по дате и упражнению
        filtered_data = [entry for entry in data if
                         start_date.date() <= datetime.strptime(entry['date'],
                                                                '%d.%m.%Y %H:%M:%S').date() <= end_date.date() and
                         (not exercise_filter or entry['exercise'].lower() == exercise_filter.lower())]

        # Проверка на существование записей, соответствующих фильтру
        if not filtered_data:
            messagebox.showinfo("Информация", "В заданный период упражнения не найдены.")
            return

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

        # Добавление кнопок для редактирования и удаления записей
        edit_button = ttk.Button(records_window, text="Редактировать", command=lambda: self.edit_entry(tree))
        edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = ttk.Button(records_window, text="Удалить", command=lambda: self.delete_entry(tree))
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

    def export_to_csv(self):
        """
        Экспорт данных в CSV файл.
        """
        # Загрузка данных о тренировках
        data = load_data()

        # Открытие диалогового окна для выбора места сохранения файла
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

        if not file_path:
            return

        # Запись данных в CSV файл
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Дата", "Упражнение", "Вес", "Повторения"])  # Запись заголовков столбцов
            for entry in data:
                writer.writerow([entry['date'], entry['exercise'], entry['weight'], entry['repetitions']])

        messagebox.showinfo("Успешно", "Данные успешно экспортированы в CSV файл.")

    def import_from_csv(self):
        """
        Импорт данных из CSV файла.
        """
        # Открытие диалогового окна для выбора файла для импорта
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

        if not file_path:
            return

        # Чтение данных из CSV файла
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Пропуск заголовков столбцов
            data = []
            for row in reader:
                date, exercise, weight, repetitions = row
                data.append({
                    'date': date,
                    'exercise': exercise,
                    'weight': weight,
                    'repetitions': repetitions
                })

        # Сохранение импортированных данных
        save_data(data)

        messagebox.showinfo("Успешно", "Данные успешно импортированы из CSV файла.")

    def edit_entry(self, tree):
        """
        Редактирование выбранной записи.
        """
        # Получение выбранной записи
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите запись для редактирования!")
            return

        # Получение данных выбранной записи
        values = tree.item(selected_item)['values']
        date, exercise, weight, repetitions = values

        # Создание нового окна для редактирования записи
        edit_window = Toplevel(self.root)
        edit_window.title("Редактировать запись")

        # Виджеты для редактирования данных
        ttk.Label(edit_window, text="Упражнение:").grid(row=0, column=0, padx=5, pady=5)
        exercise_entry = ttk.Entry(edit_window)
        exercise_entry.insert(0, exercise)
        exercise_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Вес:").grid(row=1, column=0, padx=5, pady=5)
        weight_entry = ttk.Entry(edit_window)
        weight_entry.insert(0, weight)
        weight_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Повторения:").grid(row=2, column=0, padx=5, pady=5)
        repetitions_entry = ttk.Entry(edit_window)
        repetitions_entry.insert(0, repetitions)
        repetitions_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка для сохранения изменений
        def save_changes():
            new_exercise = exercise_entry.get()
            new_weight = weight_entry.get()
            new_repetitions = repetitions_entry.get()

            if not (new_exercise and new_weight and new_repetitions):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
                return

            # Обновление данных в таблице
            tree.item(selected_item, values=(date, new_exercise, new_weight, new_repetitions))

            # Обновление данных в файле
            data = load_data()
            for entry in data:
                if entry['date'] == date and entry['exercise'] == exercise and entry['weight'] == weight and entry['repetitions'] == repetitions:
                    entry['exercise'] = new_exercise
                    entry['weight'] = new_weight
                    entry['repetitions'] = new_repetitions
                    break
            save_data(data)

            edit_window.destroy()
            messagebox.showinfo("Успешно", "Запись успешно отредактирована!")

        ttk.Button(edit_window, text="Сохранить", command=save_changes).grid(row=3, columnspan=2, pady=10)

    def delete_entry(self, tree):
        """
        Удаление выбранной записи.
        """
        # Получение выбранной записи
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите запись для удаления!")
            return

        # Получение данных выбранной записи
        values = tree.item(selected_item)['values']
        date, exercise, weight, repetitions = values

        # Удаление записи из таблицы
        tree.delete(selected_item)

        # Удаление записи из файла
        data = load_data()
        data = [entry for entry in data if not (entry['date'] == date and entry['exercise'] == exercise and entry['weight'] == weight and entry['repetitions'] == repetitions)]
        save_data(data)

        messagebox.showinfo("Успешно", "Запись успешно удалена!")


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
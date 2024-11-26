"""
Модуль для ведения дневника тренировок с использованием графического интерфейса на основе Tkinter.
"""

import csv
import json
import tkinter as tk
from datetime import datetime
from tkinter import ttk, Toplevel, messagebox, filedialog

# Импорт библиотеки Plotly для создания интерактивных графиков
import plotly.graph_objs as go
import plotly.io as pio
import plotly.subplots as sp
# Импорт виджета календаря
from tkcalendar import DateEntry

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

        # Загрузка уникальных названий упражнений для выпадающего списка
        self.exercise_filter_combobox = ttk.Combobox(self.root, state="readonly")
        self.exercise_filter_combobox.grid(column=1, row=7, sticky=tk.EW, padx=5, pady=5)
        self.update_exercise_filter_combobox()

        self.filter_button = ttk.Button(self.root, text="Отфильтровать и посмотреть записи",
                                        command=self.apply_filters)  # Создание кнопки для применения фильтра
        self.filter_button.grid(column=0, row=8, columnspan=2, pady=10)  # Размещение кнопки в сетке

        # Кнопка для просмотра статистики
        self.stats_button = ttk.Button(self.root, text="Статистика по упражнениям",
                                       command=self.view_exercise_stats)  # Создание кнопки для просмотра статистики
        self.stats_button.grid(column=0, row=9)  # Размещение кнопки в сетке

        # Кнопка для просмотра прогресса
        self.progress_button = ttk.Button(self.root, text="Прогресс по упражнениям",
                                          command=self.view_progress)  # Создание кнопки для просмотра прогресса
        self.progress_button.grid(column=1, row=9)  # Размещение кнопки в сетке

    def update_exercise_filter_combobox(self):
        """
        Обновление выпадающего списка упражнений на основе данных из файла.
        """
        data = load_data()
        exercises = sorted(set(entry['exercise'] for entry in data))
        self.exercise_filter_combobox['values'] = exercises

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

        # Обновление выпадающего списка упражнений
        self.update_exercise_filter_combobox()

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

    def save_table_data(self, tree):
        """
        Сохранение данных из таблицы в файл training_log.json.
        """
        data = []
        for item in tree.get_children():
            values = tree.item(item)['values']
            data.append({
                'date': values[0],
                'exercise': values[1],
                'weight': values[2],
                'repetitions': values[3]
            })

        save_data(data)
        messagebox.showinfo("Успешно", "Данные успешно сохранены!")

    def apply_filters(self):
        """
        Применение фильтров по дате и упражнению.
        """
        # Получение значений из полей ввода дат
        start_date_str = self.start_date_entry.get_date().strftime('%d.%m.%Y')
        end_date_str = self.end_date_entry.get_date().strftime('%d.%m.%Y')

        # Получение значения из поля ввода фильтра по упражнению
        exercise_filter = self.exercise_filter_combobox.get()

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
                try:
                    # Попытка преобразовать дату в формат %d.%m.%Y %H:%M:%S
                    datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                except ValueError:
                    # Если формат даты отличается, приводим его к %d.%m.%Y %H:%M:%S
                    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M:%S')

                data.append({
                    'date': date,
                    'exercise': exercise,
                    'weight': weight,
                    'repetitions': repetitions
                })

        # Сохранение импортированных данных
        save_data(data)

        # Обновление выпадающего списка упражнений
        self.update_exercise_filter_combobox()

        messagebox.showinfo("Успешно", "Данные успешно импортированы из CSV файла.")

    def save_changes(self, tree, edit_window, selected_item, exercise_entry, weight_entry, repetitions_entry):
        """
        Сохранение изменений в выбранной записи.
        """
        new_exercise = exercise_entry.get()
        new_weight = weight_entry.get()
        new_repetitions = repetitions_entry.get()

        if not (new_exercise and new_weight and new_repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        # Обновление данных в таблице
        tree.item(selected_item,
                  values=(tree.item(selected_item)['values'][0], new_exercise, new_weight, new_repetitions))

        # Сохранение изменений в файл
        self.save_table_data(tree)

        edit_window.destroy()
        messagebox.showinfo("Успешно", "Запись успешно отредактирована!")

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
        save_button = ttk.Button(edit_window, text="Сохранить",
                                 command=lambda: self.save_changes(tree, edit_window, selected_item, exercise_entry,
                                                                   weight_entry, repetitions_entry))
        save_button.grid(row=3, columnspan=2, pady=10)

    def delete_entry(self, tree):
        """
        Удаление выбранной записи.
        """
        # Получение выбранной записи
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите запись для удаления!")
            return

        # Удаление записи из таблицы
        tree.delete(selected_item)

        # Сохранение изменений в файл
        self.save_table_data(tree)

        messagebox.showinfo("Успешно", "Запись успешно удалена!")

    def view_exercise_stats(self):
        """
        Просмотр статистики по выполненным упражнениям.
        """
        # Загрузка данных о тренировках
        data = load_data()

        # Словарь для хранения статистики по упражнениям
        stats = {}

        for entry in data:
            exercise = entry['exercise']
            weight = float(entry['weight'])
            repetitions = int(entry['repetitions'])

            if exercise not in stats:
                stats[exercise] = {
                    'total_weight': 0,
                    'total_repetitions': 0,
                    'total_sets': 0,
                    'max_weight': 0,
                    'max_repetitions': 0
                }

            stats[exercise]['total_weight'] += weight * repetitions
            stats[exercise]['total_repetitions'] += repetitions
            stats[exercise]['total_sets'] += 1

            if weight > stats[exercise]['max_weight']:
                stats[exercise]['max_weight'] = weight

            if repetitions > stats[exercise]['max_repetitions']:
                stats[exercise]['max_repetitions'] = repetitions

        # Создание нового окна для отображения статистики
        stats_window = Toplevel(self.root)
        stats_window.title("Статистика по упражнениям")

        # Создание таблицы для отображения данных
        tree = ttk.Treeview(stats_window, columns=("Упражнение", "Всего вес", "Всего повторений", "Всего подходов",
                                                   "Макс. вес", "Макс. повторений"), show="headings")

        # Установка заголовков столбцов
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Всего вес', text="Всего вес")
        tree.heading('Всего повторений', text="Всего повторений")
        tree.heading('Всего подходов', text="Всего подходов")
        tree.heading('Макс. вес', text="Макс. вес")
        tree.heading('Макс. повторений', text="Макс. повторений")

        # Заполнение таблицы данными из статистики
        for exercise, stat in stats.items():
            tree.insert('', tk.END, values=(exercise, stat['total_weight'], stat['total_repetitions'],
                                            stat['total_sets'], stat['max_weight'], stat['max_repetitions']))

        # Размещение таблицы в окне с растягиванием на всю доступную область
        tree.pack(expand=True, fill=tk.BOTH)

    def view_progress(self):
        """
        Просмотр прогресса по выполненным упражнениям.
        """
        # Загрузка данных о тренировках
        data = load_data()

        # Получение значений из полей ввода дат
        start_date_str = self.start_date_entry.get_date().strftime('%d.%m.%Y')
        end_date_str = self.end_date_entry.get_date().strftime('%d.%m.%Y')

        # Получение значения из поля ввода фильтра по упражнению
        exercise_filter = self.exercise_filter_combobox.get()

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

        # Фильтрация записей по дате и упражнению
        filtered_data = [entry for entry in data if
                         start_date.date() <= datetime.strptime(entry['date'],
                                                                '%d.%m.%Y %H:%M:%S').date() <= end_date.date() and
                         (not exercise_filter or entry['exercise'].lower() == exercise_filter.lower())]

        # Проверка на существование записей, соответствующих фильтру
        if not filtered_data:
            messagebox.showinfo("Информация", "В заданный период упражнения не найдены.")
            return

        # Словарь для хранения данных для графика
        progress_data = {}

        for entry in filtered_data:
            exercise = entry['exercise']
            date_time = datetime.strptime(entry['date'], '%d.%m.%Y %H:%M:%S')
            weight = float(entry['weight'])
            repetitions = int(entry['repetitions'])

            if exercise not in progress_data:
                progress_data[exercise] = {'dates': [], 'weights': [], 'repetitions': []}

            progress_data[exercise]['dates'].append(date_time)
            progress_data[exercise]['weights'].append(weight)
            progress_data[exercise]['repetitions'].append(repetitions)

        # Создание нового окна для отображения прогресса
        progress_window = Toplevel(self.root)
        progress_window.title("Прогресс по упражнениям")

        # Создание фигуры для графика
        fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                               subplot_titles=('Вес', 'Повторения'))

        # Отображение графика для каждого упражнения
        for exercise, data in progress_data.items():
            fig.add_trace(
                go.Scatter(x=data['dates'], y=data['weights'], mode='lines+markers', name=f"{exercise} - Вес"),
                row=1, col=1)
            fig.add_trace(go.Scatter(x=data['dates'], y=data['repetitions'], mode='lines+markers',
                                     name=f"{exercise} - Повторения"), row=2, col=1)

        # Настройка графика
        fig.update_layout(title='Прогресс по упражнениям', xaxis_title='Дата и время', yaxis_title='Значение',
                          legend_title='Упражнения', template='plotly_white')

        # Размещение графика в окне
        pio.show(fig, filename='progress_plot.html', auto_open=True)


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

# Дневник тренировок

## Описание

Дневник тренировок — это приложение на основе графического интерфейса (GUI), разработанное с использованием библиотеки
Tkinter в Python. Приложение позволяет пользователям вести учет своих тренировок, добавлять новые записи, просматривать
историю тренировок, фильтровать записи по дате и упражнению, а также экспортировать и импортировать данные в формате
CSV. Кроме того, приложение предоставляет возможность просмотра статистики по упражнениям и отслеживания прогресса с
помощью интерактивных графиков.

## Основные функции

1. **Добавление записи о тренировке:**
    - Пользователь может добавить новую запись о тренировке, указав упражнение, вес и количество повторений.
    - Дата и время автоматически добавляются в запись.

2. **Просмотр записей:**
    - Пользователь может просмотреть все записи о тренировках в табличном формате.
    - Записи сортируются по дате в порядке от последней к первой.

3. **Фильтрация записей:**
    - Пользователь может фильтровать записи по дате и упражнению.
    - Фильтрация осуществляется с помощью виджетов календаря и выпадающего списка упражнений.

4. **Экспорт и импорт данных:**
    - Пользователь может экспортировать данные о тренировках в CSV файл.
    - Пользователь может импортировать данные из CSV файла.

5. **Редактирование и удаление записей:**
    - Пользователь может редактировать и удалять выбранные записи.

6. **Просмотр статистики:**
    - Пользователь может просмотреть статистику по выполненным упражнениям, включая общий вес, общее количество
      повторений, общее количество подходов, максимальный вес и максимальное количество повторений.

7. **Просмотр прогресса:**
    - Пользователь может просмотреть прогресс по выполненным упражнениям с помощью интерактивных графиков, отображающих
      изменение веса и количества повторений во времени.

## Структура проекта

- `Training_journal.py`: Основной файл приложения, содержащий код для создания графического интерфейса и логики работы
  приложения.
- `training_log.json`: Файл для хранения данных о тренировках в формате JSON.

## Используемые библиотеки

- **Tkinter**: Для создания графического интерфейса.
- **tkcalendar**: Для добавления виджета календаря.
- **Plotly**: Для создания интерактивных графиков.
- **CSV**: Для работы с файлами CSV.
- **JSON**: Для работы с файлами JSON.
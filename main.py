'''
Проект "School".. Куспис Н.С, 44ИС-21, Москва, КМПО РАНХиГС.
1.1. Создать базу из 3-х таблиц со связями в SQLite.
1.2. Разрботать консольное приложение, где будут следующие возможности:
    - Просмотр таблиу;
    - Запись данных в таблицы;
    - Удаление записей в таблицах;
    - Экспорт данных в текстовый формат(.txt)

---
Решение. Куспис Н.С.
Начало решения 25.10.2024, 13:20
Окончание решения 26.10.2024, 19:50
Время выполнения: 3:20
'''

from school import School
import os

if __name__ == "__main__":
    # Получаем абсолютный путь к текущему каталогу
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Формируем путь к базе данных relative к текущему каталогу
    db_path = os.path.join(current_directory, 'database', 'school.db')

    school = School(db_path)
    school.display_menu()
    school.close()

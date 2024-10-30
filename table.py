from database import Database

class Table:
    """Базовый класс для таблиц базы данных."""

    def __init__(self, db, table_name, id_column):
        """Инициализация класса Table.

        Args:
            db (Database): Объект базы данных.
            table_name (str): Название таблицы.
            id_column (str): Название колонки идентификатора.
        """
        self.db = db
        self.table_name = table_name
        self.id_column = id_column

    def view(self):
        """Отображает содержимое таблицы."""
        self.db.cursor.execute(f"SELECT * FROM [{self.table_name}]")
        columns = [column[0] for column in self.db.cursor.description]
        print(f"{' | '.join(columns)}")
        print('-' * (len(columns) * 10))

        rows = self.db.cursor.fetchall()
        if rows:
            for row in rows:
                print(' | '.join(str(value).ljust(10) for value in row))
        else:
            print(f"Таблица '{self.table_name}' пуста.")
        print("\n")

    def insert(self):
        """Вставляет данные в таблицу."""
        columns = self.get_columns()
        columns_string = ", ".join(columns)
        print(f"Введите значения для вставки в таблицу '{self.table_name}' ({columns_string}) через запятую:")

        data = input(f"Введите данные: ")
        data_tuple = tuple(value.strip() for value in data.split(","))

        if self.check_id_exists(data_tuple[0]):
            print(f"Запись с таким id ({data_tuple[0]}) уже существует. Повторите попытку.\n")
            return

        placeholders = ', '.join('?' * len(data_tuple))
        self.db.cursor.execute(f"INSERT INTO [{self.table_name}] VALUES ({placeholders})", data_tuple)
        self.db.conn.commit()
        print(f"Данные успешно добавлены в таблицу '{self.table_name}'.\n")

    def delete(self):
        """Удаляет запись из таблицы по идентификатору."""
        identifier = input(f"Введите идентификатор записи для удаления из таблицы '{self.table_name}': ")

        if self.check_id_exists(identifier):
            self.db.cursor.execute(f"DELETE FROM [{self.table_name}] WHERE {self.id_column} = ?", (identifier,))
            self.db.conn.commit()
            print(f"Запись с идентификатором {identifier} успешно удалена из таблицы '{self.table_name}'.\n")
        else:
            print(f"Запись с идентификатором {identifier} не существует, повторите попытку.\n")

    def export_to_txt(self):
        """Экспортирует содержимое таблицы в текстовый файл."""
        self.db.cursor.execute(f"SELECT * FROM [{self.table_name}]")
        rows = self.db.cursor.fetchall()

        if rows:
            with open(f"{self.table_name}.txt", "w", encoding="utf-8") as file:
                columns = [column[0] for column in self.db.cursor.description]
                file.write('\t'.join(columns) + '\n')
                for row in rows:
                    file.write('\t'.join(str(value) for value in row) + '\n')
            print(f"Данные успешно экспортированы в файл {self.table_name}.txt\n")
        else:
            print(f"Таблица '{self.table_name}' пуста, экспорт невозможен.\n")

    def check_id_exists(self, identifier):
        """Проверяет, существует ли запись с данным идентификатором.

        Args:
            identifier (str): Идентификатор записи.

        Returns:
            bool: True, если запись существует, иначе False.
        """
        self.db.cursor.execute(f"SELECT COUNT(1) FROM [{self.table_name}] WHERE {self.id_column} = ?", (identifier,))
        return self.db.cursor.fetchone()[0] > 0

    def get_columns(self):
        """Получает названия колонок таблицы.

        Returns:
            list: Список названий колонок.
        """
        self.db.cursor.execute(f"PRAGMA table_info([{self.table_name}])")
        return [column[1] for column in self.db.cursor.fetchall()]


class Group(Table):
    """Класс для работы с таблицей Group."""

    def __init__(self, db):
        """Инициализация класса Group."""
        super().__init__(db, 'group', 'id_group')

    def __add__(self, other):
        """Добавляет новую группу в таблицу."""
        if isinstance(other, Group):
            # Логика для добавления группы
            print(f"Добавление группы: {other}")
            self.insert()
            return self
        return NotImplemented


class Schedule(Table):
    """Класс для работы с таблицей Schedule."""

    def __init__(self, db):
        """Инициализация класса Schedule.

        Args:
            db (Database): Объект базы данных.
        """
        super().__init__(db, 'schedule', 'id_schedule')


class Student(Table):
    """Класс для работы с таблицей Student."""

    def __init__(self, db):
        """Инициализация класса Student."""
        super().__init__(db, 'student', 'id_student')

    def __eq__(self, other):
        """Сравнивает студентов по id."""
        if isinstance(other, Student):
            return self.id_column == other.id_column
        return NotImplemented

class TableFactory:
    """Фабрика для создания таблиц."""

    @staticmethod
    def create_table(table_name, db):
        if table_name == 'group':
            return Group(db)
        elif table_name == 'schedule':
            return Schedule(db)
        elif table_name == 'student':
            return Student(db)
        else:
            raise ValueError("Неизвестное имя таблицы")

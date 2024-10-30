import sqlite3

class Database:
    """Класс для управления соединением с базой данных SQLite."""

    def __init__(self, db_path):
        """Инициализация класса Database.

        Args:
            db_path (str): Путь к файлу базы данных.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.conn.close()

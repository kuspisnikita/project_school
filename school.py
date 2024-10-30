from table import Group, Schedule, Student, TableFactory
from database import Database

class School:
    """Класс для управления школой и взаимодействия с базой данных."""

    def __init__(self, db_path):
        """Инициализация класса School.

        Args:
            db_path (str): Путь к базе данных.
        """
        self.database = Database(db_path)
        self.group_table = Group(self.database)
        self.schedule_table = Schedule(self.database)
        self.student_table = Student(self.database)

    def display_menu(self):
        """Отображает меню и обрабатывает выбор пользователя."""
        while True:
            print("меню:")
            print("1. показать таблицу Group")
            print("2. показать таблицу Schedule")
            print("3. показать таблицу Student")
            print("4. вставить данные в таблицу Group")
            print("5. вставить данные в таблицу Schedule")
            print("6. вставить данные в таблицу Student")
            print("7. удалить данные из таблицы Group")
            print("8. удалить данные из таблицы Schedule")
            print("9. удалить данные из таблицы Student")
            print("10. экспортировать таблицу в текстовый файл")
            print("0. выйти")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.group_table.view()
            elif choice == "2":
                self.schedule_table.view()
            elif choice == "3":
                self.student_table.view()

            #Применение паттерна Фабрика.
            elif choice in ["4", "5", "6"]:
                table_names = {'4': 'group', '5': 'schedule', '6': 'student'}
                table_name = table_names[choice]
                table = TableFactory.create_table(table_name, self.database)
                table.insert()
            elif choice == "7":
                self.group_table.delete()
            elif choice == "8":
                self.schedule_table.delete()
            elif choice == "9":
                self.student_table.delete()
            elif choice == "10":
                table_name = input("Введите название таблицы для экспорта (group, schedule, student): ")
                if table_name == 'group':
                    self.group_table.export_to_txt()
                elif table_name == 'schedule':
                    self.schedule_table.export_to_txt()
                elif table_name == 'student':
                    self.student_table.export_to_txt()
                else:
                    print("Неверное название таблицы, попробуйте снова.\n")
            elif choice == "0":
                print("Выход из программы.")

                break
            else:
                print("Неверный ввод, попробуйте снова.\n")

    def close(self):
        self.database.close()

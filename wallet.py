import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List, Tuple, Optional

load_dotenv()


@dataclass
class FinanceRecord:
    """Представляет запись в кошельке.

    Атрибуты:
        date (str): Дата записи.
        category (str): Категория записи.
        amount (float): Сумма денег.
        description (str): Описание транзакции.
    """
    date: str
    category: str
    amount: float
    description: str


class FinanceManager:
    """Управление записями в кошельке.

    Аргументы:
        filepath: Путь к файлу, в котором хранятся записи.

    Аттрибуты:
        filepath: Путь к файлу, в котором хранятся записи.
        records: Список записей.

    Методы:
        load_records(): Загружает записи из файла.
        parse_records(): Парсит строки из файла в объекты FinanceRecord.
        save_records(): Сохраняет записи в файл.
        add_record(): Добавляет новую запись.
        edit_record(): Редактирует существующую запись.
        delete_record(): Удаляет запись.
        search_records(): Ищет записи по заданным параметрам.
        calculate_finances(): Вычисляет баланс, общий доход и общие расходы.
    """
    def __init__(self, filepath: str) -> None:
        """Инициализирует экземпляр класса FinanceManager."""
        self.filepath: str = filepath
        self.records: List[FinanceRecord] = self.load_records()

    def load_records(self) -> List[FinanceRecord]:
        """Загружает записи из файла."""
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, 'r') as file:
            content: str = file.read().strip()
            return self.parse_records(content)

    def parse_records(self, content: str) -> List[FinanceRecord]:
        """Парсит строки из файла в объекты FinanceRecord."""
        records: List[FinanceRecord] = []
        entries: List[str] = content.strip().split('---\n')
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            data: dict = {}
            lines: List[str] = entry.split('\n')
            for line in lines:
                line = line.strip()
                if line == "---" or not line:
                    continue
                parts: List[str] = line.split(': ', 1)
                if len(parts) == 2:
                    key, value = parts
                    data[key] = value
                else:
                    print(f'Невозможно разобрать строку: {line}')
            try:
                record = FinanceRecord(
                    date=data['Дата'],
                    category=data['Категория'],
                    amount=float(data['Сумма']),
                    description=data['Описание']
                )
                records.append(record)
            except KeyError as e:
                print(f"Отсутствует ключ в данных: {e}")
            except ValueError as e:
                print(f"Ошибка в типе данных: {e}, в записи: {data}")
        return records

    def save_records(self) -> None:
        """Сохраняет записи в файл."""
        with open(self.filepath, 'w') as file:
            for record in self.records:
                file.write(f'Дата: {record.date}\n')
                file.write(f'Категория: {record.category}\n')
                file.write(f'Сумма: {record.amount}\n')
                file.write(f'Описание: {record.description}\n')
                file.write('---\n')

    def add_record(self, record: FinanceRecord) -> None:
        """Добавляет новую запись."""
        self.records.append(record)
        self.save_records()

    def edit_record(self, index: int, new_record: FinanceRecord) -> None:
        """Редактирует существующую запись."""
        if 0 <= index < len(self.records):
            self.records[index] = new_record
            self.save_records()

    def delete_record(self, index: int) -> None:
        """Удаляет запись."""
        if 0 <= index < len(self.records):
            del self.records[index]
            self.save_records()
        else:
            raise IndexError("Запись с таким индексом не существует.")

    def search_records(
        self,
        category: Optional[str] = None,
        date: Optional[str] = None,
        amount: Optional[float] = None
            ) -> List[FinanceRecord]:
        """Ищет записи по заданным параметрам."""
        result: List[FinanceRecord] = []
        for record in self.records:
            if ((category is None or record.category == category) and
                (date is None or record.date == date) and
                    (amount is None or record.amount == amount)):
                result.append(record)
        return result

    def calculate_finances(self) -> Tuple[float, float, float]:
        """Вычисляет баланс, общий доход и общие расходы."""
        total_income: float = sum(
            record.amount
            for record in self.records
            if record.category == 'Доход'
        )
        total_expense: float = sum(
            record.amount
            for record in self.records
            if record.category == 'Расход'
        )
        balance: float = total_income - total_expense
        return balance, total_income, total_expense


class FinanceCLI:
    """Интерфейс командной строки для управления записями.

    Аттрибуты:
        manager: Менеджер записей.

    Методы:
        run(): Запускает интерфейс командной строки.
        add_record(): Добавляет новую запись.
        edit_record(): Редактирует существующую запись.
        delete_record(): Удаляет запись.
        search_records(): Ищет записи по заданным параметрам.
        view_all_records(): Выводит все записи.
        display_finances(): Выводит информацию о финансовом состоянии.
    """
    def __init__(self, manager: FinanceManager) -> None:
        """Инициализирует интерфейс командной строки с менеджером записей."""
        self.manager: FinanceManager = manager

    def run(self) -> None:
        """Запускает интерфейс командной строки."""
        while True:
            choice: str = input(
                'Введите ваш выбор - число от 1 до 6, где: \n'
                '1 - Добавить запись \n'
                '2 - Изменить запись \n'
                '3 - Удалить запись \n'
                '4 - Найти запись \n'
                '5 - Показать все записи \n'
                '6 - Показать баланс \n'
                '7 - Выйти из программы \n'
                ).strip()
            if choice == '1':
                self.add_record()
            elif choice == '2':
                self.edit_record()
            elif choice == '3':
                self.delete_record()
            elif choice == '4':
                self.search_records()
            elif choice == '5':
                self.view_all_records()
            elif choice == '6':
                self.display_finances()
            elif choice == '7':
                print('Выход из программы')
                break
            else:
                print('Неверный выбор.'
                      'Пожалуйста, выберите один из доступных вариантов.')

    def add_record(self) -> None:
        """Добавляет новую запись."""
        date: str = input('Введите дату в формате гггг-мм-дд: ')
        category: str = input('Введите категорию (Доход/Расход): ')
        amount = float(input('Введите сумму: '))
        description: str = input('Введите описание: ')
        new_record: FinanceRecord = FinanceRecord(
            date,
            category,
            amount,
            description
        )
        self.manager.add_record(new_record)
        print('Запись успешно добавлена.')

    def edit_record(self) -> None:
        """Редактирует существующую запись."""
        self.view_all_records()
        index: int = int(input(
            'Введите номер записи для редактирования: ')
            ) - 1
        date: str = input('Введите новую дату в формате гггг-мм-дд: ')
        category: str = input('Введите новую категорию (Доход/Расход): ')
        amount: float = float(input('Введите новую сумму: '))
        description: str = input('Введите новое описание: ')
        new_record: FinanceRecord = FinanceRecord(
            date,
            category,
            amount,
            description
        )
        self.manager.edit_record(index, new_record)
        print('Запись успешно обновлена.')

    def delete_record(self) -> None:
        """Удаляет запись."""
        self.view_all_records()
        try:
            index: int = int(input('Введите номер записи для удаления: ')) - 1
            self.manager.delete_record(index)
            print('Запись удалена успешно.')
        except IndexError:
            print('Ошибка: Нет записи с таким номером.')
        except ValueError:
            print(
                'Ошибка: Неправильный ввод. '
                'Пожалуйста, введите числовой индекс.')

    def search_records(self) -> None:
        """Ищет записи по заданным параметрам."""
        category: str = input(
            'Введите категорию для поиска (оставьте пустым, если не нужно): ')
        date: str = input(
            'Введите дату для поиска в формате гггг-мм-дд '
            '(оставьте пустым, если не нужно): ')
        amount_input: str = input(
            'Введите сумму для поиска '
            '(оставьте пустым, если не нужно): ')
        amount: Optional[float] = float(amount_input) if amount_input else None
        results = self.manager.search_records(
            category=category if category else None,
            date=date if date else None,
            amount=amount
            )
        if results:
            for record in results:
                print(f"Дата: {record.date}")
                print(f"Категория: {record.category}")
                print(f"Сумма: {record.amount}")
                print(f"Описание: {record.description}")
                print('---')
        else:
            print('Записи не найдены.')

    def view_all_records(self) -> None:
        """Выводит все записи."""
        if self.manager.records:
            for record in self.manager.records:
                print(f"Дата: {record.date}")
                print(f"Категория: {record.category}")
                print(f"Сумма: {record.amount}")
                print(f"Описание: {record.description}")
                print('---')
        else:
            print('Записей пока нет.')

    def display_finances(self) -> None:
        """Выводит информацию о финансовом состоянии."""
        (balance,
         total_income,
         total_expense) = self.manager.calculate_finances()
        print(f'Общий доход: {total_income}')
        print(f'Общие расходы: {total_expense}')
        print(f'Текущий баланс: {balance}')


if __name__ == '__main__':
    path_to_file: str = os.getenv('PATH_TO_FILE')
    manager: FinanceManager = FinanceManager(path_to_file)
    cli: FinanceCLI = FinanceCLI(manager)
    cli.run()

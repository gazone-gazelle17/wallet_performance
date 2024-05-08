# Управление финансовыми записями
## Предварительные требования:
#### Python 3 должен быть установлен на компьютере.
## Установка:
#### Клонирование репозитория.
`git clone https://github.com/gazone-gazelle17/wallet_performance`

`cd crypto_testcase`
#### Активация виртуального окружения.
`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`
#### Настройка переменных окружения.
Создайте файл .env и введите в нем переменную PATH_TO_FILE, в которой будет содержаться адрес расположения файла с записями.
Например, при разработке проекта я использовал такой вид: \n
`PATH_TO_FILE = '/Users/aleksandrgasymov/Dev/wallet/testfile.py'`

#### Запуск скрипта.
`python wallet.py`
## Работа приложения:
#### Начало работы.
После ввода команды `python wallet.py` откроется меню.
Вводите цифру, соответствующую требуемому действию и следуйте дальнейшим инструкциям.

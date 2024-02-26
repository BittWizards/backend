# backend

## Оглавление <a id="contents"></a>
1. [О проекте](#about)
2. [Установка зависимостей](#installation)
3. [Настройка](#setting)
4. [Запуск](#start)


## О проекте <a id="about"></a>
MVP CRM ambassador
## Установка зависимостей<a id="installation"></a>

1. Склонируйте репозиторий на локальную машину и перейдите в него:
  ```
    git clone https://github.com/BittWizards/backend.git
    cd backend
  ```

2. Создайте и активируйте виртуальное окружение
  ```
    python3 -m venv env
    source env/scripts/activate ( Для Windows)
    source env/bin/activate ( Для Linux)
  ```


3. Установите зависимости
  ```
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
```


## Настройка <a id="setting"></a>
4. Настроить pre-commit
  ```
    pre-commit install
  ```
> **Примечание**:
  > Перед каждым коммитом будет запущен линтер и форматтер,
  > который автоматически отформатирует код
  > согласно принятому в команде codestyle.
  > можно запустить pre-commit без коммита, чтоб посмотреть как работает,
  > командой:
    ```
    pre-commit run --all-files
    ```


5. Создайте .env файл
  ```
    touch .env
  ```
7. Заполните по примеру со своими значениями
  [Скопируйте этот файл](.env.example)

## Запуск <a id="start"></a>
<a name="твоё_название"></a>
1. Запустите БД командой:
  ```
    docker-compose -f docker-compose.yml up -d
  ```
2. Запустить проект:

  ```
    python3 manage.py migrate
    python3 manage.py createsuperuser
    python3 manage.py runserver
  ```
3. *Наполните базу данными*:

    Команда для загрузки данных в бд:

    ```sh
    python manage.py loaddata */fixtures/*.json
    ```
    User password: user_test
    Admin password: admin

[Оглавление](#contents)

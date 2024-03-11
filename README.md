# backend

## Оглавление <a id="contents"></a>
1. [О проекте](#about)
2. [Авторы проекта](#authors)
3. [Архив с кодом репозитория и скриншотами](#archive)
4. [Документация](#documentation)
5. [Стек технологий](#tools)
6. [Установка зависимостей](#installation)
7. [Настройка](#setting)
8. [Запуск](#start)
9. [Наполнение БД](#database)
10. [Тесты и покрытие](#tests)
11. [Frontend](#frontend)


## О проекте <a id="about"></a>
MVP CRM ambassador

## Авторы проекта <a id="authors"></a>

Команда:

- Project manager
  - Кравцова Елена

- Product manager
  - Смирнов Алексей

- Business analytics
  - Филимонова Ольга
  - Кашина Елена

- System analytics
  - Карпетис Александр
  - Гогорян Даниил
  - Ольховская Елена

- Designers
  - Каравашкина Александра
  - Каткова Анастасия
  - Храковская Ирина
  - Теплова Полина

- Frontend
  - [Шматенко Наталья](https://github.com/NatashaSolntseva)
  - [Тюлюкин Роман](https://github.com/JayWeee)
  - [Фрикина София](https://github.com/SofiaFrikina)

- Backend
  - [Синюков Алексей](https://github.com/aleksey2299-1)
  - [Дунаева Клавдия](https://github.com/KlavaD)
  - [Дровнин Павел](https://github.com/pashpiter)
  - [Варачев Андрей](https://github.com/Dartanyun)


## Архив с кодом репозитория и скриншотами <a id="archive"></a>

  [ЯндексДиск](https://disk.yandex.ru/d/b80S8N8Itl96Jg)

## Документация <a id="documentation"></a>

Документация сгенерирована автоматически при помощи drf-spectacular.

[Swagger](https://ambassadors.sytes.net/api/docs/#/)

## Стек технологий <a id="tools"></a>

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-%204.2-blue?style=flat&logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DjangoRESTFramework-%203.14.0-blue?style=flat&logo=django)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-%205.3.6-blue?style=flat&logo=celery)](https://docs.celeryq.dev/en/stable/)
[![Redis](https://img.shields.io/badge/Redis-%205.0.1-blue?style=flat&logo=redis)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%2016-blue?style=flat&logo=PostgreSQL)]([https://www.postgresql.org/])
[![Gunicorn](https://img.shields.io/badge/Gunicorn-%2020.1.0-blue?style=flat&logo=gunicorn)](https://gunicorn.org/)
[![drf-spectacular](https://img.shields.io/badge/drf--spectacular-0.27.0-blue)](https://drf-spectacular.readthedocs.io/)
[![django-channels](https://img.shields.io/badge/django--channels-4.0.0-blue)](https://channels.readthedocs.io/)

[![Swagger](https://img.shields.io/badge/Swagger-4A154B?style=for-the-badge&logo=swagger&logoColor=Black)](https://swagger.io/)
[![Docker](https://img.shields.io/badge/Docker-white?style=for-the-badge&logo=docker&logoColor=White)](https://www.docker.com/)
[![DockerCompose](https://img.shields.io/badge/Docker_Compose-34567C?style=for-the-badge&logo=docsdotrs&logoColor=White)](https://docs.docker.com/compose/)
[![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)
[![Certbot](https://img.shields.io/badge/certbot-003A70?style=for-the-badge&logo=letsencrypt&logoColor=white)](https://certbot.eff.org/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/ru)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://docs.github.com/en/actions)

## Установка зависимостей для полного разворачивания проекта<a id="installation"></a>

### В Docker контейнерах

Создайте и перейдите в директорию проекта:

```bash
mkdir ambassadors
cd ambassadors/
```

Скачайте и добавьте файл **docker-compose.production.yml** в директорию.

Cоздайте файл **.env**:

```bash
nano .env
```

Добавьте следующие строки и подставьте свои значения:
````dotenv
POSTGRES_DB=DB                           # название db
POSTGRES_USER=USER                       # имя пользователя для db
POSTGRES_PASSWORD=PASSWORD               # пароль пользователя для db
DB_HOST=db                               # если поменять, то тогда нужно поменять название сервиса в docker-compose.production.yml
DB_PORT=5432                             # это порт для доступа к db
SECRET_KEY=SECRET_KEY                    # SECRET_KEY в настройках django
DEBUG=False                              # режим debug (True или False)
ALLOWED_HOSTS=127.0.0.1 backend          # ваши адреса через пробел (пример:localhost 127.0.0.1 xxxx.com)
GET_CERTS=False                          # True для получения сертификатов (обязательно укажите email в CERTBOT_EMAIL
CERTBOT_EMAIL=example@example.com        # Email для регистрации certbot
DOMAIN=exemple.com                       # Домен на котором вы разворачиваете 
BOT_TOKEN=telegram_bot_token             # Токен телеграм бота, если вы планируете его использовать
USE_SMTP=False                           # использовать ли настоящий сервис по отправке почты, иначе сообщения будут сохранятся внутри контейнера (папка sent_emails)
EMAIL_HOST=EMAIL_HOST                    # сервер вашего email service
EMAIL_PORT=EMAIL_PORT                    # порт для сервера
EMAIL_HOST_USER=EMAIL_HOST_USER          # email с которогу будет осуществлятся рассылка
EMAIL_HOST_PASSWORD=EMAIL_HOST_PASSWORD  # пароль для доступа со стороны стороннего приложения
EMAIL_USE_TLS=False                      # использовать TLS (True или False)
EMAIL_USE_SSL=True                       # использовать SSL (True или False)
````

Установить docker: https://www.docker.com/get-started/

В терминале linux это можно сделать так:
````bash
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin 
````

Запустить Docker в директории с файлом **docker-compose.yaml** (чтобы запустить в фоновом режиме добавьте флаг -d):
````bash
docker compose -f docker-compose.production.yml up
````
В терминале Linux могут потребоваться права суперпользователя:
````bash
sudo docker compose -f docker-compose.production.yml up
````

Для доступа в админ-зону (если вам нужны какие-то данные из бд, или нужно создать объекты) перейдите на страницу http://localhost:8000/admin/:

Логин: `admin@admin.com`

Пароль: `admin`

Для импорта начальных данных воспользуйтесь командой:
````bash
docker compose -f docker-compose.production.yml exec python manage.py fill_db
````

### Локально

1. Склонируйте репозиторий на локальную машину и перейдите в него:

  ```bash
    git clone https://github.com/BittWizards/backend.git
    cd backend
  ```

2. Создайте .env файл:
  ```bash
    touch .env
  ```

3. Заполните по примеру своими значениями:
  [скопируйте этот файл](.env.example)

## Запуск <a id="start"></a>

Запустите контейнеры с проектом следующей командой:
  ```
    docker-compose up -d
  ```
## Наполнение БД <a id="database"></a>

Наполните БД тестовыми данными:

  ```
    docker compose exec backend python manage.py fill_db
  ```

Запущенный проект можно будет посмотреть по [ссылке](http://localhost:8000/).
Посмотреть документацию:
[Swagger](http://localhost:8000/api/docs/)

## Тесты и покрытие <a id="tests"></a>

Запустите тесты в терминале из текущей папки infra:

  ```
    docker compose exec backend python manage.py test
  ```
  или
  ```
    docker compose exec backend coverage run manage.py test
    docker compose exec backend coverage report
  ```

##  Frontend <a id="frontend"></a>

[Ссылка на репозиторий](https://github.com/BittWizards/frontend)

[Оглавление](#contents)

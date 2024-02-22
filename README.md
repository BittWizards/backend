***

### Backend часть командного проекта в рамках Хакатона+ Яндекс Практикум Задача Амбассадоров "03.2024"

***

## Технологии:

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-%204.2-blue?style=flat&logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DjangoRESTFramework-%203.14.0-blue?style=flat&logo=django)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%2016-blue?style=flat&logo=PostgreSQL)]([https://www.postgresql.org/])
[![Gunicorn](https://img.shields.io/badge/Gunicorn-%2020.1.0-blue?style=flat&logo=gunicorn)](https://gunicorn.org/)

[![Swagger](https://img.shields.io/badge/Swagger-68BC71?style=flat&logo=swagger)](https://swagger.io/)
[![Docker](https://img.shields.io/badge/Docker-68BC71?style=flat&logo=docker)](https://www.docker.com/)
[![DockerCompose](https://img.shields.io/badge/Docker_Compose-68BC71?style=flat&logo=docsdotrs)](https://docs.docker.com/compose/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-68BC71?style=flat&logo=githubactions)](https://github.com/features/actions)
[![Nginx](https://img.shields.io/badge/Nginx-68BC71?style=flat&logo=nginx)](https://www.nginx.com/)

***

## Функционал:

В процессе разработки проекта были реализованы:
- интуитивно понятный интерфейс
- удобное хранение и работа с записями в БД

***

## Технические особенности:

Данная инструкция подразумевает, что на вашем локальном/удалённом сервере 
уже установлен Git, Python 3.12, пакетный менеджер pip, Docker, 
Docker Compose, утилита виртуального окружения python3-venv.

В проекте настроена автодокументация с помощью **Swagger**. Для ознакомления 
перейдите по [ссылке]()

С подробными инструкциями запуска вы можете ознакомиться ниже.

***

## Как запустить:

### Если вы хотите иметь возможность поменять код:

Склонируйте репозиторий:
````bash
git clone git@github.com:ALFA-9/Backend.git
````

Cоздайте файл **.env**:

```bash
nano .env
```

Добавьте следующие строки и подставьте свои значения:
````dotenv
POSTGRES_DB=DB                           # название db
POSTGRES_USER=USER                       # имя пользователя для db
POSTGRES_PASSWORD=PASSWORD               # пароль пользователя для db
DB_HOST=db                               # если поменять, то тогда нужно поменять название сервиса в docker-compose.yml
DB_PORT=5432                             # это порт для доступа к db
SECRET_KEY=SECRET_KEY                    # SECRET_KEY в настройках django
DEBUG=False                              # режим debug (True или False)
ALLOWED_HOSTS=127.0.0.1 backend          # ваши адреса через пробел (пример:localhost 127.0.0.1 xxxx.com)
HOST_URL=http://localhost:8000           # ваш url адрес вместе с http/https
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

Перейдите в папку backend и запустите файл **docker-compose.yml**:
````bash
cd backend
docker compose up
````

Если вы хотите прикрутить автоматизацию посредством GithubActions настройте файл **.github/workflows/main.yml**

Для доступа в админ-зону (если вам нужны какие-то данные из бд, или нужно создать объекты) перейдите на страницу http://localhost:8000/admin/:

Логин: `admin`

Пароль: `admin`

> **Примечание.** Любые изменения в коде при сохранении будут немедленно отображаться при запросах к серверу
***

## Авторы

[**Алексей Синюков**](https://github.com/aleksey2299-1)

[**Павел Дровнин**](https://github.com/pashpiter)

[**Клавдия Дунаева**](https://github.com/KlavaD)

[**Андрей Варачев**](https://github.com/Dartanyun)

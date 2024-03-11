# MVP CRM-системы для Амбассадоров Яндекс Практикума.
[Проект](https://ambassadors.sytes.net/)
## Оглавление <a id="contents"></a>
1. [О проекте](#about)
2. [Архив с кодом репозитория и скриншотами](#archive)
3. [Документация](#documentation)
4. [Стек технологий](#tools)
5. [Установка зависимостей](#installation)
6. [Настройка](#setting)
7. [Запуск](#start)
8. [Наполнение БД](#database)
9. [Тесты и покрытие](#tests)
10. [Frontend](#frontend)
11. [Авторы проекта](#authors)


## О проекте <a id="about"></a>
MVP CRM-системы для Амбассадоров Яндекс Практикума.

## Архив с кодом репозитория и скриншотами <a id="archive"></a>

  [Диск](https://drive.google.com/drive/folders/1I5QRQc8Knz1CPwSR6HE3Q9DF2NiDPO0M)

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

1. Создайте и перейдите в директорию проекта:

  ```bash
  mkdir ambassadors
  cd ambassadors/
  ```
  Склонируйте репозиторий на локальную машину и перейдите в него:
  ```bash
      git clone https://github.com/BittWizards/backend.git
      cd backend
  ```
  Если вы хотите запустить на сервере, то:

  Скачайте и добавьте файл **docker-compose.production.yml** в директорию.

2. Создайте .env файл:
  ```bash
    touch .env
  ```

3. Заполните по примеру своими значениями:
  [скопируйте этот файл](.env.example)

## Запуск <a id="start"></a>

[Установить docker](https://www.docker.com/get-started/)

В терминале linux это можно сделать так:
````bash
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin
````

1. Запустите контейнеры с проектом следующей командой:
  ```
    docker compose up -d --build
  ```
На сервере:
  ```bash
  docker compose -f docker-compose.production.yml up
  ```
В терминале Linux могут потребоваться права суперпользователя:
  ```bash
  sudo docker compose -f docker-compose.production.yml up
  ```

2. Для доступа в [админ-зону](http://localhost:8000/admin/):

Логин: `admin@admin.com`

Пароль: `admin`

## Наполнение БД <a id="database"></a>

Для импорта начальных данных воспользуйтесь командой:
  ```
    docker compose exec backend python manage.py fill_db
  ```

Запущенный проект можно будет посмотреть по [ссылке](http://localhost:8000/).
Посмотреть документацию:
[Swagger](http://localhost:8000/api/docs/)

## Тесты и покрытие <a id="tests"></a>

[Проект покрыт тестами на 84%](coverage_html/index.html)

Запустите тесты в терминале из текущей папки:

  ```
    docker compose exec backend run -m pytest
  ```

##  Frontend <a id="frontend"></a>

[Ссылка на репозиторий](https://github.com/BittWizards/frontend)

## Авторы проекта <a id="authors"></a>

- Backend
  - [Синюков Алексей](https://github.com/aleksey2299-1)
  - [Дунаева Клавдия](https://github.com/KlavaD)
  - [Дровнин Павел](https://github.com/pashpiter)
  - [Варачев Андрей](https://github.com/Dartanyun)



[Оглавление](#contents)

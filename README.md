# MVP CRM-системы для Амбассадоров Яндекс Практикума.
[Посмотреть проект можно по ссылке](https://ambassadors.sytes.net/)

## Оглавление <a id="contents"></a>
1. [О проекте](#about)
2. [Архив с кодом репозитория и скриншотами](#archive)
3. [Документация](#documentation)
4. [Стек технологий](#tools)
5. [Функционал](#functional)
6. [Установка зависимостей](#installation)
7. [Запуск](#start)
8. [Наполнение БД](#database)
9. [Telegram бот](#bot)
10. [Тесты и покрытие](#tests)
11. [Авторы проекта](#authors)


## О проекте <a id="about"></a>
MVP CRM-системы для Амбассадоров Яндекс Практикума.

## Архив с кодом репозитория и скриншотами <a id="archive"></a>

  [Диск](https://drive.google.com/drive/folders/1I5QRQc8Knz1CPwSR6HE3Q9DF2NiDPO0M)

## Документация <a id="documentation"></a>

Документация сгенерирована автоматически при помощи drf-spectacular.

[Swagger](https://ambassadors.sytes.net/api/docs/#/)

## Стек технологий <a id="tools"></a>

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-%204.2-blue?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DjangoRESTFramework-%203.14.0-blue?style=for-the-badge&logo=django)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-%205.3.6-blue?style=for-the-badge&logo=celery)](https://docs.celeryq.dev/en/stable/)
[![Redis](https://img.shields.io/badge/Redis-%205.0.1-blue?style=for-the-badge&logo=redis)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%2016-blue?style=for-the-badge&logo=PostgreSQL)]([https://www.postgresql.org/])
[![Gunicorn](https://img.shields.io/badge/Gunicorn-%2020.1.0-blue?style=for-the-badge&logo=gunicorn)](https://gunicorn.org/)
[![drf-spectacular](https://img.shields.io/badge/drf--spectacular-0.27.0-blue?style=for-the-badge)](https://drf-spectacular.readthedocs.io/)
[![django-channels](https://img.shields.io/badge/django--channels-4.0.0-blue?style=for-the-badge)](https://channels.readthedocs.io/)

[![Swagger](https://img.shields.io/badge/Swagger-4A154B?style=for-the-badge&logo=swagger&logoColor=Black)](https://swagger.io/)
[![Docker](https://img.shields.io/badge/Docker-white?style=for-the-badge&logo=docker&logoColor=White)](https://www.docker.com/)
[![DockerCompose](https://img.shields.io/badge/Docker_Compose-34567C?style=for-the-badge&logo=docsdotrs&logoColor=White)](https://docs.docker.com/compose/)
[![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)
[![Certbot](https://img.shields.io/badge/certbot-003A70?style=for-the-badge&logo=letsencrypt&logoColor=white)](https://certbot.eff.org/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/ru)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://docs.github.com/en/actions)

## Функционал<a id="functional"></a>

1. Реализован базовый функционал CRM приложения.
2. Настроена интеграция с Yandex Forms.
3. Добавлена возможность наполнения бд через xlsx файл.
4. Настроен websocket для push уведомлений.
5. Подключен прототип telegram бота.
6. Реализована рассылка через email и telegram.
7. Для рассылки подкючен celery.

Помимо всего прочего для удобства ведения дальнейшей разработки мы использовали аннотацию типов и докстринги.

## Установка зависимостей для полного разворачивания проекта<a id="installation"></a>

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

4. [Установить docker](https://www.docker.com/get-started/)

  В терминале linux это можно сделать так:
  ````bash
    sudo apt update
    sudo apt install curl
    curl -fSL https://get.docker.com -o get-docker.sh
    sudo sh ./get-docker.sh
    sudo apt install docker-compose-plugin
  ````

> **Примечание.** Для запуска на сервере достаточно настроить файл .env и запустить файл docker-compose.production.yml
***

## Запуск <a id="start"></a>

1. Запустите контейнеры с проектом следующей командой (используйте флаг -d для запуска в фоновом режиме):
  ```bash
  docker compose up
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
  ```bash
  docker compose exec backend python manage.py fill_db
  ```

После запуска проект можно будет посмотреть по [ссылке](http://localhost:8000/).

Посмотреть документацию:
[Swagger](http://localhost:8000/api/docs/)

## Telegram bot<a id="bot"></a>

Реализован небольшой функционал чат бота. Добавлено веб приложение для бота.

Для прослушивания уведомлений от telegram api используется webhook.

Чтобы установить вебхук для вашего домена воспользуетесь следующей командой:

```bash
docker compose exec backend python manage.py telegram_webhook -s
```


## Тесты и покрытие <a id="tests"></a>

Покрытие составляет 84 процента.

![Процент покрытия](backend/media/test_coverage.png)

Запустите тесты в терминале из текущей папки:

  ```bash
  docker compose exec backend run -m pytest
  ```

## Авторы проекта <a id="authors"></a>

- [Синюков Алексей](https://github.com/aleksey2299-1)
- [Дунаева Клавдия](https://github.com/KlavaD)
- [Дровнин Павел](https://github.com/pashpiter)
- [Варачев Андрей](https://github.com/Dartanyun)



[Оглавление](#contents)

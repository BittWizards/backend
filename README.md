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

- Product manager
  - Смирнов Алексей

- Project manager
  - Кравцова Елена

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

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.1-green)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.14.0-orange)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.10-blue)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10.24-blue)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/Nginx-alpine-brightgreen)](https://nginx.org/)
[![drf-spectacular](https://img.shields.io/badge/drf--spectacular-0.27.0-blue)](https://drf-spectacular.readthedocs.io/)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## Установка зависимостей для полного разворачивания проекта локально<a id="installation"></a>

1. Склонируйте репозиторий на локальную машину и перейдите в него:

  ```
    git clone https://github.com/BittWizards/backend.git
    cd backend
  ```

2. Перейдите в infra и создайте .env.compose файл:
  ```
    touch .env
  ```

3. Заполните по примеру своими значениями:
  [скопируйте этот файл](.env.example)

## Запуск <a id="start"></a>

Запустите контейнеры с проектом следующей командой:
  ```
    docker-compose -f docker-compose.yml up -d
  ```
## Наполнение БД <a id="database"></a>

Наполните БД тестовыми данными:

  ```
    docker compose exec backend python manage.py fill_db
  ```

Запущенный проект можно будет посмотреть по [ссылке](http://localhost:8080/).
Посмотреть документацию:
[Swagger](http://localhost:8080/api/schema/docs/#/)

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

# NBA Project

## Описание

Данный проект представляет собой веб-приложение, связанное с  баскетбольной ассоциацией, разработанное на Django. Проект предоставляет возможность управлять данными через административную панель и взаимодействовать с различными элементами через интерфейс. Пользователи могут просматривать информацию об игроках, командах матчах. Регистрироваться в качестве игроков и подавать заявки на участие в командах. 

## Установка и запуск

### 1. Клонирование репозитория

Сначала склонируйте репозиторий на локальную машину:

`git clone https://github.com/veselchak431/NBA.git
cd NBA`

### 2. Создание виртуального окружения

Рекомендуется создать виртуальное окружение для установки зависимостей:

`python -m venv venv`

Активируйте виртуальное окружение:

Для Linux/MacOS:

`source venv/bin/activate`

Для Windows:

`venv\Scripts\activate`

### 3. Установка зависимостей

Установите все необходимые зависимости из файла requirements.txt:

`pip install -r requirements.txt`

### 4. Применение миграций базы данных

Примените миграции для настройки базы данных:

`python manage.py migrate`

### 5. Запуск сервера разработки

Запустите локальный сервер разработки:

`python manage.py runserver`

После этого веб-приложение будет доступно по адресу: http://127.0.0.1:8000/.

### 6. Создание суперпользователя (опционально)

Для доступа к административной панели можно создать суперпользователя:

`python manage.py createsuperuser`

Примечания

Убедитесь, что на вашей системе установлен Python версии 3.8 или выше.

Если при установке зависимостей возникают ошибки, проверьте корректность установленной версии pip и обновите её при необходимости:

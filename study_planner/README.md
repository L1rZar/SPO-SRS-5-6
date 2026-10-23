# Учебный планировщик

Учебный Django-проект для СРС № 5. В проекте используются Django Templates, SQLite, Tabler через CDN и JavaScript `fetch()`.

## Запуск в Windows CMD

```bat
py -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py makemigrations planner
python manage.py migrate
python manage.py check
python manage.py runserver
```

Откройте http://127.0.0.1:8000/

Сначала добавьте дисциплины на странице «Дисциплины», затем создайте задания.

## Страницы

- `/` — главная панель
- `/tasks/` — задания
- `/subjects/` — дисциплины

REST API для СРС № 6 в этом проекте намеренно не реализован.

Tabler загружается через CDN, поэтому для его оформления требуется интернет-соединение.

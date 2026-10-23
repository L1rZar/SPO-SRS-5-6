# Учебный планировщик

Учебный Django-проект для СРС № 5 и СРС № 6. В проекте используются Django Templates, SQLite, Tabler через CDN, JavaScript `fetch()` и Django REST Framework.

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

Сначала добавьте дисциплины на странице «Дисциплины», затем создайте задания. Для управления данными через REST API откройте http://127.0.0.1:8000/api-console/.

## Страницы

- `/` — главная панель
- `/tasks/` — список заданий
- `/subjects/` — список дисциплин
- `/api-console/` — интерактивный интерфейс управления через REST API
- `/api/` — корень REST API
- `/api/subjects/` — CRUD для дисциплин
- `/api/tasks/` — CRUD для заданий

## REST API

Для обеих сущностей доступны стандартные операции: `GET` (список и отдельная запись), `POST` (создание), `PUT`/`PATCH` (изменение) и `DELETE` (удаление). Ответы передаются в формате JSON.

Для `/api/tasks/` доступны серверные параметры фильтрации:

- `search` — поиск по названию задания, например `?search=лабораторная`
- `status` — статус: `new`, `in_progress` или `completed`
- `subject` — ID дисциплины
- `due_after` — срок не раньше указанной даты в формате `ГГГГ-ММ-ДД`
- `due_before` — срок не позже указанной даты в формате `ГГГГ-ММ-ДД`
- `ordering` — сортировка: `due_date`, `-due_date`, `title`, `-title`, `status`

Пример комбинированного запроса: `/api/tasks/?status=in_progress&subject=1&due_before=2026-12-31&ordering=due_date`. Параметры фильтрации применяются на сервере к QuerySet Django ORM.

При удалении дисциплины, к которой привязаны задания, API возвращает ошибку, потому что связь модели `Task` с `Subject` настроена с `on_delete=PROTECT`.

Tabler загружается через CDN, поэтому для оформления интерфейса требуется интернет-соединение.

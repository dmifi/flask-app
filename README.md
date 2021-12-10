## REST API на основе Flask

### Подготовка
- Установить Docker
- Установить docker-compose (при необходимости)
- Установить необходимые пакеты (`pip install -r requirements.txt`)
- Отредактировать .env.example (удалить .example и изменить значения при необходимости)
### Запуск
Запустить БД PostgreSQL в контейнере Docker
```
docker-compose up --build -d
```
Подготовить приложение, создать и применить миграции
```
export FLASK_APP=app.py
flask db init
flask db migrate
flask db upgrade
```
Запустить приложение
```
flask run
```

### Документация
Документация по работе с API расположена по адресу http://localhost:5000/docs/
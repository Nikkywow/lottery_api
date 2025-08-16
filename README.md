
# Lottery API

Простое API для лотереи с использованием FastAPI и SQLite. Позволяет создавать тиражи, покупать билеты, определять победителей и просматривать результаты.

## Требования

- Python 3.10+
- Установленные зависимости из requirements.txt

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Nikkywow/lottery_api
cd lottery_api
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск приложения

```bash
uvicorn app.main:app --reload
```

Сервер будет доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Использование API

### 1. Создать новый тираж
```
POST /draws
```
Пример ответа:
```json
{
    "id": 1,
    "status": "open",
    "winning_numbers": null
}
```

### 2. Купить билет
```
POST /tickets
```
Тело запроса:
```json
{
    "numbers": [1, 2, 3, 4, 5],
    "draw_id": 1
}
```
Пример ответа:
```json
{
    "id": 1,
    "draw_id": 1,
    "numbers": [1, 2, 3, 4, 5],
    "is_winner": false
}
```

### 3. Завершить тираж
```
POST /draws/{draw_id}/close
```
Пример ответа:
```json
{
    "id": 1,
    "status": "closed",
    "winning_numbers": [3, 7, 12, 25, 36]
}
```

### 4. Посмотреть результаты
```
GET /draws/{draw_id}/results
```
Пример ответа:
```json
{
    "draw": {
        "id": 1,
        "status": "closed",
        "winning_numbers": [3, 7, 12, 25, 36]
    },
    "tickets": [
        {
            "id": 1,
            "draw_id": 1,
            "numbers": [1, 2, 3, 4, 5],
            "is_winner": false
        }
    ],
    "winning_numbers": [3, 7, 12, 25, 36]
}
```

## Тестирование

### Автоматическая документация
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Примеры запросов
Файл `examples.http` содержит примеры запросов для тестирования.

## Структура проекта
```
lottery_api/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_api.py
├── requirements.txt
├── README.md
└── lottery.db
```

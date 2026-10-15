# Backend для відправки замірів у Telegram
# Простий FastAPI-сервер

## Що робить
Приймає дані заміру + фото, пакує в ZIP і відправляє в Telegram через бота.

## Швидкий старт

### 1. Створіть бота
1. Напишіть @BotFather у Telegram.
2. `/newbot` → отримаєте токен.
3. Додайте бота в потрібний чат/канал і напишіть йому будь-що.
4. Дізнайтесь chat_id:
   - Напишіть боту.
   - Відкрийте `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Знайдіть `"chat":{"id": ...}`

### 2. Локальний запуск
```bash
pip install fastapi uvicorn python-multipart httpx
export TELEGRAM_TOKEN="ваш_токен"
export TELEGRAM_CHAT_ID="ваш_chat_id"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Деплой
Можна задеплоїти на Render / Railway / Fly.io / будь-який VPS.
Встановіть змінні оточення `TELEGRAM_TOKEN` і `TELEGRAM_CHAT_ID`.

### 4. Підключення фронтенду
У `index.html` змініть URL у функції відправки на адресу вашого сервера.

## Безпека
Токен бота тримайте тільки на сервері, ніколи не вставляйте у фронтенд.

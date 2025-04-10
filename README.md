# Snap - B2B Search and Email Service

Snap - это сервис для автоматизированного поиска B2B-поставщиков и управления email-рассылками.

## Функциональность

- 🔍 Поиск поставщиков через Google
- 📧 Извлечение email-адресов с сайтов
- 📨 Управление email-рассылками
- 📊 Анализ результатов поиска
- 🔐 Безопасная аутентификация

## Технологии

- Backend: FastAPI, SQLAlchemy, Celery
- Frontend: React
- База данных: PostgreSQL
- Кэширование: Redis
- Контейнеризация: Docker

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/edwatike/snap.git
cd snap
```

2. Создайте файл .env в корне проекта:
```env
DATABASE_URL=postgresql://user:password@db:5432/snapdb
REDIS_URL=redis://redis:6379/0
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_email@example.com
SMTP_PASSWORD=your_password
```

3. Запустите сервисы через Docker Compose:
```bash
docker-compose up --build
```

4. Откройте в браузере:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API документация: http://localhost:8000/docs

## Структура проекта

```
snap/
├── backend/              # Backend на FastAPI
│   ├── app/
│   │   ├── routers/     # API маршруты
│   │   ├── services/    # Бизнес-логика
│   │   ├── models/      # Модели БД
│   │   ├── schemas/     # Pydantic схемы
│   │   └── db.py        # Настройки БД
├── frontend/            # Frontend на React
│   ├── pages/          # Страницы приложения
│   ├── components/     # React компоненты
│   ├── styles/         # CSS стили
│   └── public/         # Статические файлы
├── parsers/            # Скрипты парсинга
├── emailing/           # Функционал рассылок
└── docker-compose.yml  # Docker конфигурация
```

## API Endpoints

- `POST /api/search` - Запуск поиска поставщиков
- `GET /api/emails` - Получение списка email-адресов
- `POST /api/auth/login` - Аутентификация
- `POST /api/emailing/send` - Отправка рассылки

## Лицензия

MIT

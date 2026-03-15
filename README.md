# ИИ-Эксперт: Платформа диагностики руководителей

Веб-платформа для автоматизированной диагностики компетенций руководителей образовательных организаций с использованием ИИ.

## Структура проекта

```
/workspace
├── backend/                 # FastAPI бэкенд
│   ├── app/
│   │   ├── api/            # API эндпоинты
│   │   ├── core/           # Конфигурация, БД, безопасность
│   │   ├── models/         # SQLAlchemy модели
│   │   ├── schemas/        # Pydantic схемы
│   │   ├── services/       # Бизнес-логика
│   │   └── tasks/          # Celery задачи
│   ├── alembic/            # Миграции БД
│   └── requirements.txt    # Python зависимости
│
└── frontend/               # React фронтенд
    ├── src/
    │   ├── components/     # UI компоненты
    │   ├── pages/          # Страницы приложения
    │   ├── services/       # API клиенты
    │   └── store/          # Zustand store
    └── package.json        # Node.js зависимости
```

## Этап 1: Реализованный функционал

### Бэкенд (FastAPI)

✅ **Модели данных:**
- `Organization` - организации (школы, детсады, доп. образование)
- `Head` - руководители организаций
- `TestSession` - сессии тестирования
- `AdminUser` - администраторы системы
- Модели для настроек ИИ, вопросов, кейсов, аналитики

✅ **API эндпоинты:**
- `POST /api/v1/auth/head/login` - вход руководителя по ИНН
- `GET /api/v1/heads/me` - профиль текущего руководителя
- `PUT /api/v1/heads/me` - обновление профиля
- `POST /api/v1/heads/sessions` - создание сессии тестирования
- `GET /api/v1/heads/sessions` - история сессий
- `POST /api/v1/organizations/upload` - загрузка Excel с организациями
- `GET /api/v1/organizations/` - список организаций

✅ **Инфраструктура:**
- PostgreSQL + SQLAlchemy + Alembic миграции
- JWT аутентификация
- CORS настройка
- Конфигурация через .env

### Фронтенд (React + Material-UI)

✅ **Страницы:**
- `/login` - вход руководителя по ИНН
- `/dashboard` - личный кабинет руководителя
- `/admin/login` - вход администратора
- `/admin` - панель администратора

✅ **Компоненты:**
- Адаптивный дизайн с Material-UI
- Zustand для управления состоянием
- Axios для API запросов
- React Router для навигации

## Быстрый старт

### Бэкенд

```bash
cd backend

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# Установить зависимости
pip install -r requirements.txt

# Скопировать .env.example в .env и настроить
cp .env.example .env

# Запустить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Фронтенд

```bash
cd frontend

# Установить зависимости
npm install

# Запустить dev сервер
npm run dev
```

## Переменные окружения

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_expert_db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
OPENAI_API_KEY=your-openai-api-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## API Документация

После запуска бэкенда документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Следующие этапы

### Этап 2: Административная панель
- Полноценная аутентификация администраторов
- Управление промптами и настройками ИИ
- Справочники и категории

### Этап 3: Генерация вопросов
- Загрузка нормативных документов
- RAG-генерация тестовых вопросов
- Редактирование и публикация вопросов

### Этап 4: Генерация кейсов
- Шаблоны кейсов
- ИИ-генерация сценариев
- Управление базой кейсов

### Этап 5: Тестирование
- Прохождение тестов руководителем
- Сохранение результатов
- Выгрузка PDF отчётов

### Этап 6: Аналитика
- Отчёты и статистика
- Кластеризация руководителей
- Образовательные программы

### Этап 7: Планирование
- Календарь тестирований
- Работа с кандидатами

### Этап 8: Финализация
- Безопасность и валидация
- Нагрузочное тестирование
- Docker контейнеризация
- Документация

## Технологический стек

**Бэкенд:**
- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- Celery + Redis (для фоновых задач)

**Фронтенд:**
- React 18
- TypeScript
- Material-UI
- Zustand
- React Router
- Vite

**ИИ:**
- OpenAI API (или аналоги)
- Sentence Transformers для эмбеддингов

## Лицензия

Проект разработан для образовательных целей.

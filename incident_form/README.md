# Web-форма инцидентов

## Требования

- Python 3.15
- MS SQL Server 15.0.4430.1 (SQL Server 2019)
- ODBC Driver 17 for SQL Server
- Flask 3.0.0

## Установка

### 1. Установка Python-зависимостей

```bash
# Установка Flask и всех зависимостей
pip install -r requirements.txt
```

Или установка Flask отдельно:
```bash
pip install Flask==3.0.0
```

### 2. Установка Flask-WTF (для защиты от CSRF)

```bash
pip install Flask-WTF==1.2.1
```

## Настройка

### 1. Конфигурация через .env файл

Создайте файл `.env` на основе примера:
```bash
cp .env.example .env
```

Отредактируйте `.env`:
```
# Настройки базы данных
SQL_SERVER=localhost          # Адрес SQL Server
SQL_DATABASE=incidents_db     # Имя базы данных
SQL_USER=app_user             # Логин для подключения
SQL_PASSWORD=your_password    # Пароль

# Настройки Flask
FLASK_PORT=5000               # Порт приложения
FLASK_DEBUG=False             # Режим отладки (True/False)
SECRET_KEY=your-secret-key    # Секретный ключ для сессий и CSRF
```

**Важно:** Значение `SECRET_KEY` используется Flask для:
- Защиты сессий пользователей
- Генерации CSRF-токенов (безопасность форм)

Для production обязательно измените SECRET_KEY на случайную строку минимум 16 символов.

### 2. Настройка базы данных

Создайте базу данных и таблицу:
```sql
-- Выполните скрипт database/schema.sql в SQL Server Management Studio
-- или через командную строку:
sqlcmd -S localhost -U app_user -P your_password -i database/schema.sql
```

### 3. Проверка ODBC Driver

Убедитесь, что установлен ODBC Driver 17 for SQL Server:
- **Windows:** Панель управления → Администрирование → Источники данных ODBC (64-bit) → вкладка Драйверы
- Должен быть в списке: "ODBC Driver 17 for SQL Server"

Если отсутствует, скачайте: https://docs.microsoft.com/ru-ru/sql/connect/odbc/download-odbc-driver-for-sql-server

## Запуск

### Режим разработки

```bash
# С включенным режимом отладки
FLASK_DEBUG=True python run.py
```

В режиме разработки Flask автоматически перезагружает приложение при изменении кода и показывает подробные ошибки.

### Режим production

```bash
# Запуск через Waitress WSGI сервер
python run.py
```

Приложение будет доступно по адресу: http://localhost:5000

## Сборка .exe (для Windows Server 2016)

```bash
python build.py
```

Исполняемый файл: `dist/incident_form.exe`

**Запуск как службы Windows:**
```cmd
nssm install IncidentForm "C:\path\to\incident_form.exe"
nssm start IncidentForm
```

## API Endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| GET | / | Форма регистрации |
| POST | /api/incident | Создать инцидент |
| GET | /api/server-time | Серверное время |
| GET | /health | Health check |

## Структура проекта

```
incident_form/
├── app/                    # Flask приложение
│   ├── __init__.py        # Инициализация
│   ├── config.py          # Конфигурация Flask
│   ├── models.py          # Модели БД
│   ├── routes.py          # Маршруты API
│   ├── forms.py           # WTForms валидация
│   └── templates/
│       └── index.html     # HTML шаблон
├── static/                # CSS и JS
├── database/schema.sql    # SQL скрипт
├── .env.example           # Пример конфигурации
├── requirements.txt       # Зависимости Python
├── run.py                 # Точка входа
└── build.py               # Сборка .exe
```

## Настройка Flask (config.py)

Основные параметры Flask находятся в `app/config.py`:

```python
# Порт сервера (переопределяется через .env)
FLASK_PORT = 5000

# Режим отладки
FLASK_DEBUG = False

# Секретный ключ (ОБЯЗАТЕЛЬНО измените для production!)
SECRET_KEY = 'dev-key-change-in-production'

# Строка подключения к MS SQL Server
DATABASE_CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=incidents_db;"
    "UID=app_user;"
    "PWD=password;"
    "TrustServerCertificate=yes;"
)
```

Параметры загружаются из переменных окружения `.env`.

## Логи

Логи сохраняются в папку `logs/`:
- `app.log` — общие логи (ротация 10MB × 5 файлов)
- `sql.log` — SQL-запросы (только в режиме DEBUG)

## Устранение неполадок

### Ошибка: "No module named 'flask'"
```bash
pip install Flask==3.0.0
```

### Ошибка подключения к БД
- Проверьте настройки в `.env`
- Убедитесь, что SQL Server запущен
- Проверьте firewall (порт 1433)

### Ошибка: "ODBC Driver 17 not found"
Установите Microsoft ODBC Driver 17 for SQL Server

### CSRF ошибка при отправке формы
Проверьте, что `SECRET_KEY` установлен в `.env`

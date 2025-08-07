# 💰 Финансовый менеджер - Telegram Bot

Современный Telegram бот с веб-приложением для учета доходов и расходов. Поддерживает множественные кошельки, категории трат, источники дохода и детальную аналитику.

## ✨ Возможности

- 📊 **Учет доходов и расходов** - Добавляйте транзакции с описанием и категоризацией
- 💳 **Множественные кошельки** - Создавайте неограниченное количество кошельков
- 🏷️ **Категории трат** - Настраивайте собственные категории с цветами и иконками
- 💰 **Источники дохода** - Отслеживайте различные источники дохода
- 💱 **Мультивалютность** - Поддержка BYN, RUB, USD
- 📈 **Детальная аналитика** - Графики и отчеты по доходам и расходам
- 📱 **Современный интерфейс** - Красивое и удобное веб-приложение
- 🔒 **Безопасность** - Все данные хранятся локально

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка Telegram бота

1. Создайте бота через [@BotFather](https://t.me/BotFather) в Telegram
2. Получите токен бота
3. Скопируйте файл `env.example` в `.env`:
   ```bash
   cp env.example .env
   ```
4. Отредактируйте `.env` файл:
   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   WEBAPP_URL=https://your-domain.com
   SECRET_KEY=your-secret-key-here
   ```

### 3. Запуск приложения

```bash
python run.py
```

## 📁 Структура проекта

```
finance-bot/
├── bot.py              # Основной файл Telegram бота
├── webapp.py           # Flask веб-приложение
├── models.py           # Модели базы данных
├── database.py         # Работа с базой данных
├── config.py           # Конфигурация
├── run.py              # Запуск приложения
├── requirements.txt    # Зависимости Python
├── templates/          # HTML шаблоны
│   └── index.html      # Главная страница
├── static/             # Статические файлы
│   ├── css/
│   │   └── style.css   # Стили
│   └── js/
│       └── app.js      # JavaScript
└── README.md           # Документация
```

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | Обязательная | По умолчанию |
|------------|----------|--------------|--------------|
| `TELEGRAM_TOKEN` | Токен Telegram бота | ✅ | - |
| `WEBAPP_URL` | URL веб-приложения | ❌ | http://localhost:5000 |
| `SECRET_KEY` | Секретный ключ Flask | ❌ | auto-generated |
| `DATABASE_URL` | URL базы данных | ❌ | sqlite:///finance_bot.db |
| `DEBUG` | Режим отладки | ❌ | False |

### Настройка веб-приложения

Для продакшена рекомендуется:

1. **HTTPS**: Настройте SSL сертификат
2. **Домен**: Укажите реальный домен в `WEBAPP_URL`
3. **Секретный ключ**: Сгенерируйте безопасный `SECRET_KEY`
4. **База данных**: Используйте PostgreSQL или MySQL

## 📱 Использование

### Команды бота

- `/start` - Запустить бота и открыть приложение
- `/menu` - Показать главное меню
- `/help` - Показать справку

### Веб-приложение

После запуска бота:

1. Отправьте `/start` боту
2. Нажмите кнопку "📱 Открыть приложение"
3. Используйте веб-интерфейс для управления финансами

## 🎨 Интерфейс

### Основные разделы

1. **Обзор** - Сводка по балансам и последние транзакции
2. **Транзакции** - Полный список доходов и расходов
3. **Кошельки** - Управление кошельками в разных валютах
4. **Категории** - Настройка категорий расходов
5. **Источники дохода** - Управление источниками дохода
6. **Отчеты** - Аналитика и графики

### Быстрые действия

- Добавление дохода/расхода
- Создание нового кошелька
- Просмотр балансов
- Фильтрация транзакций

## 🗄️ База данных

Приложение использует SQLite по умолчанию. Структура базы данных:

- **users** - Пользователи
- **wallets** - Кошельки
- **income_sources** - Источники дохода
- **expense_categories** - Категории расходов
- **transactions** - Транзакции

## 🔒 Безопасность

- Все данные пользователей изолированы
- Поддержка Telegram WebApp безопасности
- Локальное хранение данных
- Валидация всех входных данных

## 🚀 Развертывание

### Локальное развертывание

```bash
# Клонирование репозитория
git clone <repository-url>
cd finance-bot

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp env.example .env
# Отредактируйте .env файл

# Запуск
python run.py
```

### Продакшен развертывание

1. **Сервер**: Настройте VPS или облачный сервис
2. **Домен**: Настройте домен и SSL
3. **База данных**: Используйте PostgreSQL
4. **Процесс**: Используйте systemd или Docker
5. **Прокси**: Настройте nginx для проксирования

### Docker развертывание

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "run.py"]
```

## 🛠️ Разработка

### Установка для разработки

```bash
# Клонирование
git clone <repository-url>
cd finance-bot

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Настройка
cp env.example .env
# Отредактируйте .env

# Запуск в режиме разработки
export DEBUG=True
python run.py
```

### Структура кода

- **bot.py** - Логика Telegram бота
- **webapp.py** - API и веб-интерфейс
- **models.py** - SQLAlchemy модели
- **database.py** - CRUD операции
- **static/js/app.js** - Фронтенд логика

## 📊 API Endpoints

### Пользователи
- `GET /api/user/{telegram_id}` - Получить пользователя
- `POST /api/user/{telegram_id}` - Создать пользователя
- `PUT /api/user/{telegram_id}/currency` - Обновить валюту

### Кошельки
- `GET /api/user/{telegram_id}/wallets` - Список кошельков
- `POST /api/user/{telegram_id}/wallets` - Создать кошелек
- `DELETE /api/user/{telegram_id}/wallets/{id}` - Удалить кошелек

### Транзакции
- `GET /api/user/{telegram_id}/transactions` - Список транзакций
- `POST /api/user/{telegram_id}/transactions` - Создать транзакцию
- `DELETE /api/user/{telegram_id}/transactions/{id}` - Удалить транзакцию

### Категории
- `GET /api/user/{telegram_id}/expense-categories` - Список категорий
- `POST /api/user/{telegram_id}/expense-categories` - Создать категорию
- `DELETE /api/user/{telegram_id}/expense-categories/{id}` - Удалить категорию

### Источники дохода
- `GET /api/user/{telegram_id}/income-sources` - Список источников
- `POST /api/user/{telegram_id}/income-sources` - Создать источник
- `DELETE /api/user/{telegram_id}/income-sources/{id}` - Удалить источник

### Аналитика
- `GET /api/user/{telegram_id}/summary` - Сводка по финансам

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## 🆘 Поддержка

Если у вас возникли проблемы:

1. Проверьте документацию
2. Создайте Issue в репозитории
3. Опишите проблему подробно

## 🔄 Обновления

Для обновления приложения:

```bash
git pull origin main
pip install -r requirements.txt
python run.py
```

---

**Создано с ❤️ для управления личными финансами** 
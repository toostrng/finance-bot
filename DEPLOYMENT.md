# 🚀 Развертывание на Render

## Подготовка к развертыванию

### 1. Создание GitHub репозитория

1. Создайте новый репозиторий на GitHub
2. Загрузите код в репозиторий:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/finance-bot.git
   git push -u origin main
   ```

### 2. Создание Telegram бота

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Сохраните полученный токен

## Развертывание на Render

### Шаг 1: Регистрация на Render

1. Перейдите на [render.com](https://render.com)
2. Зарегистрируйтесь через GitHub
3. Подтвердите email

### Шаг 2: Создание Web Service

1. В Dashboard нажмите "New +" → "Web Service"
2. Подключите ваш GitHub репозиторий
3. Выберите репозиторий с finance-bot
4. Настройте параметры:

   **Основные настройки:**
   - **Name**: `finance-bot-web`
   - **Environment**: `Python 3`
   - **Region**: Выберите ближайший к вам
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn webapp:app --bind 0.0.0.0:$PORT`

### Шаг 3: Создание базы данных

1. В Dashboard нажмите "New +" → "PostgreSQL"
2. Настройте:
   - **Name**: `finance-bot-db`
   - **Database**: `finance_bot`
   - **User**: `finance_bot_user`
   - **Region**: тот же, что и для web service

### Шаг 4: Настройка переменных окружения

В настройках вашего Web Service добавьте переменные:

1. **TELEGRAM_TOKEN** = ваш токен бота
2. **SECRET_KEY** = случайная строка (например, `my-secret-key-123`)
3. **DATABASE_URL** = скопируйте из настроек PostgreSQL
4. **WEBAPP_URL** = URL вашего web service (будет доступен после деплоя)
5. **DEBUG** = `false`

### Шаг 5: Запуск деплоя

1. Нажмите "Create Web Service"
2. Дождитесь завершения деплоя (5-10 минут)
3. Скопируйте URL вашего приложения

### Шаг 6: Обновление WEBAPP_URL

После получения URL:
1. Перейдите в настройки Web Service
2. Обновите переменную **WEBAPP_URL** на полученный URL
3. Перезапустите сервис

## Локальный запуск бота

После развертывания веб-приложения:

1. Создайте файл `.env`:
   ```env
   TELEGRAM_TOKEN=your_bot_token
   WEBAPP_URL=https://your-app-name.onrender.com
   SECRET_KEY=your_secret_key
   ```

2. Запустите бота:
   ```bash
   python3 run.py
   ```

## Проверка работы

1. Отправьте `/start` вашему боту в Telegram
2. Нажмите кнопку "📱 Открыть приложение"
3. Проверьте, что веб-приложение открывается

## Мониторинг

В Render Dashboard вы можете:
- Просматривать логи приложения
- Мониторить использование ресурсов
- Настраивать автодеплой при изменениях в репозитории

## Устранение проблем

### Ошибка "Build failed"
- Проверьте, что все файлы загружены в репозиторий
- Убедитесь, что `requirements.txt` содержит все зависимости

### Ошибка "Application error"
- Проверьте логи в Render Dashboard
- Убедитесь, что все переменные окружения настроены

### Проблемы с базой данных
- Проверьте, что DATABASE_URL правильно скопирован
- Убедитесь, что база данных создана и доступна

## Обновление приложения

Для обновления:
1. Внесите изменения в код
2. Загрузите в GitHub: `git push origin main`
3. Render автоматически перезапустит приложение

## Стоимость

- **Бесплатный план**: 750 часов в месяц
- **Web Service**: бесплатно
- **PostgreSQL**: бесплатно (до 1GB)

Для постоянной работы рекомендуется перейти на платный план. 
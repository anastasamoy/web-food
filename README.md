🍕 Food Recipes Web Application
Веб-приложение для поиска и сохранения рецептов с возможностью регистрации пользователей и персональной коллекции рецептов.

🚀 Быстрый старт
Предварительные требования
Установленный Docker

Установленный Docker Compose

Запуск приложения (рекомендуемый способ)
Клонируйте репозиторий

git clone <https://github.com/anastasamoy/web-food>
cd web-food
Запустите все сервисы одной командой

docker-compose up
Откройте приложение в браузере

Frontend: http://localhost:3000

Backend API: http://localhost:5000

📁 Структура проекта
web-food/
├── frontend/          # React/Vue фронтенд
├── backend/           # Python/Flask бэкенд
├── docker-compose.yml # Конфигурация Docker
└── README.md
🛠 Команды для работы
🐳 Работа с Docker Compose
Запуск в фоновом режиме:

docker-compose up -d
Остановка всех сервисов:

docker-compose down
Перезапуск с обновлениями (после изменений кода):

docker-compose up --build
Просмотр логов:

# Все логи
docker-compose logs

# Логи конкретного сервиса
docker-compose logs frontend
docker-compose logs backend
Статус контейнеров:

docker-compose ps
🔧 Разработка без Docker

Запуск фронтенда (для разработки):

cd frontend
npm install (установить один раз , дальше просто запускать через npm run dev)
npm run dev

Запуск бэкенда (для разработки):

cd backend
pip install -r requirements.txt
python app.py
🎯 Когда какой способ использовать
🐳 Docker Compose - для повседневного использования
✅ Тестирование готового приложения

✅ Демонстрация проекта

✅ Работа с готовыми фичами

✅ Подготовка к деплою

🔧 Раздельный запуск - для активной разработки
✅ Быстрая горячая перезагрузка фронтенда

✅ Отладка кода в реальном времени

✅ Разработка новых функций

✅ Использование dev-tools браузера

🌐 Доступ к приложению
После запуска приложение доступно по адресам:

Веб-интерфейс: http://localhost:3000

API бэкенда: http://localhost:5000

База данных: PostgreSQL на порту 5432

🔧 Настройка окружения
Переменные окружения бэкенда (.env)

DATABASE_URL=postgresql://user:password@db:5432/recipes_db
SECRET_KEY=your_secret_key
FRONTEND_URL=http://localhost:3000

🐛 Устранение неполадок
Порт уже занят:
docker-compose down
docker-compose up

Ошибки сборки:

docker-compose down
docker system prune -f
docker-compose up --build
Проблемы с базой данных:

bash
docker-compose down
docker volume rm web-food_postgres_data
docker-compose up
📦 Деплой
Для развертывания на сервере:

Скопируйте файлы проекта

Запустите: docker-compose up -d
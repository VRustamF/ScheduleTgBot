# Cовет жоский для бездарей
- ### Если будете че-то менять, то делайте это в отдельной ветке. Это ```БЕСТ ПРАКТИС```, а я буду прововдить `РЕКВЕСТЫ ЖОСКИЕ` потому что я ваш хозяин `ТИМЛИД`

# Инструкция по запуску бота для бездарей

## 1. Шаг: клонирование репозитория
```Shell
git clone https://github.com/VRustamF/ScheduleTgBot.git
```

## 2. Шаг: установка зависимостей 
- ### Для uv
```
uv sync
```
- ### Для pip
```
pip install -r requirements.txt
```
- ### Для poetry
```
poetry install
```

## 3. Шаг: установите и запустите Docker Desktop
https://docs.docker.com/get-started/get-docker/

## 4. Шаг: создайте в папке src файл `.env`
```
# Postgresql
DB__URL=postgresql+asyncpg://admin:schedule@db:5432/schedule_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=schedule
POSTGRES_DB=schedule_db

# Logging
LOG__LEVEL=DEBUG
LOG__FORMAT="[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s"

# Bot
BOT__TOKEN=8088051328:AAHIxywyMjwi7WeKESF7y6ZMBIgUHCAe1Vg

# Redis
REDIS__URL=redis://redis:6379

# RabbitMQ
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=lizaloxx
RABBITMQ__URL=amqp://admin:lizaloxx@rabbitmq:5672/
```

## 5. Шаг: запуск докера
- ### В консоль введите
```
docker compose up -d --build
```

# Что нужно добавить по моему мнению
- ### Чтобы логи выводились в tg канал
- ### Сделать рассписание для преподов

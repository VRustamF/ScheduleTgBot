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
# Zgy
ZGY__URL=https://norvuz.ru/upload/timetable/1-ochnoe.xls

# Logging
LOG__LEVEL=DEBUG
LOG__FORMAT="[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s"

# Bot (токен бота, которого я отправлял вчера, желательно поменять)
BOT__TOKEN=8088051328:AAHIxywyMjwi7WeKESF7y6ZMBIgUHCAe1Vg 

# Redis
REDIS__URL=redis://localhost:6379
```

## 5. Шаг: запуск докера
- ### В консоль введите
```
docker compose up -d
```

## 6. Шаг: создание расписания
- ### Запустите функцию `parser()` в `src/parser/parser_from_xlsx.py/`

## 7. Шаг: запуск бота
- ### Запустите `main` файл в `src/bot/main.py/`

# Что нужно добавить по моему мнению
- ### Считывать все файлв расписаний с сайта (Макс)
- ### Автоматически парсить данные каждые 10 минут (Некит, если не хочет, то тоже Макс)
- ### Чтобы логи выводились в tg канал (Дима)
- ### Перенести всё в бд (Я)
- ### Сделать рассписание для преподов (Я наверное)

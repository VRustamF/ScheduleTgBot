# Сборка на основе Ubuntu Noble
FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Создаем рабочую директорию
WORKDIR /app

# 1. Копируем файл зависимостей
COPY pyproject.toml uv.lock ./

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# 2. Устанавливаем зависимости (кэшируемый слой)
RUN uv sync --locked --no-dev

# 3. Копируем остальной код
COPY src ./
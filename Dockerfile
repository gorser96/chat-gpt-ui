# Используем официальный базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем libpq-dev
RUN apt-get update \
    && apt-get -y install libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt в рабочую директорию
COPY requirements.txt .

RUN pip install --upgrade pip
# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое текущей директории в рабочую директорию контейнера
COPY . .

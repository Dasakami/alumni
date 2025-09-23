# Используем официальный Python
FROM python:3.12-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и ставим зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Применяем миграции, собираем статику (при старте сделаем через entrypoint)
CMD ["gunicorn", "alumni.wsgi:application", "--bind", "0.0.0.0:8000"]

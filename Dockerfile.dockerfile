FROM python:3.9-alpine

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения
COPY src/ /app/src/
COPY config.json /app/
COPY manifest.json /app/
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаем симлинки как в оригинальном образе
RUN ln -sf /app /addon

# Запускаем приложение
CMD ["python", "/app/src/main.py"]
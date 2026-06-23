# 1. Базовый образ с Python 3.11 на базе облегченного Linux
FROM python:3.11-slim

# 2. Установка системных утилит для сборки OpenCV и dlib внутри Linux
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Настройка рабочей директории внутри контейнера
WORKDIR /app

# 4. Копирование всех файлов проекта внутрь образа
COPY . /app

# 5. Установка зависимостей
RUN pip install --no-cache-dir dlib-bin face_recognition Pillow

# 6. Чистый запуск тестов без всяких виртуальных серверов
CMD ["python", "test_recognize.py"]
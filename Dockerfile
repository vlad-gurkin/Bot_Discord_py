# syntax=docker/dockerfile:1.7

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# -------------------------------
# 1️⃣ Системные зависимости
# -------------------------------
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# -------------------------------
# 2️⃣ Python зависимости
# -------------------------------
FROM base AS deps

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# -------------------------------
# 3️⃣ Финальный образ
# -------------------------------
FROM base AS runtime

# Копируем ТОЛЬКО установленные пакеты
COPY --from=deps /usr/local /usr/local

# Копируем код ПОСЛЕДНИМ
COPY . .

CMD ["python", "main.py"]

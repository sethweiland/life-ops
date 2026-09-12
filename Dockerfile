# Production Dockerfile for the life-ops Flask shell
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD gunicorn -b 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120 wsgi:app

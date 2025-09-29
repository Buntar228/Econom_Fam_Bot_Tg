FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       wget \
       gnupg \
       unzip \
       curl \
       chromium \
       chromium-driver \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "main.py"]

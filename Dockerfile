
FROM python:3.10-slim-bookworm

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    musl-dev \
    ffmpeg \
    aria2 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir pytube

ENV COOKIES_FILE_PATH="youtube_cookies.txt"

CMD ["sh", "-c", "gunicorn app:app & python3 main.py"]

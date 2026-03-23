FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    espeak ffmpeg portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["gunicorn", "-k", "eventlet", "-w", "1", "app:app"]

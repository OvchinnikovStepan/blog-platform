FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m celery

COPY . .

RUN chown -R celery:celery /app

USER celery

CMD ["celery", "-A", "celery_app:celery_app", "worker", "-Q","preview.queue","--loglevel=info"]

from celery import Celery

app = Celery("moderation_worker")

app.config_from_object("shared.celery.config")

from celery import Celery

app = Celery("preview_worker")

app.config_from_object("shared.celery.config")

from celery import Celery

app = Celery("publish_worker")

app.config_from_object("shared.celery.config")

from .celery_app import app
from shared.celery.tasks import MODERATE_POST

def send_to_moderation(**kwargs):
    app.send_task(
        MODERATE_POST,
        kwargs=kwargs,
    )

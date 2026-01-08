import logging
import requests
import os
from celery_app import celery_app

BACKEND_URL = os.getenv("BACKEND_INTERNAL_URL")
DLQ_TOKEN = os.getenv("INTERNAL_DLQ_TOKEN")

HEADERS = {
    "Authorization": f"Token {DLQ_TOKEN}",
    "Content-Type": "application/json",
}

@celery_app.task(name="dlq.handle")
def handle_dlq(task_name: str, post_id: int, reason: str):
    logging.error(
        "DLQ received task=%s post_id=%s reason=%s",
        task_name,
        post_id,
        reason,
    )

    if task_name == "post.moderate":
        compensate_reject(post_id)

    elif task_name == "post.generate_preview":
        compensate_error(post_id)

    elif task_name == "post.publish":
        compensate_error(post_id)

    elif task_name == "post.notify":
        logging.warning("Notification failed, skipping compensation")

    else:
        logging.warning("Unknown task in DLQ: %s", task_name)


def compensate_reject(post_id: int):
    requests.post(
        f"{BACKEND_URL}/articles/{post_id}/reject",
        headers=HEADERS,
        timeout=5,
    )


def compensate_error(post_id: int):
    requests.post(
        f"{BACKEND_URL}/internal/posts/{post_id}/error",
        headers=HEADERS,
        timeout=5,
    )

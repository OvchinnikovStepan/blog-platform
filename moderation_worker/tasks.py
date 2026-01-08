import random
import requests
import logging
import os
from shared.celery.tasks import GENERATE_PREVIEW, MODERATE_POST
from .celery_app import app
from celery_app import celery_app

logging.basicConfig(level=logging.INFO)

BACKEND_INTERNAL_URL = os.getenv("BACKEND_INTERNAL_URL")
MODERATION_INTERNAL_TOKEN = os.getenv("MODERATION_INTERNAL_TOKEN")

if not BACKEND_INTERNAL_URL or not MODERATION_INTERNAL_TOKEN:
    raise RuntimeError("Internal backend URL or moderation token is not set")

@app.task(
    name=MODERATE_POST,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 10},
)
def moderate_post(
    self,
    post_id: int,
    author_id: int,
    requested_by: int,
    title: str,
    body: str,
    **_
):
    logging.info("Moderating post %s", post_id)

    try:
        # 70% approve, 30% reject
        approved = random.random() > 0.3

        headers = {
            "Authorization": f"Token {MODERATION_INTERNAL_TOKEN}",
            "Content-Type": "application/json",
        }

        if not approved:
            logging.info("Post %s rejected by moderation", post_id)

            resp = requests.post(
                f"{BACKEND_INTERNAL_URL}/internal/articles/{post_id}/reject",
                headers=headers,
                timeout=5,
            )
            resp.raise_for_status()
            return "rejected"

        logging.info("Post %s approved, sending to preview")

        celery_app.send_task(
            GENERATE_PREVIEW,
            kwargs={
                "post_id": post_id,
                "author_id": author_id,
                "title": title,
                "body": body,
            },
        )

        return "approved"
    
    except Exception as e:

        if self.request.retries >= 5:
            celery_app.send_task(
                "dlq.handle",
                kwargs={
                    "task_name": "post.moderate",
                    "post_id": post_id,
                    "reason": str(e),
                },
                queue="dlq",
            )
            logging.error("post.moderate sent to DLQ, post_id=%s", post_id)
            return

        raise




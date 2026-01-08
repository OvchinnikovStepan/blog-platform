import logging
import os
import requests

from .celery_app import app
from shared.celery.tasks import GENERATE_PREVIEW,PUBLISH_POST

logging.basicConfig(level=logging.INFO)

BACKEND_INTERNAL_URL = os.getenv("BACKEND_INTERNAL_URL")
PREVIEW_INTERNAL_TOKEN = os.getenv("PREVIEW_INTERNAL_TOKEN")

if not BACKEND_INTERNAL_URL or not PREVIEW_INTERNAL_TOKEN:
    raise RuntimeError("Preview worker env vars are not set")

HARDCODED_PREVIEW_URL = "https://placehold.co/600x400?text=Preview"

@app.task(
    name=GENERATE_PREVIEW,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 10},
)
def generate_preview(
    self,
    post_id: int,
    author_id: int,
    title: str,
    body: str,
):
    logging.info("Generating preview for post %s", post_id)

    try:
        headers = {
            "Authorization": f"Token {PREVIEW_INTERNAL_TOKEN}",
            "Content-Type": "application/json",
        }

        resp = requests.put(
            f"{BACKEND_INTERNAL_URL}/internal/articles/{post_id}/preview",
            json={"preview_url": HARDCODED_PREVIEW_URL},
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()

        logging.info("Preview generated for post %s", post_id)

        app.send_task(
            PUBLISH_POST,
            kwargs={"post_id": post_id, "author_id": author_id, "post_title":title},
        )

        return "preview_generated"

    except Exception as e:

        if self.request.retries >= 5:
            app.send_task(
                "dlq.handle",
                kwargs={
                    "task_name": "post.preview",
                    "post_id": post_id,
                    "reason": str(e),
                },
                queue="dlq",
            )
            logging.error("post.moderate sent to DLQ, post_id=%s", post_id)
            return

        raise

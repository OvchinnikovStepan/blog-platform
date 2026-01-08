import logging
import os
import requests

from .celery_app import app
from shared.celery.tasks import PUBLISH_POST,NOTIFY_FOLLOWERS
logging.basicConfig(level=logging.INFO)

BACKEND_INTERNAL_URL = os.getenv("BACKEND_INTERNAL_URL")
PUBLISH_INTERNAL_TOKEN = os.getenv("PUBLISH_INTERNAL_TOKEN")

if not BACKEND_INTERNAL_URL or not PUBLISH_INTERNAL_TOKEN:
    raise RuntimeError("Publish worker env vars are not set")

@app.task(
    name=PUBLISH_POST,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5},
)
def publish_post(self, 
    post_id: int,
    author_id: int,
    title: str):

    try:
            
        logging.info("Publishing post %s", post_id)

        headers = {
            "Authorization": f"Token {PUBLISH_INTERNAL_TOKEN}",
            "Content-Type": "application/json",
        }

        resp = requests.put(
            f"{BACKEND_INTERNAL_URL}/internal/articles/{post_id}/complete_publish",
            headers=headers,
            timeout=5,
        )

        resp.raise_for_status()

        logging.info("Post %s published successfully", post_id)

        app.send_task(
            NOTIFY_FOLLOWERS,
            kwargs={"post_id": post_id,"author_id":author_id,"post_title":title},
        )

        return "published"
    
    except Exception as e:

        if self.request.retries >= 5:
            app.send_task(
                "dlq.handle",
                kwargs={
                    "task_name": "post.publish",
                    "post_id": post_id,
                    "reason": str(e),
                },
                queue="dlq",
            )
            logging.error("post.moderate sent to DLQ, post_id=%s", post_id)
            return

        raise

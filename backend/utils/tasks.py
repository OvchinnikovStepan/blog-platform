from celery_app import celery_app

@celery_app.task(name="notify_followers", bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5})
def notify_followers(self, author_id: int, post_id: int, post_title:str):
    return {"author_id": author_id, "post_id": post_id, "post_title":post_title}

from celery_app import celery_app

def notify_followers(author_id: int, post_id: int):
    celery_app.send_task(
        'tasks.notify_followers',
        args=[author_id, post_id]
    )

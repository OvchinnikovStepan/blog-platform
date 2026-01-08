import logging
import requests
from celery_app import celery_app
from config import USERS_DATABASE_URL, POSTS_DATABASE_URL, PUSH_URL
from db.base import create_session
from repositories.users_repo import UsersRepository

UsersSession = create_session(USERS_DATABASE_URL)
PostsSession = create_session(POSTS_DATABASE_URL)

@celery_app.task(
    name="notify_followers",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def notify_followers(self, author_id: int, post_id: int, post_title: str):
    users_db = UsersSession()

    try:
        users_repo = UsersRepository(users_db)

        subs = users_repo.get_subscribers_with_keys(author_id)

        for sub in subs:
            if not sub.subscription_key:
                logging.warning("No subscription_key for %s", sub.subscriber_id)
                continue

            requests.post(
                PUSH_URL,
                headers={
                    "Authorization": f"Bearer {sub.subscription_key}",
                    "Content-Type": "application/json",
                },
                json={"message": f"Пользователь {author_id} выпустил новый пост: {post_title[:10]}..."},
                timeout=5,
        ).raise_for_status()

    finally:
        users_db.close()

from sqlalchemy import select
from db.users import users, subscribers

class UsersRepository:
    def __init__(self, session):
        self.session = session

    def get_subscribers_with_keys(self, author_id: int):
        stmt = (
            select(
                subscribers.c.subscriber_id,
                users.c.subscription_key,
            )
            .join(users, users.c.id == subscribers.c.subscriber_id)
            .where(subscribers.c.author_id == author_id)
        )
        return self.session.execute(stmt).all()

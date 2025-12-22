from sqlalchemy import select
from db.posts import posts

class PostsRepository:
    def __init__(self, session):
        self.session = session

    def get_post(self, post_id: int):
        stmt = select(posts).where(posts.c.id == post_id)
        return self.session.execute(stmt).first()

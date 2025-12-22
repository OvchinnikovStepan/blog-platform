import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
PUSH_URL = os.getenv("PUSH_URL")

USERS_DATABASE_URL = os.getenv("USERS_DATABASE_URL")
POSTS_DATABASE_URL = os.getenv("DATABASE_URL")

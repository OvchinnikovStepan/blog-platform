from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("subscription_key", String),
)

subscribers = Table(
    "subscribers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("subscriber_id", Integer, ForeignKey("users.id")),
    Column("author_id", Integer, ForeignKey("users.id")),
)

from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

posts = Table(
    "articles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("author_id", Integer),
)

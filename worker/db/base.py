from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session(db_url: str):
    engine = create_engine(db_url, pool_pre_ping=True)
    return sessionmaker(bind=engine)

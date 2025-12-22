from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base


class User(Base):
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    subscription_key = Column(String, nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    subscribers = relationship(
        "Subscriber",
        foreign_keys="Subscriber.author_id",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    subscriptions = relationship(
        "Subscriber",
        foreign_keys="Subscriber.subscriber_id",
        back_populates="subscriber",
        cascade="all, delete-orphan"
    )

class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True)

    subscriber_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    author_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    subscriber = relationship(
        "User",
        foreign_keys=[subscriber_id],
        back_populates="subscriptions"
    )

    author = relationship(
        "User",
        foreign_keys=[author_id],
        back_populates="subscribers"
    )

    __table_args__ = (
        UniqueConstraint(
            "subscriber_id",
            "author_id",
            name="ux_subscriber_author"
        ),
    )
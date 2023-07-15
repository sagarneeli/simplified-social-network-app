import uuid
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    userId = Column(String(50), primary_key=True)
    follows = relationship(
        "Follow", backref="follower", lazy=True, foreign_keys="Follow.followerId"
    )


class Post(Base):
    __tablename__ = "posts"

    postId = Column(String(50), primary_key=True)
    userId = Column(String(50), ForeignKey("users.userId"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Follow(Base):
    __tablename__ = "follows"

    followerId = Column(String(50), ForeignKey("users.userId"), primary_key=True)
    followeeId = Column(String(50), ForeignKey("users.userId"), primary_key=True)


def generate_post_id():
    return str(uuid.uuid4())

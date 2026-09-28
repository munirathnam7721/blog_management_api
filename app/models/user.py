from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    # Password is required for local users.
    # Auth0 users do not have a local password.
    password = Column(
        String(255),
        nullable=True
    )

    # Authentication provider
    # local = email/password
    # google = Google login
    # facebook = Facebook login
    provider = Column(
        String(20),
        nullable=False,
        default="local"
    )

    # Auth0 unique user ID
    # NULL for normal local users
    auth0_id = Column(
        String(255),
        unique=True,
        nullable=True,
        index=True
    )

    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    comments = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    likes = relationship(
        "Like",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    ai_support_chats = relationship(
        "AISupportChat",
        back_populates="user",
        cascade="all, delete-orphan"
    )
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class Post(Base):

    __tablename__ = "posts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    # Existing single image field
    image = Column(
        String(500),
        nullable=True
    )

    author_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # ==========================================
    # AUTHOR
    # ==========================================

    author = relationship(
        "User",
        back_populates="posts"
    )

    # ==========================================
    # COMMENTS
    # ==========================================

    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    # ==========================================
    # LIKES
    # ==========================================

    likes = relationship(
        "Like",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    # ==========================================
    # MULTIPLE IMAGES
    # ==========================================

    images = relationship(
        "PostImage",
        back_populates="post",
        cascade="all, delete-orphan"
    )
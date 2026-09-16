from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.base import Base

from app.database.connection import (
    engine
)

# Import all models
from app.models import (
    User,
    Post,
    Comment,
    Like
)

# Import routers
from app.routers import (
    auth,
    posts,
    comments,
    likes
)


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Blog Management API",
    description=(
        "Blog Management API using "
        "FastAPI, MySQL, SQLAlchemy, "
        "JWT Authentication and Email Notifications."
    ),
    version="1.0.0"
)


# ==========================================
# STATIC FILES
# ==========================================

app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media"
)


# ==========================================
# ROUTERS
# ==========================================

app.include_router(
    auth.router
)

app.include_router(
    posts.router
)

app.include_router(
    comments.router
)

app.include_router(
    likes.router
)


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():

    return {
        "message": "Blog Management API is running",
        "docs": "/docs"
    }
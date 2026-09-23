from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from app.database.base import Base
from app.database.connection import engine

# ==========================================
# IMPORT ALL MODELS
# ==========================================

from app.models import (
    User,
    Post,
    Comment,
    Like,
    PostImage,
    SubscriptionPlan,
    Subscription,
    BillingHistory,
    Notification,
)

# ==========================================
# IMPORT ROUTERS
# ==========================================

from app.routers import (
    auth,
    posts,
    comments,
    likes,
    subscriptions,
    dashboard,
)

from app.routers.notifications import (
    router as notifications_router
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
# CUSTOM OPENAPI
# FIX FOR SWAGGER FILE UPLOAD
# ==========================================

def custom_openapi():

    # If schema is already created,
    # return the existing schema
    if app.openapi_schema:
        return app.openapi_schema

    # Generate the normal OpenAPI schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # ==========================================
    # FIX FILE UPLOAD SCHEMA
    # ==========================================

    def fix_file_schema(obj):

        # If current object is a dictionary
        if isinstance(obj, dict):

            # Convert application/octet-stream
            # into Swagger binary file format
            if obj.get(
                "contentMediaType"
            ) == "application/octet-stream":

                obj.pop(
                    "contentMediaType",
                    None
                )

                obj["type"] = "string"
                obj["format"] = "binary"

            # Check nested objects
            for value in obj.values():
                fix_file_schema(value)

        # If current object is a list
        elif isinstance(obj, list):

            # Check every item
            for item in obj:
                fix_file_schema(item)

    # Apply file upload fix
    fix_file_schema(schema)

    # Save modified schema
    app.openapi_schema = schema

    return app.openapi_schema


# Replace FastAPI's default OpenAPI generator
app.openapi = custom_openapi


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

# Authentication
app.include_router(
    auth.router
)

# Posts
app.include_router(
    posts.router
)

# Comments
app.include_router(
    comments.router
)

# Likes
app.include_router(
    likes.router
)

# Subscriptions
app.include_router(
    subscriptions.router
)

# Dashboard
app.include_router(
    dashboard.router
)

# Notifications
app.include_router(
    notifications_router
)


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def root():

    return {
        "message": "Blog Management API is running",
        "docs": "/docs"
    }
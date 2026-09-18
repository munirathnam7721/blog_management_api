from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from app.database.base import Base

from app.database.connection import (
    engine
)

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

            # FastAPI 0.129+ / newer OpenAPI
            # may represent UploadFile as:
            #
            # type: string
            # contentMediaType: application/octet-stream
            #
            # Swagger UI may then show:
            # "Add string item"
            #
            # Convert it to:
            #
            # type: string
            # format: binary
            #
            # so Swagger shows "Choose File".

            if obj.get(
                "contentMediaType"
            ) == "application/octet-stream":

                # Remove contentMediaType
                obj.pop(
                    "contentMediaType",
                    None
                )

                # Set correct file schema
                obj["type"] = "string"
                obj["format"] = "binary"

            # Check all nested objects
            for value in obj.values():

                fix_file_schema(value)

        # If current object is a list
        elif isinstance(obj, list):

            # Check every item
            for item in obj:

                fix_file_schema(item)

    # Apply the fix to the complete OpenAPI schema
    fix_file_schema(schema)

    # Save the modified schema
    app.openapi_schema = schema

    return app.openapi_schema


# Replace FastAPI's default OpenAPI generator
# with our custom version
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

app.include_router(
    subscriptions.router
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
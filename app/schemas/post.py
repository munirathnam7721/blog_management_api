from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


# ============================================================
# CREATE POST
# ============================================================

class PostCreate(BaseModel):

    title: str = Field(
        ...,
        min_length=3,
        max_length=200
    )

    content: str = Field(
        ...,
        min_length=1
    )

    status: str = "draft"

    scheduled_at: datetime | None = None


# ============================================================
# UPDATE POST
# ============================================================

class PostUpdate(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=200
    )

    content: str | None = Field(
        default=None,
        min_length=1
    )

    status: str | None = None

    scheduled_at: datetime | None = None


# ============================================================
# POST IMAGE RESPONSE
# ============================================================

class PostImageResponse(BaseModel):

    id: int

    post_id: int

    image: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# POST RESPONSE
# ============================================================

class PostResponse(BaseModel):

    id: int

    title: str

    content: str

    image: str | None = None

    images: list[PostImageResponse] = []

    author_id: int

    created_at: datetime

    # --------------------------------------------------------
    # SCHEDULING FIELDS
    # --------------------------------------------------------

    status: str

    scheduled_at: datetime | None = None

    published_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )
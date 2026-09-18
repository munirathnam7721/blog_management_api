from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


# =========================================================
# CREATE POST
# =========================================================

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


# =========================================================
# UPDATE POST
# =========================================================

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


# =========================================================
# POST IMAGE RESPONSE
# =========================================================

class PostImageResponse(BaseModel):

    id: int

    post_id: int

    image: str

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# POST RESPONSE
# =========================================================

class PostResponse(BaseModel):

    id: int

    title: str

    content: str

    # Existing image field
    image: str | None = None

    # New multiple images field
    images: list[PostImageResponse] = []

    author_id: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status
)

from sqlalchemy.orm import Session

from app.database.connection import (
    get_db
)

from app.dependencies.auth import (
    get_current_user
)

from app.models.post import Post

from app.models.user import User

from app.schemas.post import (
    PostResponse
)


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# ==========================================
# IMAGE UPLOAD SETTINGS
# ==========================================

UPLOAD_DIR = "media/posts"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp"
}


# ==========================================
# GET ALL POSTS
# Public
# Pagination + Search
# ==========================================

@router.get("/")
def get_all_posts(
    page: int = Query(
        1,
        ge=1,
        description="Page number"
    ),

    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of posts per page"
    ),

    search: str | None = Query(
        None,
        description="Search posts by title or content"
    ),

    db: Session = Depends(get_db)
):

    query = db.query(Post)

    # --------------------------------------
    # SEARCH
    # --------------------------------------

    if search:

        search_value = f"%{search}%"

        query = query.filter(
            (Post.title.ilike(search_value)) |
            (Post.content.ilike(search_value))
        )

    # --------------------------------------
    # TOTAL POSTS
    # --------------------------------------

    total = query.count()

    # --------------------------------------
    # TOTAL PAGES
    # --------------------------------------

    total_pages = (
        (total + limit - 1) // limit
        if total > 0
        else 0
    )

    # --------------------------------------
    # PAGINATION
    # --------------------------------------

    offset = (page - 1) * limit

    posts = query.order_by(
        Post.created_at.desc()
    ).offset(
        offset
    ).limit(
        limit
    ).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "posts": posts
    }


# ==========================================
# MY POSTS
# Authenticated
# ==========================================

@router.get(
    "/mine/list",
    response_model=list[PostResponse]
)
def get_my_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    posts = db.query(
        Post
    ).filter(
        Post.author_id == current_user.id
    ).order_by(
        Post.created_at.desc()
    ).all()

    return posts


# ==========================================
# GET SINGLE POST
# Public
# ==========================================

@router.get(
    "/{post_id}",
    response_model=PostResponse
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):

    post = db.query(
        Post
    ).filter(
        Post.id == post_id
    ).first()

    if not post:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


# ==========================================
# CREATE POST
# Authenticated
# With Image Upload
# ==========================================

@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_post(
    title: str = Form(
        ...,
        min_length=3,
        max_length=200
    ),

    content: str = Form(
        ...,
        min_length=1
    ),

    image: UploadFile | None = File(
        default=None
    ),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    image_path = None

    # --------------------------------------
    # IMAGE UPLOAD
    # --------------------------------------

    if image:

        if image.content_type not in ALLOWED_IMAGE_TYPES:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, PNG and WEBP "
                    "images are allowed"
                )
            )

        extension = ALLOWED_IMAGE_TYPES[
            image.content_type
        ]

        filename = (
            f"{uuid.uuid4().hex}"
            f"{extension}"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        contents = await image.read()

        with open(
            file_path,
            "wb"
        ) as file:

            file.write(contents)

        image_path = (
            f"/media/posts/{filename}"
        )

    # --------------------------------------
    # CREATE POST
    # --------------------------------------

    post = Post(
        title=title,
        content=content,
        image=image_path,
        author_id=current_user.id
    )

    db.add(post)

    db.commit()

    db.refresh(post)

    return post


# ==========================================
# UPDATE POST
# Owner only
# With Optional Image
# ==========================================

@router.put(
    "/{post_id}",
    response_model=PostResponse
)
async def update_post(
    post_id: int,

    title: str | None = Form(
        default=None,
        min_length=3,
        max_length=200
    ),

    content: str | None = Form(
        default=None,
        min_length=1
    ),

    image: UploadFile | None = File(
        default=None
    ),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    post = db.query(
        Post
    ).filter(
        Post.id == post_id
    ).first()

    if not post:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    # --------------------------------------
    # OWNERSHIP CHECK
    # --------------------------------------

    if post.author_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail=(
                "You can only update "
                "your own posts"
            )
        )

    # --------------------------------------
    # UPDATE TITLE
    # --------------------------------------

    if title is not None:

        post.title = title

    # --------------------------------------
    # UPDATE CONTENT
    # --------------------------------------

    if content is not None:

        post.content = content

    # --------------------------------------
    # UPDATE IMAGE
    # --------------------------------------

    if image:

        if image.content_type not in ALLOWED_IMAGE_TYPES:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, PNG and WEBP "
                    "images are allowed"
                )
            )

        # Delete old image
        if post.image:

            old_file_path = post.image.lstrip(
                "/"
            )

            if os.path.exists(
                old_file_path
            ):

                os.remove(
                    old_file_path
                )

        extension = ALLOWED_IMAGE_TYPES[
            image.content_type
        ]

        filename = (
            f"{uuid.uuid4().hex}"
            f"{extension}"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        contents = await image.read()

        with open(
            file_path,
            "wb"
        ) as file:

            file.write(contents)

        post.image = (
            f"/media/posts/{filename}"
        )

    # --------------------------------------
    # SAVE CHANGES
    # --------------------------------------

    db.commit()

    db.refresh(post)

    return post


# ==========================================
# DELETE POST
# Owner only
# ==========================================

@router.delete(
    "/{post_id}"
)
def delete_post(
    post_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    post = db.query(
        Post
    ).filter(
        Post.id == post_id
    ).first()

    if not post:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    # --------------------------------------
    # OWNERSHIP CHECK
    # --------------------------------------

    if post.author_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail=(
                "You can only delete "
                "your own posts"
            )
        )

    # --------------------------------------
    # DELETE IMAGE
    # --------------------------------------

    if post.image:

        file_path = post.image.lstrip(
            "/"
        )

        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )

    # --------------------------------------
    # DELETE POST
    # --------------------------------------

    db.delete(post)

    db.commit()

    return {
        "message": "Post deleted successfully"
    }
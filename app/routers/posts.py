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
from app.models.post_image import PostImage
from app.models.user import User

from app.schemas.post import (
    PostResponse
)

from app.services.subscription_service import (
    check_post_limit,
    get_active_subscription
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
# Subscription Limit
# Multiple Image Upload
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

    images: list[UploadFile] | None = File(
        default=None
    ),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # --------------------------------------
    # CHECK POST LIMIT
    # --------------------------------------

    check_post_limit(
        db=db,
        user_id=current_user.id
    )

    # --------------------------------------
    # GET ACTIVE SUBSCRIPTION
    # --------------------------------------

    active_subscription = get_active_subscription(
        db=db,
        user_id=current_user.id
    )

    if not active_subscription:

        raise HTTPException(
            status_code=403,
            detail=(
                "You need an active subscription "
                "to continue."
            )
        )

    subscription, plan = active_subscription

    # --------------------------------------
    # GET IMAGE LIMIT
    # --------------------------------------

    image_limit = plan.max_images_per_post

    # --------------------------------------
    # IMAGE LIST
    # --------------------------------------

    uploaded_images = images or []

    # --------------------------------------
    # CHECK IMAGE LIMIT
    # --------------------------------------

    if image_limit is not None:

        if len(uploaded_images) > image_limit:

            raise HTTPException(
                status_code=403,
                detail=(
                    "You've reached your plan limit. "
                    "Kindly upgrade your plan to continue."
                )
            )

    # --------------------------------------
    # CREATE POST
    # --------------------------------------

    post = Post(
        title=title,
        content=content,
        image=None,
        author_id=current_user.id
    )

    db.add(post)

    # Get generated post ID
    db.flush()

    # --------------------------------------
    # UPLOAD IMAGES
    # --------------------------------------

    for image in uploaded_images:

        # Check image type
        if image.content_type not in ALLOWED_IMAGE_TYPES:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, PNG and WEBP "
                    "images are allowed"
                )
            )

        # ----------------------------------
        # GET EXTENSION
        # ----------------------------------

        extension = ALLOWED_IMAGE_TYPES[
            image.content_type
        ]

        # ----------------------------------
        # GENERATE UNIQUE FILE NAME
        # ----------------------------------

        filename = (
            f"{uuid.uuid4().hex}"
            f"{extension}"
        )

        # ----------------------------------
        # FILE PATH
        # ----------------------------------

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        # ----------------------------------
        # READ FILE
        # ----------------------------------

        contents = await image.read()

        # ----------------------------------
        # SAVE FILE
        # ----------------------------------

        with open(
            file_path,
            "wb"
        ) as file:

            file.write(contents)

        # ----------------------------------
        # SAVE IMAGE RECORD
        # ----------------------------------

        post_image = PostImage(
            post_id=post.id,
            image=f"/media/posts/{filename}"
        )

        db.add(post_image)

    # --------------------------------------
    # SAVE EVERYTHING
    # --------------------------------------

    db.commit()

    db.refresh(post)

    return post


# ==========================================
# UPDATE POST
# Owner Only
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

    images: list[UploadFile] | None = File(
        default=None
    ),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    # --------------------------------------
    # FIND POST
    # --------------------------------------

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
    # UPDATE IMAGES
    # --------------------------------------

    uploaded_images = images or []

    if uploaded_images:

        # ----------------------------------
        # GET ACTIVE SUBSCRIPTION
        # ----------------------------------

        active_subscription = get_active_subscription(
            db=db,
            user_id=current_user.id
        )

        if not active_subscription:

            raise HTTPException(
                status_code=403,
                detail=(
                    "You need an active subscription "
                    "to continue."
                )
            )

        subscription, plan = active_subscription

        image_limit = plan.max_images_per_post

        # ----------------------------------
        # CHECK IMAGE LIMIT
        # ----------------------------------

        if image_limit is not None:

            if len(uploaded_images) > image_limit:

                raise HTTPException(
                    status_code=403,
                    detail=(
                        "You've reached your plan limit. "
                        "Kindly upgrade your plan to continue."
                    )
                )

        # ----------------------------------
        # DELETE EXISTING POST IMAGES
        # ----------------------------------

        existing_images = db.query(
            PostImage
        ).filter(
            PostImage.post_id == post.id
        ).all()

        for old_image in existing_images:

            old_file_path = old_image.image.lstrip("/")

            if os.path.exists(old_file_path):

                os.remove(old_file_path)

            db.delete(old_image)

        # ----------------------------------
        # UPLOAD NEW IMAGES
        # ----------------------------------

        for image in uploaded_images:

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

            post_image = PostImage(
                post_id=post.id,
                image=f"/media/posts/{filename}"
            )

            db.add(post_image)

        # ----------------------------------
        # REMOVE OLD SINGLE IMAGE
        # ----------------------------------

        if post.image:

            old_file_path = post.image.lstrip("/")

            if os.path.exists(old_file_path):

                os.remove(old_file_path)

            post.image = None

    # --------------------------------------
    # SAVE CHANGES
    # --------------------------------------

    db.commit()

    db.refresh(post)

    return post


# ==========================================
# DELETE POST
# Owner Only
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

    # --------------------------------------
    # FIND POST
    # --------------------------------------

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
    # DELETE OLD SINGLE IMAGE
    # --------------------------------------

    if post.image:

        file_path = post.image.lstrip("/")

        if os.path.exists(file_path):

            os.remove(file_path)

    # --------------------------------------
    # DELETE MULTIPLE IMAGES
    # --------------------------------------

    post_images = db.query(
        PostImage
    ).filter(
        PostImage.post_id == post.id
    ).all()

    for post_image in post_images:

        file_path = post_image.image.lstrip("/")

        if os.path.exists(file_path):

            os.remove(file_path)

    # --------------------------------------
    # DELETE POST
    # --------------------------------------

    db.delete(post)

    db.commit()

    return {
        "message": "Post deleted successfully"
    }
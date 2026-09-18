from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.connection import (
    get_db
)

from app.dependencies.auth import (
    get_current_user
)

from app.models.like import Like

from app.models.post import Post

from app.models.user import User

from app.schemas.like import (
    LikeResponse
)

from app.services.email_service import (
    send_email
)

from app.services.subscription_service import (
    check_like_limit
)


router = APIRouter(
    prefix="/posts",
    tags=["Likes"]
)


# ==========================================
# LIKE POST
# ==========================================

@router.post(
    "/{post_id}/like",
    response_model=LikeResponse
)
def like_post(
    post_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    # ==========================================
    # 1. CHECK POST
    # ==========================================

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

    # ==========================================
    # 2. CHECK EXISTING LIKE
    # ==========================================

    existing_like = db.query(
        Like
    ).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if existing_like:

        raise HTTPException(
            status_code=400,
            detail="You already liked this post"
        )

    # ==========================================
    # 3. CHECK SUBSCRIPTION LIKE LIMIT
    # ==========================================

    check_like_limit(
        db=db,
        user_id=current_user.id
    )

    # ==========================================
    # 4. CREATE LIKE
    # ==========================================

    like = Like(
        post_id=post_id,
        user_id=current_user.id
    )

    db.add(like)

    db.commit()

    # ==========================================
    # 5. SEND EMAIL NOTIFICATION
    # ==========================================

    if post.author.email != current_user.email:

        email_body = (
            f"Hello {post.author.username},\n\n"
            f"{current_user.username} liked "
            f"your blog post.\n\n"
            f"Post: {post.title}"
        )

        background_tasks.add_task(
            send_email,
            post.author.email,
            "New Like on Your Blog Post",
            email_body
        )

    return {
        "message": "Post liked successfully",
        "post_id": post_id,
        "user_id": current_user.id
    }


# ==========================================
# UNLIKE POST
# ==========================================

@router.delete(
    "/{post_id}/like",
    response_model=LikeResponse
)
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    like = db.query(
        Like
    ).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if not like:

        raise HTTPException(
            status_code=404,
            detail="Like not found"
        )

    db.delete(like)

    db.commit()

    return {
        "message": "Post unliked successfully",
        "post_id": post_id,
        "user_id": current_user.id
    }


# ==========================================
# LIKE COUNT
# Public
# ==========================================

@router.get(
    "/{post_id}/likes"
)
def get_like_count(
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

    like_count = db.query(
        Like
    ).filter(
        Like.post_id == post_id
    ).count()

    return {
        "post_id": post_id,
        "like_count": like_count
    }
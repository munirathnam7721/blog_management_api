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

from app.models.notification import Notification

from app.schemas.like import (
    LikeResponse
)

from app.services.notification_service import (
    send_post_activity_notification
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

    # ==========================================
    # 5. CREATE IN-APP NOTIFICATION
    # ==========================================

    # Do not create a notification when a user
    # likes their own post.

    if post.author_id != current_user.id:

        notification = Notification(
            user_id=post.author_id,
            message=(
                f"{current_user.username} "
                f"liked your post '{post.title}'"
            ),
            notification_type="like",
            is_read=False
        )

        db.add(notification)

    # ==========================================
    # 6. SAVE LIKE AND NOTIFICATION
    # ==========================================

    db.commit()

    # ==========================================
    # 7. SEND EMAIL NOTIFICATION
    # ==========================================

    # Do not send an email when the user likes
    # their own post.

    if post.author_id != current_user.id:

        background_tasks.add_task(
            send_post_activity_notification,
            post_owner_email=post.author.email,
            post_title=post.title,
            actor_name=current_user.username,
            activity_type="like"
        )

    # ==========================================
    # 8. RETURN RESPONSE
    # ==========================================

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

    # ==========================================
    # 1. FIND LIKE
    # ==========================================

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

    # ==========================================
    # 2. DELETE LIKE
    # ==========================================

    db.delete(like)

    db.commit()

    # ==========================================
    # 3. RETURN RESPONSE
    # ==========================================

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
    # 2. COUNT LIKES
    # ==========================================

    like_count = db.query(
        Like
    ).filter(
        Like.post_id == post_id
    ).count()

    # ==========================================
    # 3. RETURN RESPONSE
    # ==========================================

    return {
        "post_id": post_id,
        "like_count": like_count
    }
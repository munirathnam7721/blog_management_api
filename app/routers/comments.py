from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database.connection import (
    get_db
)

from app.dependencies.auth import (
    get_current_user
)

from app.models.comment import Comment

from app.models.post import Post

from app.models.user import User

from app.schemas.comment import (
    CommentCreate,
    CommentResponse
)

from app.services.notification_service import (
    send_post_activity_notification
)

from app.services.subscription_service import (
    check_comment_limit
)


router = APIRouter(
    prefix="/posts",
    tags=["Comments"]
)


# ==========================================
# GET COMMENTS
# Public
# ==========================================

@router.get(
    "/{post_id}/comments",
    response_model=list[CommentResponse]
)
def get_comments(
    post_id: int,
    db: Session = Depends(get_db)
):

    # ==========================================
    # CHECK POST
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
    # GET COMMENTS
    # ==========================================

    comments = db.query(
        Comment
    ).filter(
        Comment.post_id == post_id
    ).order_by(
        Comment.created_at.desc()
    ).all()

    return comments


# ==========================================
# ADD COMMENT
# Authenticated
# ==========================================

@router.post(
    "/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def add_comment(
    post_id: int,
    comment_data: CommentCreate,
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
    # 2. CHECK COMMENT LIMIT
    # ==========================================

    check_comment_limit(
        db=db,
        user_id=current_user.id
    )

    # ==========================================
    # 3. CREATE COMMENT
    # ==========================================

    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        text=comment_data.text
    )

    db.add(comment)

    db.commit()

    db.refresh(comment)

    # ==========================================
    # 4. SEND EMAIL NOTIFICATION
    # ==========================================

    # Do not send an email if the user comments
    # on their own post.

    if post.author_id != current_user.id:

        background_tasks.add_task(
            send_post_activity_notification,
            post_owner_email=post.author.email,
            post_title=post.title,
            actor_name=current_user.username,
            activity_type="comment"
        )

    # ==========================================
    # 5. RETURN COMMENT
    # ==========================================

    return comment
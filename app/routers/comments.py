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

from app.services.email_service import (
    send_email
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
    # 4. EMAIL POST OWNER
    # ==========================================

    if post.author.email != current_user.email:

        email_body = (
            f"Hello {post.author.username},\n\n"
            f"{current_user.username} commented "
            f"on your blog post.\n\n"
            f"Post: {post.title}\n\n"
            f"Comment:\n{comment.text}"
        )

        background_tasks.add_task(
            send_email,
            post.author.email,
            "New Comment on Your Blog Post",
            email_body
        )

    return comment
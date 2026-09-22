from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ==========================================
    # TOTAL POSTS CREATED BY CURRENT USER
    # ==========================================

    total_posts = db.query(
        Post
    ).filter(
        Post.author_id == current_user.id
    ).count()


    # ==========================================
    # TOTAL COMMENTS MADE BY CURRENT USER
    # ==========================================

    total_comments = db.query(
        Comment
    ).filter(
        Comment.user_id == current_user.id
    ).count()


    # ==========================================
    # TOTAL LIKES RECEIVED ON USER'S POSTS
    # ==========================================

    total_likes_received = db.query(
        Like
    ).join(
        Post,
        Like.post_id == Post.id
    ).filter(
        Post.author_id == current_user.id
    ).count()


    # ==========================================
    # TOTAL POST VIEWS
    # ==========================================
    #
    # View tracking is not implemented yet.
    # Therefore, return 0 for now.
    #

    total_views = 0


    # ==========================================
    # PER-POST ANALYTICS
    # ==========================================

    posts = db.query(
        Post
    ).filter(
        Post.author_id == current_user.id
    ).order_by(
        Post.created_at.asc()
    ).all()


    post_analytics = []

    for post in posts:

        like_count = db.query(
            Like
        ).filter(
            Like.post_id == post.id
        ).count()

        comment_count = db.query(
            Comment
        ).filter(
            Comment.post_id == post.id
        ).count()

        post_analytics.append(
            {
                "post_id": post.id,
                "post_title": post.title,
                "likes": like_count,
                "comments": comment_count,
                "created_at": post.created_at
            }
        )


    # ==========================================
    # FINAL RESPONSE
    # ==========================================

    return {
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        },

        "statistics": {
            "total_posts": total_posts,
            "total_comments": total_comments,
            "total_likes_received": total_likes_received,
            "total_views": total_views
        },

        "post_analytics": post_analytics
    }
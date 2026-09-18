from datetime import datetime, timedelta
import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.post import Post
from app.models.like import Like
from app.models.comment import Comment
from app.models.user import User

from app.models.subscription import (
    Subscription,
    SubscriptionPlan,
    BillingHistory,
)

from app.services.invoice_service import generate_invoice


PLAN_LIMIT_MESSAGE = (
    "You've reached your plan limit. "
    "Kindly upgrade your plan to continue."
)


# =========================================================
# GET ACTIVE SUBSCRIPTION
# =========================================================

def get_active_subscription(
    db: Session,
    user_id: int
):
    """
    Get the user's currently active subscription
    and its plan.
    """

    now = datetime.now()

    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == user_id,
            Subscription.is_active == True,
            Subscription.start_date <= now,
            Subscription.end_date >= now,
        )
        .first()
    )

    if not subscription:
        return None

    plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.id == subscription.plan_id,
            SubscriptionPlan.is_active == True,
        )
        .first()
    )

    if not plan:
        return None

    return subscription, plan


# =========================================================
# CHECK POST LIMIT
# =========================================================

def check_post_limit(
    db: Session,
    user_id: int
):
    """
    Check whether the user is allowed
    to create another post.
    """

    active_subscription = get_active_subscription(
        db,
        user_id
    )

    if not active_subscription:
        raise HTTPException(
            status_code=403,
            detail="You need an active subscription to continue."
        )

    subscription, plan = active_subscription

    # None means unlimited
    if plan.max_posts is None:
        return True

    current_post_count = (
        db.query(Post)
        .filter(
            Post.author_id == user_id
        )
        .count()
    )

    if current_post_count >= plan.max_posts:
        raise HTTPException(
            status_code=403,
            detail=PLAN_LIMIT_MESSAGE
        )

    return True


# =========================================================
# CHECK LIKE LIMIT
# =========================================================

def check_like_limit(
    db: Session,
    user_id: int
):
    """
    Check whether the user is allowed
    to create another like.
    """

    active_subscription = get_active_subscription(
        db,
        user_id
    )

    if not active_subscription:
        raise HTTPException(
            status_code=403,
            detail="You need an active subscription to continue."
        )

    subscription, plan = active_subscription

    # None means unlimited
    if plan.max_likes is None:
        return True

    current_like_count = (
        db.query(Like)
        .filter(
            Like.user_id == user_id
        )
        .count()
    )

    if current_like_count >= plan.max_likes:
        raise HTTPException(
            status_code=403,
            detail=PLAN_LIMIT_MESSAGE
        )

    return True


# =========================================================
# CHECK COMMENT LIMIT
# =========================================================

def check_comment_limit(
    db: Session,
    user_id: int
):
    """
    Check whether the user is allowed
    to create another comment.
    """

    active_subscription = get_active_subscription(
        db,
        user_id
    )

    if not active_subscription:
        raise HTTPException(
            status_code=403,
            detail="You need an active subscription to continue."
        )

    subscription, plan = active_subscription

    # None means unlimited
    if plan.max_comments is None:
        return True

    current_comment_count = (
        db.query(Comment)
        .filter(
            Comment.user_id == user_id
        )
        .count()
    )

    if current_comment_count >= plan.max_comments:
        raise HTTPException(
            status_code=403,
            detail=PLAN_LIMIT_MESSAGE
        )

    return True


# =========================================================
# CREATE SUBSCRIPTION
# =========================================================

def create_subscription(
    db: Session,
    user_id: int,
    plan_id: int
):
    """
    Create subscription,
    create billing history,
    and generate invoice PDF.
    """

    # 1. Find selected plan
    plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.id == plan_id,
            SubscriptionPlan.is_active == True,
        )
        .first()
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found."
        )

    # 2. Get user
    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    # 3. Deactivate existing active subscriptions
    existing_subscriptions = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == user_id,
            Subscription.is_active == True,
        )
        .all()
    )

    for subscription in existing_subscriptions:
        subscription.is_active = False

    # 4. Create subscription dates
    start_date = datetime.now()

    end_date = (
        start_date + timedelta(days=30)
    )

    # 5. Create subscription
    new_subscription = Subscription(
        user_id=user_id,
        plan_id=plan.id,
        start_date=start_date,
        end_date=end_date,
        is_active=True,
        created_at=start_date,
    )

    db.add(new_subscription)

    # Generate subscription ID
    db.flush()

    # 6. Generate transaction ID
    transaction_id = (
        f"TXN-{uuid.uuid4().hex[:12].upper()}"
    )

    # 7. Create billing history
    billing = BillingHistory(
        user_id=user_id,
        subscription_id=new_subscription.id,
        plan_id=plan.id,
        amount=plan.price,
        transaction_id=transaction_id,
        billing_date=start_date,
        invoice_path=None,
        payment_status="SUCCESS",
    )

    db.add(billing)

    # Generate billing ID
    db.flush()

    # 8. Generate invoice PDF
    invoice_path = generate_invoice(
        user=user,
        subscription=new_subscription,
        billing=billing,
        plan=plan
    )

    # 9. Save invoice path
    billing.invoice_path = invoice_path

    # 10. Commit everything
    db.commit()

    # 11. Refresh objects
    db.refresh(new_subscription)
    db.refresh(billing)

    return new_subscription, billing, plan
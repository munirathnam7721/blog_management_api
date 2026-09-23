from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.models.subscription import (
    SubscriptionPlan,
    BillingHistory,
)

from app.models.notification import Notification

from app.schemas.subscription import (
    SubscriptionPlanResponse,
    SubscriptionCreate,
    SubscribeResponse,
    BillingHistoryResponse,
)

from app.services.subscription_service import (
    create_subscription,
    renew_subscription,
    get_active_subscription,
)


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


# =========================================================
# GET ALL ACTIVE SUBSCRIPTION PLANS
# =========================================================

@router.get(
    "/plans",
    response_model=list[SubscriptionPlanResponse]
)
def get_subscription_plans(
    db: Session = Depends(get_db)
):

    plans = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.is_active == True
        )
        .all()
    )

    return plans


# =========================================================
# CREATE / PURCHASE SUBSCRIPTION
# =========================================================

@router.post(
    "/subscribe",
    response_model=SubscribeResponse
)
def subscribe_to_plan(
    subscription_data: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ==========================================
    # 1. CREATE SUBSCRIPTION
    # ==========================================

    subscription, billing, plan = create_subscription(
        db=db,
        user_id=current_user.id,
        plan_id=subscription_data.plan_id
    )

    # ==========================================
    # 2. CREATE ACTIVATION NOTIFICATION
    # ==========================================

    notification = Notification(
        user_id=current_user.id,
        message=(
            f"Your {plan.name} subscription "
            f"has been activated successfully."
        ),
        notification_type="subscription",
        is_read=False
    )

    db.add(notification)

    db.commit()

    # ==========================================
    # 3. RETURN RESPONSE
    # ==========================================

    return {
        "message": "Subscription created successfully",
        "subscription": subscription,
        "billing": billing,
        "plan": plan
    }


# =========================================================
# RENEW SUBSCRIPTION
# =========================================================

@router.post(
    "/renew",
    response_model=SubscribeResponse
)
def renew_user_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ==========================================
    # 1. RENEW SUBSCRIPTION
    # ==========================================

    subscription, billing, plan = renew_subscription(
        db=db,
        user_id=current_user.id
    )

    # ==========================================
    # 2. CREATE RENEWAL NOTIFICATION
    # ==========================================

    notification = Notification(
        user_id=current_user.id,
        message=(
            f"Your {plan.name} subscription "
            f"has been renewed successfully."
        ),
        notification_type="subscription_renewal",
        is_read=False
    )

    db.add(notification)

    db.commit()

    # ==========================================
    # 3. RETURN RESPONSE
    # ==========================================

    return {
        "message": "Subscription renewed successfully",
        "subscription": subscription,
        "billing": billing,
        "plan": plan
    }


# =========================================================
# GET MY BILLING HISTORY
# =========================================================

@router.get(
    "/billing-history",
    response_model=list[BillingHistoryResponse]
)
def get_billing_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    billing_history = (
        db.query(BillingHistory)
        .filter(
            BillingHistory.user_id == current_user.id
        )
        .order_by(
            BillingHistory.billing_date.desc()
        )
        .all()
    )

    return billing_history


# =========================================================
# GET MY ACTIVE SUBSCRIPTION
# =========================================================

@router.get(
    "/my-subscription"
)
def get_my_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    active_subscription = get_active_subscription(
        db=db,
        user_id=current_user.id
    )

    if not active_subscription:

        return {
            "message": "No active subscription found"
        }

    subscription, plan = active_subscription

    return {
        "subscription": subscription,
        "plan": plan
    }
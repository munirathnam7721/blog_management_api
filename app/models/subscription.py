from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Numeric,
    Text,
    ForeignKey,
)

from app.database.base import Base


# =========================================================
# SUBSCRIPTION PLAN
# =========================================================

class SubscriptionPlan(Base):

    __tablename__ = "subscriptions_subscriptionplan"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(50),
        unique=True,
        nullable=False
    )

    price = Column(
        Numeric(10, 2),
        nullable=False
    )

    max_posts = Column(
        Integer,
        nullable=True
    )

    max_images_per_post = Column(
        Integer,
        nullable=True
    )

    max_likes = Column(
        Integer,
        nullable=True
    )

    max_comments = Column(
        Integer,
        nullable=True
    )

    description = Column(
        Text,
        nullable=False,
        default=""
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        nullable=False
    )


# =========================================================
# SUBSCRIPTION
# =========================================================

class Subscription(Base):

    __tablename__ = "subscriptions_subscription"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    plan_id = Column(
        Integer,
        ForeignKey("subscriptions_subscriptionplan.id"),
        nullable=False
    )

    start_date = Column(
        DateTime,
        nullable=False
    )

    end_date = Column(
        DateTime,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        nullable=False
    )


# =========================================================
# BILLING HISTORY
# =========================================================

class BillingHistory(Base):

    __tablename__ = "subscriptions_billinghistory"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    subscription_id = Column(
        Integer,
        ForeignKey("subscriptions_subscription.id"),
        nullable=False
    )

    plan_id = Column(
        Integer,
        ForeignKey("subscriptions_subscriptionplan.id"),
        nullable=False
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    transaction_id = Column(
        String(100),
        unique=True,
        nullable=False
    )

    billing_date = Column(
        DateTime,
        nullable=False
    )

    invoice_path = Column(
        String(500),
        nullable=True
    )

    payment_status = Column(
        String(30),
        default="SUCCESS"
    )
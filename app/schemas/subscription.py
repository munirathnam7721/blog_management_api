from datetime import datetime

from pydantic import BaseModel


class SubscriptionPlanResponse(BaseModel):
    id: int
    name: str
    price: float
    max_posts: int | None
    max_images_per_post: int | None
    max_likes: int | None
    max_comments: int | None
    description: str
    is_active: bool

    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    plan_id: int


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    start_date: datetime
    end_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class BillingHistoryResponse(BaseModel):
    id: int
    user_id: int
    subscription_id: int
    plan_id: int
    amount: float
    transaction_id: str
    billing_date: datetime
    invoice_path: str | None
    payment_status: str

    class Config:
        from_attributes = True


class SubscribeResponse(BaseModel):
    message: str
    subscription: SubscriptionResponse
    billing: BillingHistoryResponse
    plan: SubscriptionPlanResponse
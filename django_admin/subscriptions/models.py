from django.db import models


class BlogUser(models.Model):
    """
    Django representation of the existing FastAPI users table.

    This table is already managed by SQLAlchemy/FastAPI,
    so Django must NOT create or modify this table.
    """

    id = models.IntegerField(primary_key=True)

    username = models.CharField(
        max_length=50,
        unique=True
    )

    email = models.EmailField(
        max_length=100,
        unique=True
    )

    password = models.CharField(
        max_length=255
    )

    class Meta:
        managed = False
        db_table = "users"

    def __str__(self):
        return self.username


class SubscriptionPlan(models.Model):
    """
    Stores the available subscription plans.

    Example:
    Basic
    Premium
    Pro
    """

    name = models.CharField(
        max_length=50,
        unique=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    max_posts = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Leave blank for unlimited posts."
    )

    max_images_per_post = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Leave blank for unlimited images."
    )

    max_likes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Leave blank for unlimited likes."
    )

    max_comments = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Leave blank for unlimited comments."
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """
    Stores a user's current subscription.
    """

    user = models.ForeignKey(
        BlogUser,
        on_delete=models.DO_NOTHING,
        related_name="subscriptions"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name="subscriptions"
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"


class BillingHistory(models.Model):
    """
    Stores billing/payment information for subscriptions.
    """

    user = models.ForeignKey(
        BlogUser,
        on_delete=models.DO_NOTHING,
        related_name="billing_history"
    )

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name="billing_records"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name="billing_history"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    billing_date = models.DateTimeField(
        auto_now_add=True
    )

    invoice_path = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=30,
        default="SUCCESS"
    )

    def __str__(self):
        return f"{self.transaction_id} - {self.user.username}"
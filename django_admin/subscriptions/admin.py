from django.contrib import admin
from .models import (
    BlogUser,
    SubscriptionPlan,
    Subscription,
    BillingHistory,
)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "max_posts",
        "max_images_per_post",
        "max_likes",
        "max_comments",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan",
        "start_date",
        "end_date",
        "is_active",
        "created_at",
    )

    list_filter = (
        "plan",
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__email",
    )


@admin.register(BillingHistory)
class BillingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "user",
        "plan",
        "amount",
        "payment_status",
        "billing_date",
        "invoice_path",
    )

    list_filter = (
        "payment_status",
        "plan",
    )

    search_fields = (
        "transaction_id",
        "user__username",
        "user__email",
    )


@admin.register(BlogUser)
class BlogUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
    )

    search_fields = (
        "username",
        "email",
    )

    readonly_fields = (
        "id",
        "username",
        "email",
        "password",
    )
from datetime import datetime

from app.services.email_service import send_email


# ==========================================
# SEND POST ACTIVITY NOTIFICATION
# ==========================================

def send_post_activity_notification(
    post_owner_email: str,
    post_title: str,
    actor_name: str,
    activity_type: str,
):
    """
    Send an email notification to the owner of a post
    when someone likes or comments on the post.
    """

    # ==========================================
    # GET CURRENT TIME
    # ==========================================

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %I:%M %p"
    )

    # ==========================================
    # ACTIVITY MESSAGE
    # ==========================================

    if activity_type.lower() == "like":

        activity_text = "Liked your post"

    elif activity_type.lower() == "comment":

        activity_text = "Commented on your post"

    else:

        activity_text = activity_type

    # ==========================================
    # EMAIL SUBJECT
    # ==========================================

    subject = (
        f"New activity on your post: "
        f"{post_title}"
    )

    # ==========================================
    # EMAIL BODY
    # ==========================================

    body = f"""
Hello,

There is new activity on your blog post.

Post: {post_title}

User: {actor_name}

Activity: {activity_text}

Time: {timestamp}

Thank you,
Blog Management API
"""

    # ==========================================
    # SEND EMAIL
    # ==========================================

    send_email(
        recipient=post_owner_email,
        subject=subject,
        body=body,
    )
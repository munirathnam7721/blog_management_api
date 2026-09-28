def get_ai_response(message: str) -> str:

    # Convert message to lowercase and remove extra spaces
    message = message.lower().strip()

    # ==========================================
    # CREATE POST
    # ==========================================

    if (
        "create post" in message
        or "create a post" in message
        or "new post" in message
        or "add post" in message
        or "add a post" in message
        or "make a post" in message
        or "make a new post" in message
        or "write a post" in message
        or "how to create" in message
        or "how can i create" in message
        or "how do i create" in message
    ):
        return (
            "To create a post, log in to your account and use "
            "the Create Post option. Enter the post title, content, "
            "and any required images, then submit the post."
        )

    # ==========================================
    # EDIT POST
    # ==========================================

    if (
        "edit post" in message
        or "edit a post" in message
        or "update post" in message
        or "update a post" in message
        or "modify post" in message
        or "modify a post" in message
        or "change my post" in message
        or "how to edit" in message
        or "how can i edit" in message
        or "how do i edit" in message
    ):
        return (
            "To edit a post, open your posts and select the post "
            "you want to modify. Update the title or content and "
            "save the changes."
        )

    # ==========================================
    # DELETE POST
    # ==========================================

    if (
        "delete post" in message
        or "delete a post" in message
        or "remove post" in message
        or "remove a post" in message
        or "erase post" in message
        or "how to delete" in message
        or "how can i delete" in message
        or "how do i delete" in message
    ):
        return (
            "To delete a post, open your post management section, "
            "select the post you want to remove, and use the "
            "Delete option. Please confirm the deletion when prompted."
        )

    # ==========================================
    # SUBSCRIPTION
    # ==========================================

    if (
        "subscription" in message
        or "subscriptions" in message
        or "subscribe" in message
        or "subscribed" in message
        or "plan" in message
        or "plans" in message
        or "premium" in message
    ):
        return (
            "You can view the available subscription plans and "
            "their features from the Subscriptions section. "
            "After selecting a plan, you can subscribe and manage "
            "your active subscription."
        )

    # ==========================================
    # BILLING
    # ==========================================

    if (
        "billing" in message
        or "invoice" in message
        or "invoices" in message
        or "payment" in message
        or "payments" in message
        or "transaction" in message
        or "transactions" in message
        or "billing history" in message
        or "payment history" in message
    ):
        return (
            "Your billing information can be viewed from the "
            "Billing History section. It contains information "
            "about payments, transaction IDs, billing dates, "
            "amounts, and invoice details."
        )

    # ==========================================
    # PROFILE
    # ==========================================

    if (
        "profile" in message
        or "my profile" in message
        or "account" in message
        or "my account" in message
        or "username" in message
        or "email" in message
        or "user details" in message
    ):
        return (
            "You can manage your account information from your "
            "profile section. Your username and email are associated "
            "with your registered account."
        )

    # ==========================================
    # DASHBOARD
    # ==========================================

    if (
        "dashboard" in message
        or "analytics" in message
        or "statistics" in message
        or "stats" in message
        or "performance" in message
        or "blog activity" in message
    ):
        return (
            "The dashboard provides an overview of your blog activity. "
            "It can display total posts, comments, likes received, "
            "views, and post-level activity using visual charts."
        )

    # ==========================================
    # NOTIFICATIONS
    # ==========================================

    if (
        "notification" in message
        or "notifications" in message
        or "alerts" in message
        or "alert" in message
    ):
        return (
            "Notifications keep you informed about important activity "
            "such as likes, comments, subscription activation, and "
            "subscription renewals. You can mark individual "
            "notifications or all notifications as read."
        )

    # ==========================================
    # COMMENTS
    # ==========================================

    if (
        "comment" in message
        or "comments" in message
        or "commenting" in message
    ):
        return (
            "You can add comments to posts and view existing comments. "
            "When another user comments on your post, you receive a "
            "notification."
        )

    # ==========================================
    # LIKES
    # ==========================================

    if (
        "like" in message
        or "likes" in message
        or "liked" in message
    ):
        return (
            "Users can like posts. When another user likes one of "
            "your posts, the system creates a notification for you."
        )

    # ==========================================
    # LOGIN
    # ==========================================

    if (
        "login" in message
        or "log in" in message
        or "logging in" in message
        or "sign in" in message
        or "signin" in message
    ):
        return (
            "Use your registered email address and password to log in. "
            "After successful authentication, the system provides "
            "access to protected features."
        )

    # ==========================================
    # LOGOUT
    # ==========================================

    if (
        "logout" in message
        or "log out" in message
        or "sign out" in message
    ):
        return (
            "To log out, use the Logout option available in your "
            "account. This will end your current authenticated session."
        )

    # ==========================================
    # PASSWORD
    # ==========================================

    if (
        "password" in message
        or "forgot password" in message
        or "reset password" in message
        or "change password" in message
    ):
        return (
            "For password-related issues, use the available password "
            "management option in your account. If you forgot your "
            "password, use the password reset process provided by "
            "the application."
        )

    # ==========================================
    # GREETING
    # ==========================================

    if (
        message == "hi"
        or message == "hello"
        or message == "hey"
        or message.startswith("hi ")
        or message.startswith("hello ")
        or message.startswith("hey ")
    ):
        return (
            "Hello! I'm your Blog Support Assistant. "
            "I can help you with posts, subscriptions, billing, "
            "comments, likes, notifications, profile management, "
            "login, and dashboard analytics. "
            "What would you like to know?"
        )

    # ==========================================
    # HELP
    # ==========================================

    if (
        "help me" in message
        or message == "help"
        or "what can you do" in message
        or "what do you support" in message
    ):
        return (
            "I'm your Blog Support Assistant. I can help you with "
            "creating, editing, and deleting posts, subscriptions, "
            "billing, profile management, dashboard analytics, "
            "comments, likes, notifications, login, and account "
            "questions."
        )

    # ==========================================
    # GENERAL BLOG QUESTIONS
    # ==========================================

    if (
        "blog" in message
        or "blog management" in message
    ):
        return (
            "The Blog Management system allows you to create and "
            "manage posts, add comments, like posts, manage "
            "subscriptions, view billing information, receive "
            "notifications, and monitor your activity through "
            "the dashboard."
        )

    # ==========================================
    # DEFAULT RESPONSE
    # ==========================================

    return (
        "I'm sorry, I don't have a specific answer for that yet. "
        "I can currently help with creating, editing, and deleting "
        "posts, subscriptions, billing, profile management, "
        "dashboard analytics, comments, likes, notifications, "
        "login, passwords, and general blog-related questions."
    )
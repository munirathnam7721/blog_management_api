import json
import requests
import plotly.graph_objects as go

from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    ALL,
    no_update,
)

from django_plotly_dash import DjangoDash


app = DjangoDash("UserDashboard")


# ============================================================
# COMMON STYLES
# ============================================================

PAGE_STYLE = {
    "backgroundColor": "#f5f7fb",
    "minHeight": "100vh",
    "padding": "20px",
    "fontFamily": "Arial, sans-serif",
}


CARD_STYLE = {
    "backgroundColor": "white",
    "padding": "20px",
    "borderRadius": "12px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
    "textAlign": "center",
    "flex": "1",
    "minWidth": "200px",
}


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_token(request):

    if request is None:
        return None

    return request.session.get("fastapi_jwt")


# ============================================================
# DASHBOARD LAYOUT
# ============================================================

app.layout = html.Div(
    style=PAGE_STYLE,
    children=[

        # ====================================================
        # HEADER
        # ====================================================

        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "backgroundColor": "white",
                "padding": "15px 25px",
                "borderRadius": "12px",
                "marginBottom": "20px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
                "position": "relative",
            },
            children=[

                # --------------------------------------------
                # DASHBOARD TITLE
                # --------------------------------------------

                html.Div(
                    children=[

                        html.H2(
                            "Blog Dashboard",
                            style={
                                "margin": "0",
                                "color": "#222",
                            },
                        ),

                        html.P(
                            "Welcome to your dashboard",
                            style={
                                "margin": "5px 0 0 0",
                                "color": "#777",
                            },
                        ),
                    ]
                ),

                # --------------------------------------------
                # NOTIFICATION CENTER
                # --------------------------------------------

                html.Div(
                    style={
                        "position": "relative",
                    },
                    children=[

                        # ------------------------------------
                        # BELL
                        # ------------------------------------

                        html.Button(
                            "🔔",
                            id="notification-bell",
                            n_clicks=0,
                            style={
                                "fontSize": "28px",
                                "border": "none",
                                "background": "transparent",
                                "cursor": "pointer",
                                "position": "relative",
                            },
                        ),

                        # ------------------------------------
                        # UNREAD BADGE
                        # ------------------------------------

                        html.Span(
                            "0",
                            id="notification-badge",
                            style={
                                "position": "absolute",
                                "top": "-2px",
                                "right": "-2px",
                                "backgroundColor": "red",
                                "color": "white",
                                "borderRadius": "50%",
                                "minWidth": "20px",
                                "height": "20px",
                                "fontSize": "12px",
                                "fontWeight": "bold",
                                "display": "none",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "textAlign": "center",
                                "lineHeight": "20px",
                            },
                        ),

                        # ------------------------------------
                        # DROPDOWN
                        # ------------------------------------

                        html.Div(
                            id="notification-dropdown",
                            style={
                                "display": "none",
                                "position": "absolute",
                                "right": "0",
                                "top": "45px",
                                "width": "380px",
                                "maxHeight": "500px",
                                "overflowY": "auto",
                                "backgroundColor": "white",
                                "borderRadius": "12px",
                                "boxShadow": "0 5px 20px rgba(0,0,0,0.15)",
                                "zIndex": "9999",
                                "border": "1px solid #eee",
                            },
                            children=[

                                # ============================
                                # DROPDOWN HEADER
                                # ============================

                                html.Div(
                                    style={
                                        "padding": "15px",
                                        "borderBottom": "1px solid #eee",
                                        "display": "flex",
                                        "justifyContent": "space-between",
                                        "alignItems": "center",
                                    },
                                    children=[

                                        html.Strong(
                                            "Notifications",
                                            style={
                                                "fontSize": "18px",
                                            },
                                        ),

                                        html.Button(
                                            "Mark all as read",
                                            id="mark-all-read",
                                            n_clicks=0,
                                            style={
                                                "border": "none",
                                                "background": "transparent",
                                                "color": "#007bff",
                                                "cursor": "pointer",
                                                "fontSize": "12px",
                                            },
                                        ),
                                    ],
                                ),

                                # ============================
                                # NOTIFICATION CONTENT
                                # ============================

                                html.Div(
                                    id="notification-content",
                                    children=[],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),

        # ====================================================
        # DASHBOARD REFRESH
        # ====================================================

        dcc.Interval(
            id="dashboard-refresh",
            interval=10000,
            n_intervals=0,
        ),

        # ====================================================
        # NOTIFICATION REFRESH
        # ====================================================

        dcc.Interval(
            id="notification-refresh",
            interval=10000,
            n_intervals=0,
        ),

        # ====================================================
        # ACTION STORE
        # ====================================================

        dcc.Store(
            id="notification-action-store",
            data=0,
        ),

        # ====================================================
        # USER SECTION
        # ====================================================

        html.Div(
            id="user-section",
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "12px",
                "marginBottom": "20px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
            },
        ),

        # ====================================================
        # STATISTICS
        # ====================================================

        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
                "marginBottom": "25px",
            },
            children=[

                # --------------------------------------------
                # TOTAL POSTS
                # --------------------------------------------

                html.Div(
                    children=[

                        html.H4("Total Posts"),

                        html.H2(
                            id="total-posts",
                            children="0",
                        ),
                    ],
                    style=CARD_STYLE,
                ),

                # --------------------------------------------
                # TOTAL COMMENTS
                # --------------------------------------------

                html.Div(
                    children=[

                        html.H4("Total Comments"),

                        html.H2(
                            id="total-comments",
                            children="0",
                        ),
                    ],
                    style=CARD_STYLE,
                ),

                # --------------------------------------------
                # TOTAL LIKES
                # --------------------------------------------

                html.Div(
                    children=[

                        html.H4("Likes Received"),

                        html.H2(
                            id="total-likes",
                            children="0",
                        ),
                    ],
                    style=CARD_STYLE,
                ),

                # --------------------------------------------
                # TOTAL VIEWS
                # --------------------------------------------

                html.Div(
                    children=[

                        html.H4("Total Views"),

                        html.H2(
                            id="total-views",
                            children="0",
                        ),
                    ],
                    style=CARD_STYLE,
                ),
            ],
        ),

        # ====================================================
        # CHARTS
        # ====================================================

        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
            },
            children=[

                # --------------------------------------------
                # LIKES / COMMENTS
                # --------------------------------------------

                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "flex": "1",
                        "minWidth": "400px",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
                    },
                    children=[

                        html.H3(
                            "Likes and Comments"
                        ),

                        dcc.Graph(
                            id="likes-comments-chart"
                        ),
                    ],
                ),

                # --------------------------------------------
                # POST ACTIVITY
                # --------------------------------------------

                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "flex": "1",
                        "minWidth": "400px",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
                    },
                    children=[

                        html.H3(
                            "Post Activity"
                        ),

                        dcc.Graph(
                            id="post-activity-chart"
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# ============================================================
# DASHBOARD CALLBACK
# ============================================================

@app.expanded_callback(
    [
        Output(
            "user-section",
            "children",
        ),

        Output(
            "total-posts",
            "children",
        ),

        Output(
            "total-comments",
            "children",
        ),

        Output(
            "total-likes",
            "children",
        ),

        Output(
            "total-views",
            "children",
        ),

        Output(
            "likes-comments-chart",
            "figure",
        ),

        Output(
            "post-activity-chart",
            "figure",
        ),
    ],
    [
        Input(
            "dashboard-refresh",
            "n_intervals",
        ),
    ],
)
def update_dashboard(
    n_intervals,
    request=None,
):

    empty_figure = go.Figure()

    empty_figure.update_layout(
        template="plotly_white"
    )

    token = get_token(request)

    if not token:

        return (
            html.Div(
                "Please login to view dashboard.",
                style={
                    "color": "red",
                    "fontWeight": "bold",
                },
            ),
            "0",
            "0",
            "0",
            "0",
            empty_figure,
            empty_figure,
        )

    # ========================================================
    # GET DASHBOARD API
    # ========================================================

    try:

        response = requests.get(
            "http://127.0.0.1:8000/dashboard",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )

    except requests.RequestException:

        return (
            html.Div(
                "Unable to connect to FastAPI.",
                style={
                    "color": "red",
                    "fontWeight": "bold",
                },
            ),
            "0",
            "0",
            "0",
            "0",
            empty_figure,
            empty_figure,
        )

    if response.status_code != 200:

        return (
            html.Div(
                "Unable to load dashboard data.",
                style={
                    "color": "red",
                    "fontWeight": "bold",
                },
            ),
            "0",
            "0",
            "0",
            "0",
            empty_figure,
            empty_figure,
        )

    data = response.json()

    # ========================================================
    # DATA
    # ========================================================

    user = data.get(
        "user",
        {},
    )

    statistics = data.get(
        "statistics",
        {},
    )

    post_analytics = data.get(
        "post_analytics",
        [],
    )

    # ========================================================
    # USER
    # ========================================================

    user_section = html.Div(
        children=[

            html.H3(
                f"Welcome, {user.get('username', '')}"
            ),

            html.P(
                f"Email: {user.get('email', '')}"
            ),

            html.P(
                f"User ID: {user.get('id', '')}"
            ),
        ],
    )

    # ========================================================
    # STATISTICS
    # ========================================================

    total_posts = statistics.get(
        "total_posts",
        0,
    )

    total_comments = statistics.get(
        "total_comments",
        0,
    )

    total_likes = statistics.get(
        "total_likes_received",
        0,
    )

    total_views = statistics.get(
        "total_views",
        0,
    )

    # ========================================================
    # POST DATA
    # ========================================================

    titles = [
        post.get(
            "post_title",
            "",
        )
        for post in post_analytics
    ]

    likes = [
        post.get(
            "likes",
            0,
        )
        for post in post_analytics
    ]

    comments = [
        post.get(
            "comments",
            0,
        )
        for post in post_analytics
    ]

    dates = [
        post.get(
            "created_at",
        )
        for post in post_analytics
    ]

    post_counts = [
        1
        for _ in post_analytics
    ]

    # ========================================================
    # LIKES / COMMENTS CHART
    # ========================================================

    likes_comments_figure = go.Figure()

    likes_comments_figure.add_trace(
        go.Bar(
            x=titles,
            y=likes,
            name="Likes",
        )
    )

    likes_comments_figure.add_trace(
        go.Bar(
            x=titles,
            y=comments,
            name="Comments",
        )
    )

    likes_comments_figure.update_layout(
        barmode="group",
        template="plotly_white",
        xaxis_title="Posts",
        yaxis_title="Count",
    )

    # ========================================================
    # POST ACTIVITY CHART
    # ========================================================

    post_activity_figure = go.Figure()

    if dates:

        post_activity_figure.add_trace(
            go.Scatter(
                x=dates,
                y=post_counts,
                mode="lines+markers",
                name="Posts",
            )
        )

    post_activity_figure.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Posts",
    )

    return (
        user_section,
        str(total_posts),
        str(total_comments),
        str(total_likes),
        str(total_views),
        likes_comments_figure,
        post_activity_figure,
    )


# ============================================================
# NOTIFICATION CENTER
# ============================================================

@app.expanded_callback(
    [
        Output(
            "notification-content",
            "children",
        ),

        Output(
            "notification-badge",
            "children",
        ),

        Output(
            "notification-badge",
            "style",
        ),

        Output(
            "notification-dropdown",
            "style",
        ),
    ],
    [
        Input(
            "notification-refresh",
            "n_intervals",
        ),

        Input(
            "notification-bell",
            "n_clicks",
        ),

        Input(
            "notification-action-store",
            "data",
        ),
    ],
    [
        State(
            "notification-dropdown",
            "style",
        ),
    ],
)
def load_notifications(
    n_intervals,
    bell_clicks,
    action_refresh,
    current_dropdown_style,
    request=None,
    callback_context=None,
):

    # ========================================================
    # DEFAULT DROPDOWN STYLE
    # ========================================================

    if not current_dropdown_style:

        current_dropdown_style = {
            "display": "none",
            "position": "absolute",
            "right": "0",
            "top": "45px",
            "width": "380px",
            "maxHeight": "500px",
            "overflowY": "auto",
            "backgroundColor": "white",
            "borderRadius": "12px",
            "boxShadow": "0 5px 20px rgba(0,0,0,0.15)",
            "zIndex": "9999",
            "border": "1px solid #eee",
        }

    dropdown_style = {
        **current_dropdown_style
    }

    # ========================================================
    # HANDLE BELL CLICK
    #
    # IMPORTANT:
    # django-plotly-dash uses:
    #
    # callback_context.triggered
    #
    # NOT:
    #
    # callback_context.triggered_id
    # ========================================================

    if callback_context is not None:

        triggered = None

        if callback_context.triggered:

            prop_id = (
                callback_context.triggered[0]
                .get(
                    "prop_id",
                    "",
                )
            )

            if prop_id:

                triggered = (
                    prop_id
                    .split(".")[0]
                )

        if triggered == "notification-bell":

            current_display = (
                current_dropdown_style.get(
                    "display",
                    "none",
                )
            )

            if current_display == "none":

                dropdown_style["display"] = "block"

            else:

                dropdown_style["display"] = "none"

    # ========================================================
    # GET TOKEN
    # ========================================================

    token = get_token(request)

    if not token:

        return (
            html.Div(
                "Please login to view notifications.",
                style={
                    "padding": "20px",
                    "color": "#777",
                    "textAlign": "center",
                },
            ),
            "0",
            {
                "display": "none",
            },
            dropdown_style,
        )

    # ========================================================
    # GET NOTIFICATIONS
    # ========================================================

    try:

        response = requests.get(
            "http://127.0.0.1:8000/notifications",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )

    except requests.RequestException:

        return (
            html.Div(
                "Unable to load notifications.",
                style={
                    "padding": "20px",
                    "color": "red",
                    "textAlign": "center",
                },
            ),
            "0",
            {
                "display": "none",
            },
            dropdown_style,
        )

    if response.status_code != 200:

        return (
            html.Div(
                "Unable to load notifications.",
                style={
                    "padding": "20px",
                    "color": "red",
                    "textAlign": "center",
                },
            ),
            "0",
            {
                "display": "none",
            },
            dropdown_style,
        )

    notifications = response.json()

    # ========================================================
    # UNREAD COUNT
    # ========================================================

    unread_count = sum(
        1
        for notification in notifications
        if not notification.get(
            "is_read",
            False,
        )
    )

    # ========================================================
    # BADGE
    # ========================================================

    if unread_count > 0:

        badge_style = {
            "position": "absolute",
            "top": "-2px",
            "right": "-2px",
            "backgroundColor": "red",
            "color": "white",
            "borderRadius": "50%",
            "minWidth": "20px",
            "height": "20px",
            "fontSize": "12px",
            "fontWeight": "bold",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "textAlign": "center",
            "lineHeight": "20px",
        }

    else:

        badge_style = {
            "display": "none",
        }

    # ========================================================
    # NO NOTIFICATIONS
    # ========================================================

    if not notifications:

        notification_items = html.Div(
            "No notifications",
            style={
                "padding": "25px",
                "textAlign": "center",
                "color": "#777",
            },
        )

        return (
            notification_items,
            "0",
            badge_style,
            dropdown_style,
        )

    # ========================================================
    # ONLY SHOW 10 RECENT
    # ========================================================

    notifications = notifications[:10]

    notification_items = []

    # ========================================================
    # CREATE NOTIFICATION ITEMS
    # ========================================================

    for notification in notifications:

        notification_id = notification.get(
            "id"
        )

        message = notification.get(
            "message",
            "",
        )

        notification_type = notification.get(
            "notification_type",
            "",
        )

        is_read = notification.get(
            "is_read",
            False,
        )

        created_at = notification.get(
            "created_at",
            "",
        )

        # ====================================================
        # ICON
        # ====================================================

        if notification_type == "like":

            icon = "❤️"

        elif notification_type == "comment":

            icon = "💬"

        elif notification_type == "subscription":

            icon = "⭐"

        elif notification_type == "subscription_renewal":

            icon = "🔄"

        else:

            icon = "🔔"

        # ====================================================
        # UNREAD STYLE
        # ====================================================

        if is_read:

            background_color = "#ffffff"

            font_weight = "normal"

        else:

            background_color = "#eef5ff"

            font_weight = "bold"

        # ====================================================
        # BUTTON TEXT
        # ====================================================

        if is_read:

            status_text = "Mark as unread"

        else:

            status_text = "Mark as read"

        # ====================================================
        # NOTIFICATION ITEM
        # ====================================================

        notification_items.append(

            html.Div(
                style={
                    "padding": "12px",
                    "borderBottom": "1px solid #eee",
                    "backgroundColor": background_color,
                },

                children=[

                    html.Div(
                        style={
                            "display": "flex",
                            "gap": "10px",
                            "alignItems": "flex-start",
                        },

                        children=[

                            # --------------------------------
                            # ICON
                            # --------------------------------

                            html.Div(
                                icon,
                                style={
                                    "fontSize": "22px",
                                    "width": "30px",
                                },
                            ),

                            # --------------------------------
                            # CONTENT
                            # --------------------------------

                            html.Div(
                                style={
                                    "flex": "1",
                                },

                                children=[

                                    # MESSAGE
                                    html.Div(
                                        message,
                                        style={
                                            "fontWeight": font_weight,
                                            "fontSize": "14px",
                                            "color": "#222",
                                            "marginBottom": "5px",
                                        },
                                    ),

                                    # TIMESTAMP
                                    html.Div(
                                        created_at,
                                        style={
                                            "fontSize": "11px",
                                            "color": "#888",
                                            "marginBottom": "7px",
                                        },
                                    ),

                                    # --------------------------------
                                    # READ / UNREAD BUTTON
                                    #
                                    # IMPORTANT:
                                    # We use n_clicks_timestamp
                                    # instead of n_clicks.
                                    # --------------------------------

                                    html.Button(
                                        status_text,

                                        id={
                                            "type":
                                                "notification-action",

                                            "notification_id":
                                                notification_id,
                                        },

                                        n_clicks=0,

                                        n_clicks_timestamp=None,

                                        style={
                                            "border": "none",
                                            "background": "transparent",
                                            "padding": "0",
                                            "color": "#007bff",
                                            "cursor": "pointer",
                                            "fontSize": "11px",
                                        },
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            )
        )

    return (
        notification_items,
        str(unread_count),
        badge_style,
        dropdown_style,
    )


# ============================================================
# INDIVIDUAL NOTIFICATION READ / UNREAD
#
# IMPORTANT FIX:
# Use n_clicks_timestamp instead of n_clicks.
#
# This prevents automatic dashboard refreshes from being
# interpreted as user clicks.
# ============================================================

@app.expanded_callback(
    Output(
        "notification-action-store",
        "data",
    ),

    [
        Input(
            {
                "type": "notification-action",
                "notification_id": ALL,
            },
            "n_clicks_timestamp",
        ),
    ],

    State(
        "notification-action-store",
        "data",
    ),

    prevent_initial_call=True,
)
def change_notification_status(
    n_clicks_timestamp,
    current_value,
    request=None,
    callback_context=None,
):

    # ========================================================
    # NO TIMESTAMP = NO REAL CLICK
    # ========================================================

    if not n_clicks_timestamp:

        return no_update

    # ========================================================
    # MAKE SURE AT LEAST ONE BUTTON WAS ACTUALLY CLICKED
    # ========================================================

    valid_timestamps = [
        timestamp
        for timestamp in n_clicks_timestamp
        if timestamp is not None
        and timestamp > 0
    ]

    if not valid_timestamps:

        return no_update

    # ========================================================
    # CALLBACK CONTEXT
    # ========================================================

    if callback_context is None:

        return no_update

    if not callback_context.triggered:

        return no_update

    # ========================================================
    # GET TRIGGERED PROPERTY
    # ========================================================

    prop_id = (
        callback_context.triggered[0]
        .get(
            "prop_id",
            "",
        )
    )

    if not prop_id:

        return no_update

    # ========================================================
    # EXTRACT JSON ID
    #
    # Example:
    #
    # {"notification_id":5,"type":"notification-action"}.n_clicks_timestamp
    # ========================================================

    triggered_id_string = (
        prop_id.rsplit(
            ".",
            1,
        )[0]
    )

    try:

        triggered = json.loads(
            triggered_id_string
        )

    except (
        json.JSONDecodeError,
        TypeError,
        ValueError,
    ):

        return no_update

    # ========================================================
    # CHECK DICTIONARY
    # ========================================================

    if not isinstance(
        triggered,
        dict,
    ):

        return no_update

    # ========================================================
    # GET NOTIFICATION ID
    # ========================================================

    notification_id = triggered.get(
        "notification_id"
    )

    if not notification_id:

        return no_update

    # ========================================================
    # GET TOKEN
    # ========================================================

    token = get_token(request)

    if not token:

        return no_update

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # ========================================================
    # GET CURRENT NOTIFICATIONS
    # ========================================================

    try:

        response = requests.get(
            "http://127.0.0.1:8000/notifications",
            headers=headers,
            timeout=10,
        )

    except requests.RequestException:

        return no_update

    if response.status_code != 200:

        return no_update

    notifications = response.json()

    # ========================================================
    # FIND SELECTED NOTIFICATION
    # ========================================================

    selected_notification = None

    for notification in notifications:

        if notification.get(
            "id"
        ) == notification_id:

            selected_notification = notification

            break

    if selected_notification is None:

        return no_update

    # ========================================================
    # DETERMINE READ / UNREAD
    # ========================================================

    if selected_notification.get(
        "is_read",
        False,
    ):

        endpoint = (
            "http://127.0.0.1:8000/"
            f"notifications/"
            f"{notification_id}/unread"
        )

    else:

        endpoint = (
            "http://127.0.0.1:8000/"
            f"notifications/"
            f"{notification_id}/read"
        )

    # ========================================================
    # UPDATE FASTAPI
    # ========================================================

    try:

        update_response = requests.patch(
            endpoint,
            headers=headers,
            timeout=10,
        )

    except requests.RequestException:

        return no_update

    if update_response.status_code != 200:

        return no_update

    # ========================================================
    # TRIGGER NOTIFICATION REFRESH
    # ========================================================

    if current_value is None:

        current_value = 0

    return current_value + 1


# ============================================================
# MARK ALL NOTIFICATIONS AS READ
# ============================================================

@app.expanded_callback(
    Output(
        "notification-action-store",
        "data",
        allow_duplicate=True,
    ),

    Input(
        "mark-all-read",
        "n_clicks",
    ),

    State(
        "notification-action-store",
        "data",
    ),

    prevent_initial_call=True,
)
def mark_all_notifications_as_read(
    n_clicks,
    current_value,
    request=None,
):

    # ========================================================
    # NO CLICK
    # ========================================================

    if not n_clicks:

        return no_update

    # ========================================================
    # GET TOKEN
    # ========================================================

    token = get_token(request)

    if not token:

        return no_update

    # ========================================================
    # MARK ALL AS READ
    # ========================================================

    try:

        response = requests.patch(
            "http://127.0.0.1:8000/"
            "notifications/read-all",

            headers={
                "Authorization": f"Bearer {token}",
            },

            timeout=10,
        )

    except requests.RequestException:

        return no_update

    if response.status_code != 200:

        return no_update

    # ========================================================
    # TRIGGER REFRESH
    # ========================================================

    if current_value is None:

        current_value = 0

    return current_value + 1
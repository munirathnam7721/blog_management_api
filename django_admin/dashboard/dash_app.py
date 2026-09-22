import requests
import plotly.graph_objects as go

from datetime import datetime

from dash import html, dcc
from dash.dependencies import Input, Output

from django_plotly_dash import DjangoDash


app = DjangoDash(
    "UserDashboard"
)


# =========================================================
# DASHBOARD LAYOUT
# =========================================================

app.layout = html.Div(
    [

        # =================================================
        # MAIN CONTAINER
        # =================================================

        html.Div(
            [

                # =================================================
                # HEADER
                # =================================================

                html.Div(
                    [

                        html.H1(
                            "User Dashboard",
                            style={
                                "margin": "0",
                                "fontSize": "32px",
                                "fontWeight": "700"
                            }
                        ),

                        html.P(
                            "Blog Management Analytics",
                            style={
                                "margin": "5px 0 0 0",
                                "fontSize": "16px",
                                "color": "#666"
                            }
                        )

                    ],

                    style={
                        "marginBottom": "30px"
                    }
                ),


                # =================================================
                # AUTO REFRESH
                # =================================================

                dcc.Interval(
                    id="dashboard-refresh",
                    interval=60000,
                    n_intervals=0
                ),


                # =================================================
                # USER INFORMATION
                # =================================================

                html.Div(
                    id="dashboard-user",
                    style={
                        "marginBottom": "20px"
                    }
                ),


                # =================================================
                # STATISTICS CARDS
                # =================================================

                html.Div(
                    id="dashboard-data",

                    style={
                        "display": "grid",
                        "gridTemplateColumns":
                            "repeat(4, 1fr)",
                        "gap": "20px",
                        "marginBottom": "30px"
                    }
                ),


                # =================================================
                # LIKES & COMMENTS BAR CHART
                # =================================================

                html.Div(
                    [

                        dcc.Graph(
                            id="likes-comments-chart",
                            style={
                                "width": "100%"
                            }
                        )

                    ],

                    style={
                        "backgroundColor": "white",
                        "borderRadius": "12px",
                        "padding": "20px",
                        "boxShadow":
                            "0 2px 10px rgba(0,0,0,0.08)",
                        "marginBottom": "30px"
                    }
                ),


                # =================================================
                # POST ACTIVITY LINE CHART
                # =================================================

                html.Div(
                    [

                        dcc.Graph(
                            id="post-activity-chart",
                            style={
                                "width": "100%"
                            }
                        )

                    ],

                    style={
                        "backgroundColor": "white",
                        "borderRadius": "12px",
                        "padding": "20px",
                        "boxShadow":
                            "0 2px 10px rgba(0,0,0,0.08)",
                        "marginBottom": "30px"
                    }
                ),

            ],

            style={
                "maxWidth": "1200px",
                "margin": "0 auto",
                "padding": "30px",
                "fontFamily":
                    "Arial, sans-serif",
                "backgroundColor":
                    "#f5f7fb",
                "minHeight": "100vh"
            }
        )

    ]
)


# =========================================================
# DASHBOARD CALLBACK
# =========================================================

@app.expanded_callback(
    [

        Output(
            "dashboard-data",
            "children"
        ),

        Output(
            "likes-comments-chart",
            "figure"
        ),

        Output(
            "post-activity-chart",
            "figure"
        ),

        Output(
            "dashboard-user",
            "children"
        ),

    ],

    [

        Input(
            "dashboard-refresh",
            "n_intervals"
        )

    ]
)
def load_dashboard_data(
    n_intervals,
    request=None
):

    # =====================================================
    # GET JWT FROM DJANGO SESSION
    # =====================================================

    token = request.session.get(
        "fastapi_jwt"
    )

    if not token:

        return (
            html.P(
                "JWT token not found in Django session."
            ),
            {},
            {},
            ""
        )


    # =====================================================
    # CALL FASTAPI DASHBOARD API
    # =====================================================

    try:

        response = requests.get(
            "http://127.0.0.1:8000/dashboard",

            headers={
                "Authorization":
                    f"Bearer {token}"
            },

            timeout=10
        )

    except requests.RequestException as error:

        return (
            html.P(
                f"Could not connect to FastAPI: {error}"
            ),
            {},
            {},
            ""
        )


    # =====================================================
    # CHECK API RESPONSE
    # =====================================================

    if response.status_code != 200:

        return (
            html.Div(
                [

                    html.P(
                        f"FastAPI returned status "
                        f"{response.status_code}"
                    ),

                    html.Pre(
                        response.text
                    )

                ]
            ),
            {},
            {},
            ""
        )


    # =====================================================
    # READ API DATA
    # =====================================================

    data = response.json()

    statistics = data["statistics"]

    post_analytics = data["post_analytics"]


    # =====================================================
    # USER INFORMATION
    # =====================================================

    username = data["user"]["username"]


    user_section = html.Div(
        [

            html.H2(
                f"Welcome, {username}",

                style={
                    "margin": "0",
                    "fontSize": "24px"
                }
            ),

            html.P(
                "Here is your blog performance overview.",

                style={
                    "marginTop": "5px",
                    "color": "#666"
                }
            )

        ]
    )


    # =====================================================
    # STATISTIC CARD STYLE
    # =====================================================

    card_style = {

        "backgroundColor": "white",

        "borderRadius": "12px",

        "padding": "20px",

        "boxShadow":
            "0 2px 10px rgba(0,0,0,0.08)",

        "textAlign": "center",

        "minHeight": "110px",

        "display": "flex",

        "flexDirection": "column",

        "justifyContent": "center"

    }


    # =====================================================
    # STATISTICS CARDS
    # =====================================================

    dashboard_cards = [

        # -----------------------------------------------
        # TOTAL POSTS
        # -----------------------------------------------

        html.Div(
            [

                html.P(
                    "Total Posts",

                    style={
                        "margin": "0",
                        "fontSize": "15px",
                        "color": "#666"
                    }
                ),

                html.H2(
                    statistics["total_posts"],

                    style={
                        "margin": "10px 0 0 0",
                        "fontSize": "32px"
                    }
                )

            ],

            style=card_style
        ),


        # -----------------------------------------------
        # COMMENTS
        # -----------------------------------------------

        html.Div(
            [

                html.P(
                    "Comments Made",

                    style={
                        "margin": "0",
                        "fontSize": "15px",
                        "color": "#666"
                    }
                ),

                html.H2(
                    statistics["total_comments"],

                    style={
                        "margin": "10px 0 0 0",
                        "fontSize": "32px"
                    }
                )

            ],

            style=card_style
        ),


        # -----------------------------------------------
        # LIKES
        # -----------------------------------------------

        html.Div(
            [

                html.P(
                    "Likes Received",

                    style={
                        "margin": "0",
                        "fontSize": "15px",
                        "color": "#666"
                    }
                ),

                html.H2(
                    statistics["total_likes_received"],

                    style={
                        "margin": "10px 0 0 0",
                        "fontSize": "32px"
                    }
                )

            ],

            style=card_style
        ),


        # -----------------------------------------------
        # VIEWS
        # -----------------------------------------------

        html.Div(
            [

                html.P(
                    "Total Views",

                    style={
                        "margin": "0",
                        "fontSize": "15px",
                        "color": "#666"
                    }
                ),

                html.H2(
                    statistics["total_views"],

                    style={
                        "margin": "10px 0 0 0",
                        "fontSize": "32px"
                    }
                )

            ],

            style=card_style
        )

    ]


    # =====================================================
    # PREPARE BAR CHART DATA
    # =====================================================

    post_titles = [

        post["post_title"]

        for post in post_analytics

    ]


    likes = [

        post["likes"]

        for post in post_analytics

    ]


    comments = [

        post["comments"]

        for post in post_analytics

    ]


    # =====================================================
    # LIKES & COMMENTS BAR CHART
    # =====================================================

    bar_figure = go.Figure()


    bar_figure.add_trace(
        go.Bar(
            x=post_titles,
            y=likes,
            name="Likes"
        )
    )


    bar_figure.add_trace(
        go.Bar(
            x=post_titles,
            y=comments,
            name="Comments"
        )
    )


    bar_figure.update_layout(

        barmode="group",

        title={
            "text":
                "Likes & Comments Per Post",
            "x": 0.5
        },

        xaxis_title="Post",

        yaxis_title="Count",

        legend_title="Engagement",

        height=450,

        margin={
            "l": 50,
            "r": 30,
            "t": 80,
            "b": 80
        },

        plot_bgcolor="white",

        paper_bgcolor="white"

    )


    # =====================================================
    # PREPARE POST ACTIVITY DATA
    # =====================================================

    activity_dates = []

    activity_counts = []


    for post in post_analytics:

        created_at = post["created_at"]

        # Convert API date string to datetime
        if created_at:

            try:

                created_date = datetime.fromisoformat(
                    created_at
                )

                activity_dates.append(
                    created_date
                )

                activity_counts.append(
                    1
                )

            except ValueError:

                continue


    # =====================================================
    # SORT POST ACTIVITY BY DATE
    # =====================================================

    activity_data = sorted(
        zip(
            activity_dates,
            activity_counts
        )
    )


    if activity_data:

        activity_dates = [
            item[0]
            for item in activity_data
        ]

        activity_counts = [
            item[1]
            for item in activity_data
        ]

    else:

        activity_dates = []

        activity_counts = []


    # =====================================================
    # POST ACTIVITY LINE CHART
    # =====================================================

    activity_figure = go.Figure()


    activity_figure.add_trace(
        go.Scatter(

            x=activity_dates,

            y=activity_counts,

            mode="lines+markers",

            name="Posts Created"

        )
    )


    activity_figure.update_layout(

        title={
            "text":
                "Post Activity Over Time",
            "x": 0.5
        },

        xaxis_title="Date",

        yaxis_title="Posts Created",

        height=450,

        margin={
            "l": 50,
            "r": 30,
            "t": 80,
            "b": 80
        },

        plot_bgcolor="white",

        paper_bgcolor="white"

    )


    # =====================================================
    # RETURN ALL DASHBOARD DATA
    # =====================================================

    return (

        dashboard_cards,

        bar_figure,

        activity_figure,

        user_section

    )
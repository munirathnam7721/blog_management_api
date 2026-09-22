from django.contrib import admin
from django.urls import path, include

from dashboard import dash_app

from dashboard.views import (
    home,
    login_view,
    dashboard_login
)


urlpatterns = [

    # ========================================================
    # DJANGO ADMIN
    # ========================================================

    path(
        "admin/",
        admin.site.urls
    ),

    # ========================================================
    # DJANGO PLOTLY DASH
    # ========================================================

    path(
        "django_plotly_dash/",
        include(
            "django_plotly_dash.urls"
        )
    ),

    # ========================================================
    # LOGIN
    # ========================================================

    path(
        "login/",
        login_view,
        name="login"
    ),

    # ========================================================
    # OLD DASHBOARD LOGIN
    # ========================================================

    path(
        "dashboard-login/",
        dashboard_login,
        name="dashboard_login"
    ),

    # ========================================================
    # HOME PAGE
    # ========================================================

    path(
        "",
        home,
        name="home"
    ),

]
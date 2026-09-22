import requests

from django.http import JsonResponse
from django.shortcuts import render, redirect


# ============================================================
# DJANGO HOME PAGE
# ============================================================

def home(request):

    return render(
        request,
        "dashboard/home.html"
    )


# ============================================================
# LOGIN PAGE
# ============================================================

def login_view(request):

    # --------------------------------------------------------
    # SHOW LOGIN PAGE
    # --------------------------------------------------------

    if request.method == "GET":

        return render(
            request,
            "dashboard/login.html"
        )

    # --------------------------------------------------------
    # GET LOGIN DETAILS
    # --------------------------------------------------------

    email = request.POST.get("email")
    password = request.POST.get("password")

    # --------------------------------------------------------
    # VALIDATE INPUT
    # --------------------------------------------------------

    if not email or not password:

        return render(
            request,
            "dashboard/login.html",
            {
                "error": "Email and password are required."
            }
        )

    # --------------------------------------------------------
    # CALL FASTAPI LOGIN
    # --------------------------------------------------------

    try:

        response = requests.post(
            "http://127.0.0.1:8000/auth/login",

            json={
                "email": email,
                "password": password
            },

            timeout=10
        )

    except requests.RequestException as error:

        return render(
            request,
            "dashboard/login.html",
            {
                "error":
                    f"Could not connect to FastAPI: {error}"
            }
        )

    # --------------------------------------------------------
    # CHECK FASTAPI LOGIN RESPONSE
    # --------------------------------------------------------

    if response.status_code != 200:

        try:

            error_data = response.json()

            error_message = error_data.get(
                "detail",
                "Invalid email or password."
            )

        except ValueError:

            error_message = "Invalid email or password."

        return render(
            request,
            "dashboard/login.html",
            {
                "error": error_message
            }
        )

    # --------------------------------------------------------
    # GET JWT TOKEN
    # --------------------------------------------------------

    try:

        data = response.json()

    except ValueError:

        return render(
            request,
            "dashboard/login.html",
            {
                "error":
                    "Invalid response received from FastAPI."
            }
        )

    token = data.get("access_token")

    # --------------------------------------------------------
    # CHECK TOKEN
    # --------------------------------------------------------

    if not token:

        return render(
            request,
            "dashboard/login.html",
            {
                "error":
                    "Login successful, but JWT token was not received."
            }
        )

    # --------------------------------------------------------
    # IMPORTANT:
    # REMOVE OLD JWT
    # --------------------------------------------------------

    request.session.pop(
        "fastapi_jwt",
        None
    )

    # --------------------------------------------------------
    # STORE NEW USER JWT
    # --------------------------------------------------------

    request.session["fastapi_jwt"] = token

    request.session.modified = True

    # --------------------------------------------------------
    # REDIRECT TO DASHBOARD
    # --------------------------------------------------------

    return redirect(
        "/django_plotly_dash/app/UserDashboard/"
    )


# ============================================================
# OLD DASHBOARD LOGIN
# ============================================================

def dashboard_login(request):

    token = request.GET.get("token")

    if not token:

        return JsonResponse(
            {
                "error": "JWT token is required"
            },
            status=400
        )

    request.session["fastapi_jwt"] = token

    request.session.modified = True

    return JsonResponse(
        {
            "message":
                "JWT stored successfully in Django session",

            "session_key":
                request.session.session_key
        }
    )
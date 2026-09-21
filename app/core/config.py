# import os

# from dotenv import load_dotenv


# load_dotenv()


# DATABASE_URL = os.getenv(
#     "DATABASE_URL"
# )

# SECRET_KEY = os.getenv(
#     "SECRET_KEY",
#     "change-this-secret-key"
# )

# ALGORITHM = os.getenv(
#     "ALGORITHM",
#     "HS256"
# )

# ACCESS_TOKEN_EXPIRE_MINUTES = int(
#     os.getenv(
#         "ACCESS_TOKEN_EXPIRE_MINUTES",
#         "60"
#     )
# )


# SMTP_SERVER = os.getenv(
#     "SMTP_SERVER",
#     "smtp.gmail.com"
# )

# SMTP_PORT = int(
#     os.getenv(
#         "SMTP_PORT",
#         "587"
#     )
# )

# SMTP_USERNAME = os.getenv(
#     "SMTP_USERNAME",
#     ""
# )

# SMTP_PASSWORD = os.getenv(
#     "SMTP_PASSWORD",
#     ""
# )


import os

from dotenv import load_dotenv


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# DATABASE
# ==========================================

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# JWT AUTHENTICATION
# ==========================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-this-secret-key"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "60"
    )
)


# ==========================================
# SMTP / EMAIL CONFIGURATION
# ==========================================

SMTP_SERVER = os.getenv(
    "SMTP_HOST",
    "smtp.gmail.com"
)

SMTP_PORT = int(
    os.getenv(
        "SMTP_PORT",
        "587"
    )
)

SMTP_USERNAME = os.getenv(
    "SMTP_USERNAME",
    ""
)

SMTP_PASSWORD = os.getenv(
    "SMTP_PASSWORD",
    ""
)

SMTP_FROM_EMAIL = os.getenv(
    "SMTP_FROM_EMAIL",
    SMTP_USERNAME
)

SMTP_FROM_NAME = os.getenv(
    "SMTP_FROM_NAME",
    "Blog Management API"
)
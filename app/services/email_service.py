import logging
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_FROM_EMAIL,
    SMTP_FROM_NAME,
)


# ==========================================
# LOGGER
# ==========================================

logger = logging.getLogger(__name__)


# ==========================================
# SEND EMAIL
# ==========================================

def send_email(
    recipient: str,
    subject: str,
    body: str
):
    """
    Send an email using SMTP.

    This function can be used with
    FastAPI BackgroundTasks.
    """

    # ==========================================
    # CHECK SMTP CONFIGURATION
    # ==========================================

    if not SMTP_USERNAME or not SMTP_PASSWORD:

        logger.warning(
            "SMTP credentials are not configured."
        )

        return

    # ==========================================
    # CREATE EMAIL
    # ==========================================

    message = MIMEMultipart()

    message["From"] = (
        f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
    )

    message["To"] = recipient

    message["Subject"] = subject

    message.attach(
        MIMEText(
            body,
            "plain"
        )
    )

    # ==========================================
    # SEND EMAIL
    # ==========================================

    try:

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        ) as server:

            # Enable TLS
            server.starttls()

            # Login to SMTP server
            server.login(
                SMTP_USERNAME,
                SMTP_PASSWORD
            )

            # Send email
            server.sendmail(
                SMTP_FROM_EMAIL,
                recipient,
                message.as_string()
            )

        logger.info(
            "Email sent successfully to %s",
            recipient
        )

    except Exception as error:

        logger.error(
            "Email sending failed: %s",
            error
        )
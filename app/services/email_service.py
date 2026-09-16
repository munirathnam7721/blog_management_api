import smtplib

from email.mime.multipart import (
    MIMEMultipart
)

from email.mime.text import MIMEText

from app.core.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD
)


def send_email(
    recipient: str,
    subject: str,
    body: str
):

    # Email settings not configured
    if not SMTP_USERNAME or not SMTP_PASSWORD:

        print(
            "SMTP credentials are not configured."
        )

        return

    message = MIMEMultipart()

    message["From"] = SMTP_USERNAME

    message["To"] = recipient

    message["Subject"] = subject

    message.attach(
        MIMEText(
            body,
            "plain"
        )
    )

    try:

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        ) as server:

            server.starttls()

            server.login(
                SMTP_USERNAME,
                SMTP_PASSWORD
            )

            server.sendmail(
                SMTP_USERNAME,
                recipient,
                message.as_string()
            )

        print(
            "Email sent successfully."
        )

    except Exception as error:

        print(
            f"Email sending failed: {error}"
        )
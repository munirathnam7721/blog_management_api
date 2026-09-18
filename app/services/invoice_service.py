import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


INVOICE_DIR = "media/invoices"

os.makedirs(INVOICE_DIR, exist_ok=True)


def generate_invoice(
    user,
    subscription,
    billing,
    plan
):
    """
    Generate an invoice PDF for a subscription.
    """

    # Create invoice filename
    filename = f"invoice_{billing.transaction_id}.pdf"

    # Full file path
    file_path = os.path.join(
        INVOICE_DIR,
        filename
    )

    # Create PDF
    pdf = canvas.Canvas(
        file_path,
        pagesize=A4
    )

    width, height = A4

    # --------------------------------------------------
    # Invoice heading
    # --------------------------------------------------

    pdf.setFont("Helvetica-Bold", 20)

    pdf.drawString(
        50,
        height - 60,
        "BLOG MANAGEMENT API"
    )

    pdf.setFont("Helvetica-Bold", 16)

    pdf.drawString(
        50,
        height - 100,
        "SUBSCRIPTION INVOICE"
    )

    # --------------------------------------------------
    # Invoice details
    # --------------------------------------------------

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        50,
        height - 140,
        f"Transaction ID: {billing.transaction_id}"
    )

    pdf.drawString(
        50,
        height - 160,
        f"Billing Date: {billing.billing_date.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # --------------------------------------------------
    # User details
    # --------------------------------------------------

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        50,
        height - 210,
        "Customer Details"
    )

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        50,
        height - 230,
        f"Username: {user.username}"
    )

    pdf.drawString(
        50,
        height - 250,
        f"Email: {user.email}"
    )

    # --------------------------------------------------
    # Subscription details
    # --------------------------------------------------

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        50,
        height - 300,
        "Subscription Details"
    )

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        50,
        height - 320,
        f"Plan: {plan.name}"
    )

    pdf.drawString(
        50,
        height - 340,
        f"Price: Rs. {billing.amount}"
    )

    pdf.drawString(
        50,
        height - 360,
        f"Start Date: {subscription.start_date.strftime('%Y-%m-%d')}"
    )

    pdf.drawString(
        50,
        height - 380,
        f"End Date: {subscription.end_date.strftime('%Y-%m-%d')}"
    )

    pdf.drawString(
        50,
        height - 400,
        f"Payment Status: {billing.payment_status}"
    )

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------

    pdf.setFont("Helvetica-Bold", 11)

    pdf.drawString(
        50,
        height - 450,
        "Thank you for subscribing!"
    )

    # Finish PDF
    pdf.save()

    # Return database path
    invoice_path = f"/media/invoices/{filename}"

    return invoice_path
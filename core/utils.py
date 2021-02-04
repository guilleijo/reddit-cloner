from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def send_contact_email(data):
    name = data.get("name")
    from_email = data.get("from_email")
    message = data.get("message")

    subject = "Reddit cloner"
    context = {
        "name": name,
        "from_email": from_email,
        "message": message,
    }

    html_message = render_to_string("email.html", context)
    email_msg = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.EMAIL_TO],
    )
    email_msg.content_subtype = "html"
    email_msg.send()

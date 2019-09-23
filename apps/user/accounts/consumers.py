from channels.consumer import SyncConsumer
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.conf import settings

from apps.user.authorisation.tokens import account_activation_token


class ConfirmationEmailConsumer(SyncConsumer):
    def send_email(self, message):
        print("ConfirmationEmailConsumer.send_email")
        print(message)
        user = get_user_model().objects.get(id=message["user_id"])

        mail_subject = "Activate your blog account."
        message = render_to_string(
            "emails/active_email.html",
            {
                "user": user,
                "domain": settings.DOMAIN,
                "uid": user.pk,
                "token": account_activation_token.make_token(user),
            },
        )

        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

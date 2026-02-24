import os
from django.dispatch import receiver
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # Construct the password reset URL
    #
    reset_url = f"http://localhost:5173/reset-password?token={reset_password_token.key}"

    message = f"Hello,\n\nYou requested a password reset. Use the link below:\n\n{reset_url}\n\nIf you didn't request this, ignore this email."

    send_mail(
        subject="Password Reset Request",
        message=message,
        from_email="noreply@issue-reporting.com",
        recipient_list=[reset_password_token.user.email],
        fail_silently=False,
    )
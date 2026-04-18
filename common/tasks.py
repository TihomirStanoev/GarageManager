from celery import shared_task
from django.core.mail import  send_mail
from django.conf import settings

@shared_task
def send_mail_async(
        subject,
        message,
        recipient_list,
        from_email=None,
    ):
    print('foo bar!')
    send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        from_email=from_email or settings.DEFAULT_FROM_EMAIL,
    )


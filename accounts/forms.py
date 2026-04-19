import logging

from django.contrib.auth import get_user_model
import django.contrib.auth.forms as auth_forms
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from common.tasks import send_mail_async

User = get_user_model()
logger = logging.getLogger("django.contrib.auth")

class RegisterForm(auth_forms.BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number')



class LoginForm(auth_forms.AuthenticationForm):
    pass


class UpdateProfileForm(auth_forms.UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'last_login')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ('email', 'last_login'):
            self.fields[field].disabled = True



class GaragePasswordResetForm(auth_forms.PasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")
        try:
            send_mail_async.delay(
                subject=email_message.subject,
                message=email_message.body,
                recipient_list=[to_email]
            )
        except Exception:
            logger.exception(
                "Failed to send password reset email to %s", context["user"].pk
            )



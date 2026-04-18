from django.template.loader import render_to_string

from cars.models import Car
from common.tasks import send_mail_async



class CarNotificationMixin:
    template_add_car_owner_subject = None
    template_add_car_owner_message = None
    template_remove_car_owner_subject = None
    template_remove_car_owner_message = None


    def _send_car_notification(self, context, owner, subject_template, message_template):
        context['first_name'] = owner.first_name
        subject = render_to_string(subject_template, context)
        message = render_to_string(message_template, context)
        recipient = [owner.email]

        send_mail_async.delay(
            subject=subject,
            message=message,
            recipient_list=recipient
        )

    def form_valid(self, form):
        car_new_owner = form.cleaned_data.get('owner')
        car_old_owner = Car.objects.get(pk=self.object.pk).owner if self.object else None
        context = {**form.cleaned_data}

        if car_new_owner and not car_old_owner:
            self._send_car_notification(
                context=context,
                owner=car_new_owner,
                subject_template=self.template_add_car_owner_subject,
                message_template=self.template_add_car_owner_message
            )

        elif car_old_owner and not car_new_owner:
            self._send_car_notification(
                context=context,
                owner=car_old_owner,
                subject_template=self.template_remove_car_owner_subject,
                message_template=self.template_remove_car_owner_message
            )

        elif car_old_owner != car_new_owner:
            self._send_car_notification(
                context=context,
                owner=car_new_owner,
                subject_template=self.template_add_car_owner_subject,
                message_template=self.template_add_car_owner_message
            )
            self._send_car_notification(
                context=context,
                owner=car_old_owner,
                subject_template=self.template_remove_car_owner_subject,
                message_template=self.template_remove_car_owner_message
            )


        return super().form_valid(form)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .models import Appointment


@receiver(post_save, sender=Appointment)
def post_save_email_confirmation(sender, instance, created, *args, **kwargs):
    email = EmailMessage(
        'subject',
        'body',
        settings.EMAIL_HOST_USER,
        ['olujic.branko@gmail.com', ]  # Here goes secretary`s email.
    )
    email.fail_silently = True
    context = {
        'name': instance.name,
        'date': instance.date,
        'hour': instance.hour,
        'message': instance.message,
        'phone': instance.phone
    }

    if created:
        # Mail goes just to the secretary, to confirm day and hour with the customer
        template = render_to_string('appointment_requested.html', context)
        email.subject = 'New Appointment Request'
        email.body = template

    else:
        # After confirmation and saving to database, mail goes to the doctor with time and message
        template = render_to_string('appointment_confirmed.html', context)
        email.subject = 'New Appointment'
        email.body = template
        email.to = ['brolujay@gmail.com', ]  # Here goes doctor`s email.

    email.send()
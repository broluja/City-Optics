from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .models import Reply


@receiver(post_save, sender=Reply)
def post_save_email_sending(sender, instance, created, **kwargs):
    print(kwargs, sender)
    content = instance.content
    email_address = instance.message.mail
    customer = instance.message.name
    email = EmailMessage(
        'subject',
        'body',
        settings.EMAIL_HOST_USER,
        [email_address, ]
    )
    email.fail_silently = True

    context = {
        'customer': customer,
        'content': content,
    }

    if created:
        # Mail with response for customer
        template = render_to_string('reply.html', context)
        email.subject = 'Admin Reply'
        email.body = template
        email.send()

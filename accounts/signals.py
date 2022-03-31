from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .models import Customer

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def post_save_customer_creation(sender, instance, created, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Customer.objects.create(user=instance, email=instance.email)


@receiver(post_save, sender=Customer)
def post_save_code_sending(sender, instance, created, *args, **kwargs):
    email = EmailMessage(
        'subject',
        'body',
        settings.EMAIL_HOST_USER,
        (instance.email, )  # Here goes secretary`s email.
    )
    email.fail_silently = True
    context = {
        'name': instance.user.username,
        'date': instance.created_on,
        'code': instance.code,
    }
    if created:
        # Mail goes to the customer with the code for discount of 5%
        template = render_to_string('accounts/account_created.html', context)
        email.subject = 'Registration Successful'
        email.body = template
        email.send()


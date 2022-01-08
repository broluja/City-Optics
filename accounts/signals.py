from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer


@receiver(post_save, sender=User)
def pre_save_customer_creation(sender, instance, created, *args, **kwargs):
    if created:
        Customer.objects.create(user=instance, email=instance.email)


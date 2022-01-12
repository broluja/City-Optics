import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    email = models.CharField(max_length=55, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    discount_used = models.BooleanField(default=False)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.user.username

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save()
        value = f"{self.user.first_name} {self.user.last_name} {self.user.username}"
        if self.slug is None:
            self.slug = slugify(value)
            self.save()


class Coupon(models.Model):
    code = models.CharField(max_length=36)
    used_on = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(Customer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.code

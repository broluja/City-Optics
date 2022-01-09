import uuid

from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=55, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    discount_used = models.BooleanField(default=False)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=36)
    used_on = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(Customer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.code


from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=55, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    discount_used = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

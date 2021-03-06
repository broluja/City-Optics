import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    email = models.CharField(max_length=55, unique=True)
    phone = models.CharField(max_length=99, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    discount_used = models.BooleanField(default=False)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.user.username

    def __repr__(self):
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

    objects = models.Manager()


class Testimony(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    comment = models.TextField(max_length=555)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    image = models.ImageField(default='cat.jpg', upload_to='feedback_pics')

    def __str__(self):
        return self.customer.user.username

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Testimonies'




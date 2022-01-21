from django.db import models
from accounts.models import Customer


class Appointment(models.Model):

    HOURS = [
        ('9H', '9H - 10H'),
        ('10H', '10H - 11H'),
        ('11H', '11H - 12H'),
        ('12H', '12H - 13H'),
        ('13H', '13H - 14H'),
        ('14H', '14H - 15H'),
        ('15H', '15H - 16H'),
        ('16H', '16H - 17H')
    ]

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=33)
    email = models.EmailField(blank=True, null=True)
    hour = models.CharField(max_length=33, choices=HOURS)
    message = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.name} requests for: {self.date}, {self.hour}'


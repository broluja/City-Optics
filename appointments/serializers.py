from .models import Appointment

# Third party import
from rest_framework import serializers


class AppointmentSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = Appointment
        fields = ['id', 'name', 'phone', 'email', 'hour', 'date', 'customer']

    @staticmethod
    def get_full_name(model):
        if model.customer:
            customer = model.customer.user.username
        else:
            customer = 'Non-registered user'
        return customer

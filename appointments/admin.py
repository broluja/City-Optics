from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone', 'is_confirmed', 'id')
    list_per_page = 20
    ordering = ('date', )
    search_fields = ('date',)
    list_filter = ('date', 'hour')
    list_editable = ('is_confirmed', )



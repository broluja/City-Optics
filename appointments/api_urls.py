from django.urls import path
from . import views


urlpatterns = [
    path('get-appointments/', views.AppointmentAPIView.as_view(), name='get_appointments')
]
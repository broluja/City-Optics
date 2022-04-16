from django.urls import path
from . import views


urlpatterns = [
    path('get-appointments/', views.AppointmentAPIView.as_view(), name='get_appointments'),
    path('post-appointment/', views.post_appointment, name='post_appointments'),
    path('edit-appointment/', views.edit_appointment, name='edit_appointments'),
]

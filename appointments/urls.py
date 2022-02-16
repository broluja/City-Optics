from django.urls import path
from . import views


urlpatterns = [
    path('', views.appointment, name='appointment'),
    path('schedules/', views.schedules, name='schedules'),
    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
]

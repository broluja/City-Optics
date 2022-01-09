from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('logout/', views.CustomerLogoutView.as_view(), name='logout'),
    path('profile/<slug:slug>', views.profile, name='profile')
]

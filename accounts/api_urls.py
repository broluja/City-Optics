from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('get-customers/', views.CustomerAPIView.as_view(), name='get_customers'),
    path('get-coupons/', views.CouponAPIView.as_view(), name='get_coupons'),
    path('register/', views.registration_view, name='registration_api'),
    path('login/', obtain_auth_token, name='registration_api'),
]

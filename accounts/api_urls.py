from django.urls import path
from . import views


urlpatterns = [
    path('get-customers/', views.CustomerAPIView.as_view(), name='get_customers'),
    path('get-coupons/', views.CouponAPIView.as_view(), name='get_coupons'),
]

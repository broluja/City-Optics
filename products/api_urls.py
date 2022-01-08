from django.urls import path
from . import views


urlpatterns = [
    path('get-available-products/', views.ProductAPIView.as_view(), name='get_available_products'),
    path('get-orders/', views.OrderAPIView.as_view(), name='get_orders'),
    path('get-messages/', views.MessageAPIView.as_view(), name='get_messages')
]
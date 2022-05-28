from django.urls import path

from . import views


urlpatterns = [
    path('city-optics/', views.city_optics, name='city-optics'),
    path('products', views.home_products, name='products'),
    path('all-products/', views.ProductListView.as_view(), name='all_products'),
    path('product-detail/<str:pk>', views.details, name='product_details'),
    path('create/', views.create_product, name='create'),
    path('order/', views.order, name='order'),
    path('order/<str:pk>', views.order_specific, name='order_specific'),
    path('message/', views.get_message, name='message'),
]
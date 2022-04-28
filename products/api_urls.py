from django.urls import path
from . import views


urlpatterns = [
    path('get-available-products/', views.ProductAPIView.as_view()),
    path('post-new-product/', views.post_new_product_api),
    path('edit-product/', views.edit_product_api),
    path('delete-product/', views.delete_product_api),
    path('get-orders/', views.OrderAPIView.as_view()),
    path('get-messages/', views.MessageAPIView.as_view()),
    path('create-reply/', views.ReplyCreateAPIView.as_view())
]

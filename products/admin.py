from django.contrib import admin
from .models import Product, Order, Message


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'present')
    list_editable = ('present', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'phone', 'is_shipped')
    list_editable = ('is_shipped', )
    search_fields = ('product', )
    list_filter = ('product', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'mail', 'text_message', 'is_for_front_page')
    list_editable = ('is_for_front_page', )


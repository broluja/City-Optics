from django.contrib import admin
from .models import Product, Order, Message
from django.contrib.auth.models import User

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'customer', )
    list_display_links = ('username', 'customer')
    list_per_page = 10
    search_fields = ('username', 'first_name', 'last_name')
    readonly_fields = ('username', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'present')
    list_editable = ('present',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'phone', 'is_shipped', 'discount_approved')
    list_editable = ('is_shipped',)
    search_fields = ('product',)
    list_filter = ('product',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'mail', 'text_message', 'is_for_front_page')
    list_editable = ('is_for_front_page',)

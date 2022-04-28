from django.contrib import admin
from .models import Product, Order, Message, Reply
from django.contrib.auth.models import User

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'customer',)
    list_display_links = ('username', 'customer')
    list_per_page = 10
    search_fields = ('username', 'first_name', 'last_name')
    readonly_fields = ('username',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'present', 'id')
    list_editable = ('present',)
    ordering = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'phone', 'is_shipped', 'discount_approved', 'customer')
    list_editable = ('is_shipped',)
    search_fields = ('product',)
    list_filter = ('product',)


class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 1
    verbose_name_plural = 'Replies'
    can_delete = True
    show_change_link = True


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    inlines = (ReplyInline, )
    list_display = ('__str__', 'mail', 'text_message', 'id')

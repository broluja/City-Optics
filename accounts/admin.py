from django.contrib import admin
from .models import Customer, Coupon


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'created_on', 'discount_used', 'code')
    list_display_links = ('__str__', 'email', )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'used_on')


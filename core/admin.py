from django.contrib import admin

from core.models import File, Address, Category, Coupon, Item, Order, OrderItem, Payment, Supervisor

# Register your models here.
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(Address)
admin.site.register(Coupon)
admin.site.register(Supervisor)
admin.site.register(File)
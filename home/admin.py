from django.contrib import admin
from .models import *


# Register your models here.
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id','cat_name','cat_status', 'date']
    list_filter = ['date']
admin.site.register(Category, CategoriesAdmin)

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id','pro_name','cat_id','pro_price','pro_quantity', 'date']
    list_filter = ['date']
admin.site.register(Product, ProductsAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','transaction_id','complete', 'date']
    list_filter = ['date']
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','product','order', 'date']
    list_filter = ['date']
admin.site.register(OrderItem, OrderItemAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','name','email']
admin.site.register(Customer, CustomerAdmin)

class ShippingAdressAdmin(admin.ModelAdmin):
    list_display = ['id','customer','order','address','phone', 'date']
    list_filter = ['date']
admin.site.register(ShippingAddress, ShippingAdressAdmin)

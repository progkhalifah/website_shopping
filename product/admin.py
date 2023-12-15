from django.contrib import admin
from .models import *

# Register your models here.

# Eng_Khalifah
# I am Best Programmer
admin.site.site_title = 'I am Title of Admin'
admin.site.site_header = 'Dashboard Admin'
admin.site.index_title = 'I am Index Title'


@admin.register(Products_shop)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name_product", "image_product")
    list_filter = ("sizes",)
    search_fields = ("name_product",)


@admin.register(Color_product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ("name_product", "image_product")
    # list_filter = ("",)
    search_fields = ("name_product",)


@admin.register(Size_product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ("name_product", "image_product")
    # list_filter = ("",)
    search_fields = ("name_product",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "customer_id_order", "product_name", "status", "created_at")

# registration admin for models
# admin.site.register(Products_shop, ProductAdmin)

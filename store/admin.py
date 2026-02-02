from django.contrib import admin
from .models import Product, PurchaseRegistration


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category")
    search_fields = ("name", "category")
    list_filter = ("category",)


@admin.register(PurchaseRegistration)
class PurchaseRegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "product_name", "reference_no", "created_at")
    search_fields = ("user__username", "product_name", "reference_no")
    list_filter = ("created_at",)

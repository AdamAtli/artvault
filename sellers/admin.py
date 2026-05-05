from django.contrib import admin
from .models import Seller

@admin.register(Seller)
class SellersAdmin(admin.ModelAdmin):
    list_display = ("name", "seller_type", "street_name", "city", "postal_code")
    list_filter = ("name", "seller_type", "street_name", "city", "postal_code")
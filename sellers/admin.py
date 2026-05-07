from django.contrib import admin
from .models import Seller

@admin.register(Seller)
class SellersAdmin(admin.ModelAdmin):
    list_display = ("user", "seller_type", "street_name", "city", "postal_code")
    list_filter = ("seller_type", "city")
    search_fields = ("user__username", "city")
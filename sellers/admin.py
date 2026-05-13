from django.contrib import admin
from .models import Seller

@admin.action(description="Approve selected sellers")
def approve_sellers(modeladmin, request, queryset):
    queryset.update(is_approved=True)


@admin.action(description="Revoke seller approval")
def revoke_sellers(modeladmin, request, queryset):
    queryset.update(is_approved=False)

@admin.register(Seller)
class SellersAdmin(admin.ModelAdmin):
    list_display = ("user", "seller_type", "street_name", "city", "postal_code")
    list_filter = ("seller_type", "city")
    search_fields = ("user__username", "city")

    actions = [approve_sellers, revoke_sellers]
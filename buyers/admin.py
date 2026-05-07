from django.contrib import admin
from .models import Buyer

@admin.register(Buyer)
class SellersAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)
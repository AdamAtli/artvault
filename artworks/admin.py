from django.contrib import admin
from .models import Artwork, Image, Medium, Style

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

admin.site.register(Medium)
admin.site.register(Style)

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("title", "get_mediums", "style", "starting_bid_price", "is_sold")
    list_filter = ("style", "mediums", "edition", "is_sold")
    exclude = ("is_sold",)
    inlines = [ImageInline]

    filter_horizontal = ("mediums",)

    def get_mediums(self, obj):
        return ", ".join(
            medium.name for medium in obj.mediums.all()
        )

    get_mediums.short_description = "Mediums"
import django_filters
from django.db.models import Q
from django import forms
from .models import Artwork



SIZE_CHOICES = [
    ("small", "Small(up to 30cm)"),
    ("medium", "Medium(30-70cm)"),
    ("large", "Large (70cm+)"),
]

class ArtworkFilter(django_filters.FilterSet):
    medium = django_filters.MultipleChoiceFilter(
        choices=lambda: [(m, m) for m in Artwork.objects.values_list("medium", flat=True).distinct()],
        widget=forms.CheckboxSelectMultiple,
    )
    style = django_filters.MultipleChoiceFilter(
        choices=lambda: [(s, s) for s in Artwork.objects.values_list('style', flat=True).distinct()],
        widget=forms.CheckboxSelectMultiple,
    )
    edition = django_filters.MultipleChoiceFilter(
        choices=Artwork.EDITION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    size = django_filters.MultipleChoiceFilter(
        choices=SIZE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        method="filter_by_size",
    )

    def filter_by_size(self, queryset, name, value):
        if not value:
            return queryset

        q = Q()
        for size in value:
            if size == "small":
                q |= Q(width_cm__lte=30, height_cm__lte=30)
            elif size == "medium":
                q |= Q(width_cm__lte=70, height_cm__lte=70) & ~Q(width_cm__lte=30, height_cm__lte=30)
            elif size == "large":
                q |= Q(width_cm__gt=70) | Q(height_cm__gt=70)
        return queryset.filter(q)

    order_by = django_filters.OrderingFilter(

        choices=(
            ("title", "Title A-Z"),

            ("-title", "Title Z-A"),

            ("current_price", "Price: Low to High"),

            ("-current_price", "Price High to Low"),

            ("-listing_date", "Newest First"),

            ("listing_date", "Oldest First"),

            ("year_of_creation", "Year Created ↑"),

            ("-year_of_creation", "Year Created ↓"),
        )
    )

    class Meta:
        model = Artwork
        fields = ['medium', 'style', 'edition', 'size']

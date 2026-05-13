import django_filters
from django.db.models import Q
from django import forms
from .models import Artwork, Medium, Style



SIZE_CHOICES = [
    ("small", "Small(up to 30cm)"),
    ("medium", "Medium(30-70cm)"),
    ("large", "Large (70cm+)"),
]

PRICE_CHOICES = [
    ("under_100k", "Under $100,000"),
    ("100k_250k", "$100,000 - $250,000"),
    ("250k_500k", "$250,000 - $500,000"),
    ("over_500k", "Over $500,000"),
]

class ArtworkFilter(django_filters.FilterSet):
    mediums = django_filters.ModelMultipleChoiceFilter(
        queryset=Medium.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    style = django_filters.ModelMultipleChoiceFilter(
        queryset=Style.objects.all(),
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

    price_range = django_filters.ChoiceFilter(
        choices=PRICE_CHOICES,
        method="filter_by_price_range",
    )

    def filter_by_price_range(self, queryset, name, value):

        if value == "under_100k":
            return queryset.filter(
                current_price__lt=100000
            )

        elif value == "100k_250k":
            return queryset.filter(
                current_price__gte=100000,
                current_price__lte=250000
            )

        elif value == "250k_500k":
            return queryset.filter(
                current_price__gte=250000,
                current_price__lte=500000
            )

        elif value == "over_500k":
            return queryset.filter(
                current_price__gt=500000
            )

        return queryset

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
        fields = ['edition', 'size']

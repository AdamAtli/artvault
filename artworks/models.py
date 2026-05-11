import django_filters
from django.db.models import Q
from django import forms
from django.db import models
from sellers.models import Seller

class Artwork(models.Model):
    title = models.CharField(max_length=200)
    medium =models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    starting_bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    width_cm = models.DecimalField(max_digits=10, decimal_places=2)
    height_cm = models.DecimalField(max_digits=10, decimal_places=2)
    listing_date = models.DateField(auto_now_add=True)
    year_of_creation = models.IntegerField()

    EDITION_CHOICES = [
        ("original", "Original Edition"),
        ("open", "Open Edition"),
        ("limited", "Limited Edition"),
    ]
    edition = models.CharField(
        max_length=20,
        choices=EDITION_CHOICES,
    )

    provenance = models.TextField(blank=True)

    is_sold = models.BooleanField(default=False)

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='artworks')

    def save(self, *args, **kwargs):
        if self.medium:
            self.medium = self.medium.strip().capitalize()
        if self.style:
            self.style = self.style.strip().capitalize()
        if self.edition:
            self.edition = self.edition.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class Image(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='artworks/')

    def __str__(self):
        return self.artwork.title

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
    starting_bid_price = django_filters.RangeFilter()

    year_of_creation = django_filters.RangeFilter()

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


    class Meta:
        model = Artwork
        fields = ['medium', 'style', 'edition', 'starting_bid_price', 'year_of_creation', 'size']

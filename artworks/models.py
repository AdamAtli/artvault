from django.db import models
from django.db.models import ForeignKey, ManyToManyField

from sellers.models import Seller

class Artwork(models.Model):
    title = models.CharField(max_length=200)
    mediums = ManyToManyField("Medium", related_name='artworks', blank=True)
    style = ForeignKey("Style", on_delete=models.CASCADE, related_name='artworks')
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

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return not self.is_sold and not self.bids.filter(
            status__in=["accepted", "contingent" ,"finalized"]
        ).exists()
    @property
    def highest_bid(self):
        return self.bids.order_by("-amount").first()


class Image(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='artworks/')

    def __str__(self):
        return self.artwork.title

class Medium(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().title()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Style(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().title()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


from django.contrib.auth.models import User
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

    def __str__(self):
        return self.title



class Images(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='artworks/')

    def __str__(self):
        return self.artwork.title
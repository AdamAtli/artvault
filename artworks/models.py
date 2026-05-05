from django.db import models

class Artwork(models.Model):
    title = models.CharField(max_length=200)

    medium =models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    starting_bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    listing_date = models.DateField(auto_now_add=True)
    width_cm = models.DecimalField(max_digits=10, decimal_places=2)
    height_cm = models.DecimalField(max_digits=10, decimal_places=2)
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
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title


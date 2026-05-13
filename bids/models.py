from django.db import models
from django.core.exceptions import ValidationError
from artworks.models import Artwork
from buyers.models import Buyer
from django.utils import timezone


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name="bids")
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="bids")
    timestamp = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("contingent", "Contingent"),
        ("finalized", "Finalized"),
        ("expired", "Expired"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    expiration_date = models.DateField(null=True, blank=True)

    def clean(self):
        if self.amount < self.artwork.starting_bid_price:
            raise ValidationError(
                f"Bid must be at least the starting bid price of ${self.artwork.starting_bid_price}"
            )

    @property
    def is_expired(self):
        return (
            self.status == "pending"
            and self.expiration_date
            and self.expiration_date <= timezone.localdate()
        )

    @property
    def is_active(self):
        return self.status in ["pending", "accepted", "rejected"]



    class Meta:
        ordering = ['-timestamp']
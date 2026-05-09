from django.db import models
from django.core.exceptions import ValidationError
from artworks.models import Artwork
from buyers.models import Buyer


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name="bids")
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="bids")
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        highest_bid = self.artwork.bids.order_by("-amount").first()
        if highest_bid and self.amount <= highest_bid.amount:
            raise ValidationError(f"Bid must be higher than the current highest bid of ${highest_bid.amount}")

    class Meta:
        ordering = ['-timestamp']
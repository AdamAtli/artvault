from django.db import models
from artworks.models import Artwork
from buyers.models import Buyer


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name="bids")
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="bids")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        constraints = [
            models.UniqueConstraint(fields=['amount', 'artwork'], name='unique-amount-per-artwork'),
            
        ]
from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    Artist = 'artist'
    Gallery = 'gallery'

    Seller_Type_choices = [
        (Artist, 'Artist'),
        (Gallery, 'Gallery'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    seller_type = models.CharField(max_length=10, choices=Seller_Type_choices, blank=True)

    logo = models.ImageField(upload_to='seller_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='seller_cover/', blank=True, null=True)
    bio = models.TextField(blank=True)

    street_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def clean(self):
        if self.seller_type == self.Gallery:
            if not self.street_name or not self.city or not self.postal_code:
                raise ValueError("Gallery must have a full address")


    def __str__(self):
        return self.user.username



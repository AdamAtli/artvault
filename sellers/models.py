from django.db import models

class Sellers(models.Model):
    Artist = 'artist'
    Gallery = 'gallery'

    Seller_Type_choices = [
        (Artist, 'Artist'),
        (Gallery, 'Gallery'),
    ]

    name = models.CharField(max_length=100)
    seller_type = models.CharField(max_length=10, choices=Seller_Type_choices)

    logo = models.ImageField(upload_to='seller_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='seller_cover/', blank=True, null=True)
    bio = models.TextField(blank=True)

    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()

    def clean(self):
        if self.seller_type == self.Gallery:
            if not self.street_name or not self.city or not self.postal_code:
                raise ValueError("Gallery must have a full address")


    def __str__(self):
        return self.name



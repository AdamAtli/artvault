from django.db import models
from django.contrib.auth.models import User

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics", default="profile_pics/default.png", blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
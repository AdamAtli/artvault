from django import forms

from .models import Buyer

class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ["profile_pic", "bio", "full_name"]

        widgets = {
            "profile_pic": forms.FileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows":4}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
        }
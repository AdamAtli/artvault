from django import forms

from .models import Seller

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = [
            "logo",
            "cover_image",
            "bio",
            "street_name",
            "city",
            "postal_code",
            "full_name",
        ]
        widgets = {
            "logo": forms.FileInput(attrs={"class": "form-control"}),
            "cover_image": forms.FileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
            "street_name": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.NumberInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
        }
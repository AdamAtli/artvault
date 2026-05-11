from django import forms

from .models import Seller
#TODO only display address of galleries
class SellerProfileForm(forms.ModelForm):
    username = forms.CharField(max_length = 150)

    class Meta:
        model = Seller
        fields = [
            "logo",
            "cover_image",
            "bio",
            "street_name",
            "city",
            "postal_code",
        ]
        widgets = {
            "logo": forms.FileInput(attrs={"class": "form-control"}),
            "cover_image": forms.FileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
            "street_name": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].initial = self.instance.user.username
        self.fields['username'].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        seller = super().save(commit=False)
        seller.user.username = self.cleaned_data["username"]

        if commit:
            seller.user.save()
            seller.save()

        return seller
from django import forms
from django.contrib.auth.models import User

from .models import Buyer

class BuyerProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)

    class Meta:
        model = Buyer
        fields = ["profile_pic", "bio"]
        widgets = {
            "profile_pic": forms.FileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows":4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].initial = self.instance.user.username
        self.fields["username"].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        buyer = super().save(commit=False)
        buyer.user.username = self.cleaned_data["username"]

        if commit:
            buyer.user.save()
            buyer.save()

        return buyer 

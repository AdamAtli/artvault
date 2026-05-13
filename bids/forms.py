from django import forms

from .models import BidContingency

class SellerContingencyForm(forms.ModelForm):
    class Meta:
        model = BidContingency
        fields = ["seller_message"]
        widgets = {
            "seller_message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder" : "Write the conditions the buyer must agree to..."
            })
        }

class BuyerContingencyResponseForm(forms.ModelForm):
    buyer_response = forms.ChoiceField(
        choices=BidContingency.RESPONSE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = BidContingency
        fields = ["buyer_response", "buyer_message"]
        widgets = {
            "buyer_response": forms.RadioSelect,
            "buyer_message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder" : "Write response to the seller..."
            })
        }

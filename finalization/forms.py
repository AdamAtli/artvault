from django import forms

class ContactInformationForm(forms.Form):
    street_name = forms.CharField(max_length=200)
    city = forms.CharField(max_length=200)
    postal_code = forms.CharField(max_length=50)

    COUNTRY_CHOICES = [
        ('IS', 'Iceland'),
        ('US', 'United States'),
        ('CA', 'Canada'),
        ("DK", "Denmark"),
        ("NO", "Norway"),
        ("SW", "Sweden"),
        ("FI", "Finland"),
    ]

    country = forms.ChoiceField(choices=COUNTRY_CHOICES)

    national_id = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
            })

        self.fields["country"].widget.attrs.update({
            "class": "form-select"
        })

class PaymentForm(forms.Form):

    PAYMENT_CHOICES = [
        ("credit_card", "Credit Card"),
        ("bank_transfer", "Bank Transfer"),
        ("wire_transfer", "Wire Transfer"),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
    )

    cardholder_name = forms.CharField(required=False)
    credit_card_number = forms.CharField(required=False)
    expiry_date = forms.CharField(required=False)
    cvc = forms.CharField(required=False)

    bank_account = forms.CharField(required=False)

    sending_bank = forms.CharField(required=False)
    routing_number = forms.CharField(required=False)
    account_number = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != "payment_method":
                field.widget.attrs.update({
                    "class": "form-control"
                })

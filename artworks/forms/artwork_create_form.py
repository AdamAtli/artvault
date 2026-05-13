from django.forms import ModelForm
from django import forms

from artworks.models import Artwork, Image


class ArtworkCreateForm(ModelForm):

    new_medium = forms.CharField(
        required=False,
    )
    new_style = forms.CharField(
        required=False,
    )

    class Meta:
        model = Artwork
        fields = [
            'title',
            'mediums',
            'style',
            'starting_bid_price',
            'width_cm',
            'height_cm',
            'year_of_creation',
            'edition',
            'provenance',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artwork Title'}),
            'mediums': forms.CheckboxSelectMultiple(),
            'style': forms.Select(attrs={'class': 'form-select'}),
            'starting_bid_price':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Artwork Starting Bid Price'}),
            'width_cm': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Width in cm'}),
            'height_cm': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height in cm'}),
            'year_of_creation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year of Creation'}),
            'edition': forms.Select(attrs={'class':'form-select', 'placeholder': 'Edition'}),
            'provenance': forms.Textarea(attrs={'class':'form-control', 'rows':4, 'placeholder': 'Provenance'}),
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]

        return single_file_clean(data, initial)

class ImageCreateForm(forms.Form):
    image = MultipleFileField(
        widget=MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}),
    )
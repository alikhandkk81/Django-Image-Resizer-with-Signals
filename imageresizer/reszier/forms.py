# forms.py
from django import forms
from .models import ImageModel

class ResizeForm(forms.Form):
    image = forms.ImageField()
    width = forms.IntegerField(min_value=1, label="Width")
    height = forms.IntegerField(min_value=1, label="Height")

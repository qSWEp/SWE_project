# store/forms.py
from django import forms
from .models import DeliveryInfo

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        fields = ['address', 'city', 'postal_code', 'phone']








class DeliveryForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        fields = ['address', 'city', 'postal_code', 'phone']

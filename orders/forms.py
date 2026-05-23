from django import forms
from .models import Order, ShipmentTracking


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model  = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class ShipmentTrackingForm(forms.ModelForm):
    class Meta:
        model  = ShipmentTracking
        fields = ['carrier', 'tracking_number', 'tracking_url', 'shipped_at']
        widgets = {
            'carrier'         : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Royal Mail'}),
            'tracking_number' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tracking number'}),
            'tracking_url'    : forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'shipped_at'      : forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
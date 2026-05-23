from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    class Meta:
        model  = Store
        fields = [
            'name', 'channel', 'status', 'description',
            'api_key', 'api_secret', 'access_token',
            'refresh_token', 'store_id',
            'auto_sync', 'sync_inventory',
            'sync_prices', 'markup_percent',
        ]
        widgets = {
            'name'          : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Rolzay Amazon UK'}),
            'channel'       : forms.Select(attrs={'class': 'form-select'}),
            'status'        : forms.Select(attrs={'class': 'form-select'}),
            'description'   : forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'api_key'       : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'API Key'}),
            'api_secret'    : forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'API Secret'}, render_value=True),
            'access_token'  : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Access Token'}),
            'refresh_token' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Refresh Token'}),
            'store_id'      : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seller / Store ID'}),
            'markup_percent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }
from django import forms
from .models import Product, ProductImage, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = [
            'name', 'category', 'description', 'price',
            'stock', 'sku', 'status', 'image',
            'sync_amazon', 'sync_ebay', 'sync_etsy',
        ]
        widgets = {
            'name'        : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'category'    : forms.Select(attrs={'class': 'form-select'}),
            'description' : forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Product description'}),
            'price'       : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'stock'       : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'sku'         : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. RLZ-001'}),
            'status'      : forms.Select(attrs={'class': 'form-select'}),
            'image'       : forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model  = ProductImage
        fields = ['image', 'alt']
        widgets = {
            'image' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'alt'   : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image description'}),
        }


# Allows multiple gallery images at once
ProductImageFormSet = forms.inlineformset_factory(
    Product,
    ProductImage,
    form    = ProductImageForm,
    extra   = 3,
    max_num = 10,
    can_delete = True,
)
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'present', 'image']
        labels = {
            'name': '',
            'description': '',
            'price': 'Price ($)',
            'image': 'Attach an image on your product',
            'present': 'Presence on Stock'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg mt-3 mb-3', 'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control mt-3 mb-3', 'placeholder': 'Description'}),
            'present': forms.NullBooleanSelect(attrs={'class': 'form-control mt-2 mb-3'}),
            'image': forms.FileInput(attrs={'class': ' mt-2 mb-3'}),
        }
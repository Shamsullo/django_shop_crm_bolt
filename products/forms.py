from django import forms
from .models import Product, Service, Pattern

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'unit_price', 'stock', 'min_stock', 
                 'is_active', 'is_glass_type', 'thickness', 'max_width', 'max_height']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'base_price', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PatternForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = ['name', 'description', 'image', 'price', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
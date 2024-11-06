from django import forms
from django.core.exceptions import ValidationError
from .models import Order, OrderItem, OrderService
from accounts.models import Customer
from products.models import Product, Service, Pattern

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'width', 'height']

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')

        if product and product.is_glass_type:
            if not width or not height:
                raise ValidationError("Width and height are required for glass/mirror products")
            if product.max_width and width > product.max_width:
                raise ValidationError(f"Width cannot exceed {product.max_width}")
            if product.max_height and height > product.max_height:
                raise ValidationError(f"Height cannot exceed {product.max_height}")

        return cleaned_data

class OrderServiceForm(forms.ModelForm):
    class Meta:
        model = OrderService
        fields = ['service', 'pattern']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pattern'].required = False
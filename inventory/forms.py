from django import forms
from .models import InventoryTransaction, Supplier

class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        fields = ['product', 'transaction_type', 'quantity', 'unit_price', 'reference', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
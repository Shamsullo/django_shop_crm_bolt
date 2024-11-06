from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Customer

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role', 'phone')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'email', 'role', 'phone')

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
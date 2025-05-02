from django import forms
from .models import Subscription
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'category', 'price', 'billing_period', 'next_payment_date', 'is_active']
        widgets = {
            'next_payment_date': forms.DateInput(attrs={'type': 'date'})
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']
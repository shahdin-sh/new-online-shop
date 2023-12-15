from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'company', 'country', 'address', 'town', 'area', 'zip_code', 'phone_number', 'email', 'note']




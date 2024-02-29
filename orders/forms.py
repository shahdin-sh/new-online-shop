from django import forms
from orders.models import CustomerWithAddress


class CustomerWithAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerWithAddress
        fields = ['company', 'country', 'address', 'town', 'zip_code', 'phone_number', 'note']




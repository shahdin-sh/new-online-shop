from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'company', 'country', 'address', 'town', 'area', 'zip_code', 'phone_number', 'email', 'note']
        # we use html input for implementing our forms
        # widgets = {
        #         'country': forms.Select(choices=[
        #             ('iran', 'ایران'),
        #             ('iraq', 'عراق'),
        #             ('bahrain', 'بحرین'),
        #             ('uae', 'امارات'),
        #             ('turkey', 'ترکیه'),
        #         ]),
        #         'area': forms.Select(choices=[
        #             ('area 1', 'منطقه 1'),
        #             ('area 2', 'منطقه 2'),
        #             ('area 3', 'منطقه 3'),
        #             ('area 4', 'منطقه 4'),
        #             ('area 5', 'منطقه 5'),
        #         ]),
        #         # 'email': forms.EmailInput(attrs={'placeholder': 'Please enter your email address'}),
        #         # 'note': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        # }





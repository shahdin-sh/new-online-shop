from django import forms

class AddToCartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        product_stock = kwargs.pop('product_stock')
        super(AddToCartForm, self).__init__(*args, **kwargs)
        QUANTITY_CHOICES = [(i, str(i)) for i in range(1, int(product_stock) + 1)]
        COLOR_CHOICES =  (('BLACK', 'black'),('WHITE', 'white'),('PINK', 'pink'))
        SIZE_CHOICES = (('LARGE', 'large'),('MEDIUM', 'medium'),('SMALL', 'small'))
        self.fields['quantity'] = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int, required=True)
        self.fields['inplace'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
        self.fields['color'] = forms.ChoiceField(choices=COLOR_CHOICES, required=True, widget=forms.HiddenInput())
        self.fields['size'] =  forms.ChoiceField(choices=SIZE_CHOICES, required=True, widget=forms.HiddenInput())
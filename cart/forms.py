from django.forms import forms

class AddToCartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AddToCartForm, self).__init__( *args, **kwargs)
        product_stock = int(kwargs.pop('product_stock'))
        QUANTITY_CHOICES = [(i, str(i)) for i in range(1, product_stock)] 
        self.fields['quantity'] = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int, required=True)




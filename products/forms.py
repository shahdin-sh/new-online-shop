from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from django.contrib.auth import get_user_model

from products.models import Comment, Discount
from products.models import Discount

User = get_user_model()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # we fill author and product manually in the product_detail_views
        fields = ['content', 'name', 'email', 'rating']

    def __init__(self, request, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        # honeypot field
        self.fields['website'] = forms.CharField(required=False)
    
    
class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['promo_code']

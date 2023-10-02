from django import forms
from .models import Comment
from accounts.models import CustomUserModel
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # we fill author and post manually in the product_detail_views
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['website'] = forms.CharField(
        required=False,
        help_text="Please leave this field blank",
    ) 
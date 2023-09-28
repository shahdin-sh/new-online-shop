from django import forms
from .models import Comment
from accounts.models import CustomUserModel
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # we fill author and post manually in the product_detail_views
        fields = ['content']
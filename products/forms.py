from django import forms
from .models import Comment, Product
from accounts.models import CustomUserModel
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # we fill author and product manually in the product_detail_views
        fields = ['content', 'name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add custom validation logic for the email field
        if email:
            # Your custom validation conditions go here
            # For example, check if the email is already in use in the database
            if CustomUserModel.objects.filter(email__iexact=email).exists() or Comment.objects.filter(email=email).exists():
                raise ValidationError("This email is already in use.")
        return email
       

       
class SizeAndColorForm(forms.ModelForm):
    COLOR_CHOICES = (
        ('BLACK', 'black'),
        ('WHITE', 'white'),
        ('PINK', 'pink'),
    )

    SIZE_CHOICES = (
        ('LARGE', 'large'),
        ('MEDIUM', 'medium'),
        ('SMALL', 'small'),

    )
    color = forms.MultipleChoiceField(choices=COLOR_CHOICES, required=False)
    size = forms.MultipleChoiceField(choices=SIZE_CHOICES, required=False)
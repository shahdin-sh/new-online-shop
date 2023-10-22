from django import forms
from .models import Comment, Product
from accounts.models import CustomUserModel
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # we fill author and product manually in the product_detail_views
        fields = ['content', 'name', 'email', 'rating']

    def __init__(self, request, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        # honeypot field
        self.fields['website'] = forms.CharField(required=False, help_text="Please leave this field blank",)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add custom validation logic for the email field
        if email:
            # Your custom validation conditions go here
            # For example, check if the email is already in use in the database excepts for users who are not login and their emails are in the DB.
            if CustomUserModel.objects.filter(email__iexact=email).exists() or Comment.objects.filter(email=email, session_token=None).exists():
                raise ValidationError("This email is already in use.")
        return email
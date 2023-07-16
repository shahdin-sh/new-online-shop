from django import forms
from .models import Comment, Product
from accounts.models import CustomUserModel


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # we fill author and product manually in the product_detail_views
        fields = ['content']

        # widgets = {
        #     'rating' : forms.HiddenInput(),
        # }


class GuestCommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Address already exists.")
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Override the required error message for each field
        self.fields['content'].error_messages['required'] = ('Please enter your comment.')
        self.fields['name'].error_messages['required'] = ('Please enter your name.')
        self.fields['email'].error_messages['required'] = ('Please enter your email address.')


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
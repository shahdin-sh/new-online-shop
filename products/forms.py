from django import forms
from .models import Comment, Product


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # we fill author and product manually in the product_detail_views
        fields = ['content']

        # widgets = {
        #     'rating' : forms.HiddenInput(),
        # }


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
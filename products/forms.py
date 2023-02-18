from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # we fill author and product manually in the product_detail_views
        fields = ['content']

        # widgets = {
        #     'rating' : forms.HiddenInput(),
        # }

    
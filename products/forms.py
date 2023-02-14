from django import forms
from .models import Comments


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        # we fill author and product manually in the product_detail_views
        fields = ['content', ]

        # widgets = {
        #     'content' : forms.TextInput(),
        # }
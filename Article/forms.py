from . import models
from django import forms

class article_post_form(forms.ModelForm):
    class Meta:
        model = models.ArticlePost
        fields = ('title','body')
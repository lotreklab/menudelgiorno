from django import forms

from web.models import Review


class ReviewForm(forms.ModelForm):

    text = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Review
        fields = ('score', 'text')

from django import forms

from posts.models import BookReview

class BookReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = BookReview
        fields = ('stars_given', 'comment')

class NewsCreateForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'description', 'cover_picture')
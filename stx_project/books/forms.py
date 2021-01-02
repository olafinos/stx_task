from django import forms
from .models import Book


class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=150, required=False)
    author = forms.CharField(max_length=150, required=False)
    publication_date_start = forms.DateField(required=False)
    publication_date_end = forms.DateField(required=False)
    publication_language = forms.CharField(max_length=150, required=False)

class BookAddForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = "__all__"
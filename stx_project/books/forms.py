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

class GoogleBooksAPIForm(forms.Form):
    q = forms.CharField(max_length=150,required=False)
    intitle = forms.CharField(max_length=150, required=False)
    inauthor = forms.CharField(max_length=150, required=False)
    inpublisher = forms.CharField(max_length=150, required=False)
    subject = forms.CharField(max_length=150, required=False)
    isbn = forms.IntegerField(required=False)
    lccn = forms.IntegerField(required=False)
    oclc = forms.IntegerField(required=False)
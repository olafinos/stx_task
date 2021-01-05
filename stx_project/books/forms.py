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
        fields = [
            "isbn_number",
            "title",
            "author",
            "publication_date",
            "number_of_pages",
            "cover_link",
            "publication_language",
        ]


class GoogleBooksAPIForm(forms.Form):
    q = forms.CharField(max_length=150, required=False)
    intitle = forms.CharField(max_length=150, required=False)
    inauthor = forms.CharField(max_length=150, required=False)
    inpublisher = forms.CharField(max_length=150, required=False)
    subject = forms.CharField(max_length=150, required=False)
    isbn = forms.CharField(max_length=13, required=False)
    lccn = forms.CharField(max_length=13, required=False)
    oclc = forms.CharField(required=False)

from .models import Book
from .forms import BookSearchForm
import datetime
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.db.models import Q


class BooksList(ListView):
    model = Book
    template_name = "books_list.html"
    form_class = BookSearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            object_list = Book.objects.filter(
              self._create_filter_object(form.cleaned_data)
            )
            return object_list
        return Book.objects.all()

    def _create_filter_object(self, form_data):
        filter_object = Q(title__icontains=form_data["title"])
        filter_object &= Q(author__icontains=form_data["author"])
        filter_object &= Q(
                    publication_language__icontains=form_data[
                        "publication_language"
                    ]
                )
        if form_data['publication_date_start']:
            filter_object &= Q(publication_date__gte=form_data['publication_date_start'])
        if form_data['publication_date_end']:
            filter_object &= Q(publication_date__lte=form_data['publication_date_end'])
        return filter_object

class BookDetail(DetailView):
    model = Book
    template_name = "books_detail.html"

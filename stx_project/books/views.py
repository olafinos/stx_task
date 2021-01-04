from .google_books import add_books_using_api
from .models import Book
from .forms import BookSearchForm, BookAddForm, GoogleBooksAPIForm
from typing import Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView
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

    def _create_filter_object(self, form_data: Dict) -> Q:
        filter_object = Q(title__icontains=form_data["title"])
        filter_object &= Q(author__icontains=form_data["author"])
        filter_object &= Q(
            publication_language__icontains=form_data["publication_language"]
        )
        if form_data["publication_date_start"]:
            filter_object &= Q(
                publication_date__gte=form_data["publication_date_start"]
            )
        if form_data["publication_date_end"]:
            filter_object &= Q(publication_date__lte=form_data["publication_date_end"])
        return filter_object


class BookDetail(DetailView):
    model = Book
    template_name = "books_detail.html"


class EditBook(UpdateView):
    model = Book
    template_name = "add_book.html"
    fields = [
        "isbn_number",
        "title",
        "author",
        "publication_date",
        "number_of_pages",
        "cover_link",
        "publication_language",
    ]


class AddBook(CreateView):
    model = Book
    template_name = "add_book.html"
    form_class = BookAddForm


class AddBookGoogleAPI(View):
    def get(self, request: HttpRequest, format=None) -> HttpResponse:
        form = GoogleBooksAPIForm()
        return render(request, "add_books_using_api.html", {"form": form})

    def post(self, request: HttpRequest, format=None) -> HttpResponse:
        form = GoogleBooksAPIForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data
            added_books = add_books_using_api(keywords)
            messages.add_message(
                request, messages.SUCCESS, f"Number of books added: {added_books}"
            )
        return render(request, "add_books_using_api.html", {"form": form})

from .google_books import GoogleBooksDownloader, GoogleBooksParser
from .models import Book
from .forms import BookSearchForm, BookAddForm, GoogleBooksAPIForm
from .serializers import BookSerializer
from typing import Dict, List
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView
from django.db.models import Q
from django.db import IntegrityError
from rest_framework import viewsets


class BooksList(ListView):
    """
    View responsible for listing all books. It also allows to use search filters.
    """

    model = Book
    template_name = "books_list.html"
    paginate_by = 25
    form_class = BookSearchForm

    def get_queryset(self):
        """
        Method which filters returned results.
        :return: Returns Book objects and filters them if needed.
        """
        form = self.form_class(self.request.GET)
        if form.is_valid():
            object_list = Book.objects.filter(
                self._create_filter_object(form.cleaned_data)
            )
            return object_list
        return Book.objects.all()

    @staticmethod
    def _create_filter_object(form_data: Dict) -> Q:
        """
        Creates search query based on query parameters.
        :param form_data: Form data
        :return: Query object based on given parameters
        """
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


class BookListREST(viewsets.generics.ListAPIView):
    """
    View responsible for listing all books in REST format. It also allows to use search filters.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Method which filters returned results.
        :return: Returns Book objects and filters them if needed.
        """
        queryset = Book.objects.all()
        title = self.request.query_params.get("title", None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        author = self.request.query_params.get("author", None)
        if author:
            queryset = queryset.filter(author__icontains=author)
        publication_language = self.request.query_params.get(
            "publication_language", None
        )
        if publication_language:
            queryset = queryset.filter(
                publication_language__icontains=publication_language
            )
        publication_date_start = self.request.query_params.get(
            "publication_date_start", None
        )
        if publication_date_start:
            queryset = queryset.filter(publication_date__gte=publication_date_start)
        publication_date_end = self.request.query_params.get(
            "publication_date_end", None
        )
        if publication_date_end:
            queryset = queryset.filter(publication_date__lte=publication_date_end)
        return queryset


class BookDetail(DetailView):
    """
    View responsible for displaying Book detail.
    """

    model = Book
    template_name = "books_detail.html"


class EditBook(UpdateView):
    """
    View responsible for editing Book objects.
    """

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
    """
    View responsible for adding Book objects.
    """

    model = Book
    template_name = "add_book.html"
    form_class = BookAddForm


class AddBooksGoogleAPI(View):
    """
    View responsible for adding books using GoogleBooksAPI
    """

    def get(self, request: HttpRequest, format=None) -> HttpResponse:
        form = GoogleBooksAPIForm()
        return render(request, "add_books_using_api.html", {"form": form})

    def post(self, request: HttpRequest, format=None) -> HttpResponse:
        form = GoogleBooksAPIForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data
            books = self._get_books_from_api(keywords)
            added_books = self.add_books(books)
            messages.add_message(
                request, messages.SUCCESS, f"Number of books added: {added_books}"
            )
        return render(request, "add_books_using_api.html", {"form": form})

    def _get_books_from_api(self, keywords: Dict) -> List[Dict]:
        """
        Downloads and parses books which was found for given keywords.
        :param keywords: Dictionary with keywords for search query
        :return: List with books compatible with Book model.
        """
        downloader = GoogleBooksDownloader()
        parser = GoogleBooksParser()
        downloaded_books = downloader.get_books_using_api(keywords=keywords)
        parsed_books = parser.parse(downloaded_books)
        return parsed_books

    @staticmethod
    def add_books(books: List[Dict]) -> int:
        """
        Adds Book objects to database.
        :param books: List with books compatible with Book model.
        :return: Number of books successfully added.
        """
        added_books = 0
        for book in books:
            try:
                book_object = Book(**book)
                book_object.save()
                added_books += 1
            except IntegrityError:
                continue
        return added_books

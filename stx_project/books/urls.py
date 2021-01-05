from .views import (
    BooksList,
    BookDetail,
    EditBook,
    AddBook,
    AddBookGoogleAPI,
    BookListREST,
)
from django.urls import path, re_path

urlpatterns = [
    path("books/", BooksList.as_view(), name="books_list"),
    path("books/<uuid:pk>", BookDetail.as_view(), name="books_detail"),
    path("books/<uuid:pk>/edit", EditBook.as_view(), name="edit_book"),
    path("books/add_book", AddBook.as_view(), name="add_book"),
    path(
        "books/add_book_using_api",
        AddBookGoogleAPI.as_view(),
        name="add_books_using_api",
    ),
    re_path("v1/books/?$", BookListREST.as_view(), name="books_list_REST"),
]

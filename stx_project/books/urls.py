from .views import BooksList, BookDetail, AddBook
from django.urls import path

urlpatterns = [
    path("books/", BooksList.as_view(), name="books_list"),
    path("books/<int:pk>", BookDetail.as_view(), name="books_detail"),
    path("books/add_book", AddBook.as_view(), name="add_book")
]

from .views import BooksList, BookDetail
from django.urls import path

urlpatterns = [
    path("books/", BooksList.as_view(), name="books_list"),
    path("books/<int:pk>", BookDetail.as_view(), name="books_detail"),
]

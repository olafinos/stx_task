from django.db import models
from django.urls import reverse
from uuid import uuid4


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    isbn_number = models.IntegerField(unique=True)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    publication_date = models.DateField()
    number_of_pages = models.IntegerField()
    cover_link = models.CharField(max_length=200)
    publication_language = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse("books_detail", kwargs={"pk": self.pk})

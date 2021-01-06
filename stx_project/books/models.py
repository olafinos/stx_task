from django.db import models
from django.urls import reverse
from uuid import uuid4


class Book(models.Model):
    """
    Class for Book model.
    """

    id = models.UUIDField(primary_key=True, default=uuid4)
    isbn_number = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150, null=True, default=None, blank=True)
    publication_date = models.DateField(null=True, default=None, blank=True)
    number_of_pages = models.IntegerField(null=True, default=None, blank=True)
    cover_link = models.CharField(max_length=200, null=True, default=None, blank=True)
    publication_language = models.CharField(max_length=150)

    def get_absolute_url(self) -> str:
        """
        Retrieves url to self
        :return: Url to self resource.
        """
        return reverse("books_detail", kwargs={"pk": self.pk})

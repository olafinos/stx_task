from django.db import models


class Book(models.Model):
    isbn_number = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    publication_date = models.DateField()
    number_of_pages = models.IntegerField()
    cover_link = models.CharField(max_length=200)
    publication_language = models.CharField(max_length=150)

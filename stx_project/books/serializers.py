from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.HyperlinkedModelSerializer):
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

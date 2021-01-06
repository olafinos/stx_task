from django.test import TestCase
from ..models import Book


class TestBook(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.book = Book.objects.create(
            isbn_number="123456789",
            title="test",
            author="author",
            publication_date="2021-01-06",
            number_of_pages=220,
            cover_link="link",
            publication_language="test",
        )

    def test_object_added(self):
        book = Book.objects.get(title="test")
        self.assertEqual(book.title, "test")

    def test_get_absolute_url(self):
        url = self.book.get_absolute_url()
        self.assertEqual(url, f"/books/{self.book.pk}")

    def test_isbn_number_max_length(self):
        max_length = self.book._meta.get_field("isbn_number").max_length
        self.assertEqual(max_length, 13)

    def test_title_max_length(self):
        max_length = self.book._meta.get_field("title").max_length
        self.assertEqual(max_length, 150)

    def test_author_max_length(self):
        max_length = self.book._meta.get_field("author").max_length
        self.assertEqual(max_length, 150)

    def test_cover_link_max_length(self):
        max_length = self.book._meta.get_field("cover_link").max_length
        self.assertEqual(max_length, 200)

    def test_publication_language_max_length(self):
        max_length = self.book._meta.get_field("publication_language").max_length
        self.assertEqual(max_length, 150)

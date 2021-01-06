from django.test import TestCase
from unittest.mock import patch
from ..google_books import GoogleBooksParser, GoogleBooksDownloader
from django.urls import reverse


class TestGoogleBooksDownloader(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.downloader = GoogleBooksDownloader()

    def test_create_link(self):
        keywords = {"q": "test_q", "subject": "test_subject", "isbn": "1234"}
        link = self.downloader._create_link(keywords)
        self.assertEqual(
            link,
            "https://www.googleapis.com/books/v1/volumes?q=test_q+subject=test_subject+isbn=1234+",
        )

    def test_get_resource(self):
        resource = self.downloader._get_resource(
            "https://www.googleapis.com/books/v1/volumes?q=+isbn=0007488319"
        )
        self.assertTrue(isinstance(resource, dict))

    @patch("books.google_books.GoogleBooksDownloader._get_resource")
    def test_get_all_books(self, mocked_get_resource):
        link = "https://www.googleapis.com/books/v1/volumes?isbn=0007488319"
        resource = {
            "volumeInfo": {
                "title": "The Fellowship of the Ring",
                "publishedDate": "2012-03-01",
                "authors": ["J. R. R. Tolkien"],
                "industryIdentifiers": [
                    {"type": "ISBN_10", "identifier": "0007488319"},
                    {"type": "ISBN_13", "identifier": "9780007488315"},
                ],
                "pageCount": 448,
                "imageLinks": {
                    "smallThumbnail": "http://books.google.com/books/content?id=lqHNugAACAAJ&printsec=frontcover&img"
                    "=1&zoom=5&source=gbs_api",
                    "thumbnail": "http://books.google.com/books/content?id=lqHNugAACAAJ&printsec=frontcover&img=1"
                    "&zoom=1&source=gbs_api",
                },
                "language": "en",
            }
        }
        mocked_get_resource.side_effect = [{"items": [resource]}, {}]
        books = self.downloader._get_all_books(link)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0], resource["volumeInfo"])

    class TestGoogleBooksParser(TestCase):
        @classmethod
        def setUpTestData(cls):
            cls.parser = GoogleBooksParser()

        def test_parse(self):
            resource = [
                {
                    "title": "The Fellowship of the Ring",
                    "publishedDate": "2012-03-01",
                    "authors": ["J. R. R. Tolkien"],
                    "industryIdentifiers": [
                        {"type": "ISBN_10", "identifier": "0007488319"},
                        {"type": "ISBN_13", "identifier": "9780007488315"},
                    ],
                    "pageCount": 448,
                    "imageLinks": {
                        "smallThumbnail": "http://books.google.com/books/content?id=lqHNugAACAAJ&printsec=frontcover"
                        "&img=1&zoom=5&source=gbs_api",
                        "thumbnail": "http://books.google.com/books/content?id=lqHNugAACAAJ&printsec=frontcover&img=1"
                        "&zoom=1&source=gbs_api",
                    },
                    "language": "en",
                }
            ]
            result = [
                {
                    "title": "The Fellowship of the Ring",
                    "isbn_number": "0007488319",
                    "author": "J. R. R. Tolkien",
                    "publication_date": "2012-03-01",
                    "number_of_pages": 448,
                    "cover_link": "http://books.google.com/books/content?id=lqHNugAACAAJ&printsec=frontcover&img=1"
                    "&zoom=1&source=gbs_api",
                    "publication_language": "en",
                }
            ]
            self.assertEqual(self.parser(resource), result)

        def test_get_isbn(self):
            isbn_resource = {
                "industryIdentifiers": [
                    {"type": "ISBN_10", "identifier": "0007488319"},
                    {"type": "ISBN_13", "identifier": "9780007488315"},
                ]
            }
            self.assertEqual(self.parser._get_isbn(isbn_resource), "0007488319")

        def test_get_isbn_bad_type(self):
            isbn_resource = {
                "industryIdentifiers": [
                    {"type": "OTHER", "identifier": "XYZ"},
                ]
            }
            self.assertEqual(self.parser._get_isbn(isbn_resource), None)

        def test_get_author(self):
            author_resource = {"authors": ["J. R. R. Tolkien"]}
            self.assertEqual(
                self.parser._get_author(author_resource), "J. R. R. Tolkien"
            )

        def test_get_author_multiple(self):
            author_resource = {"authors": ["J. R. R. Tolkien", "Test author"]}
            self.assertEqual(
                self.parser._get_author(author_resource),
                "J. R. R. Tolkien, Test author",
            )

        def test_get_publication_date(self):
            date_resource = {"publishedDate": "2012-03-01"}
            self.assertEqual(
                self.parser._get_publication_date(date_resource), "2012-03-01"
            )

        def test_get_publication_date_only_year(self):
            date_resource = {"publishedDate": "2012"}
            self.assertEqual(
                self.parser._get_publication_date(date_resource), "2012-05-01"
            )

        def test_get_publication_date_wrong_format(self):
            date_resource = {"publishedDate": "2012*"}
            self.assertEqual(self.parser._get_publication_date(date_resource), None)

from django.test import TestCase
from django.urls import reverse
from ..models import Book
import json


class TestBooksList(TestCase):
    @classmethod
    def setUpTestData(cls):
        books_number = 28
        for book_id in range(books_number):
            Book.objects.create(
                isbn_number=book_id,
                title=f"test_{book_id}",
                author="author",
                publication_date="2021-01-06",
                number_of_pages=220,
                cover_link="link",
                publication_language="test",
            )

    def test_books_view_url(self):
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 200)

    def test_books_view_uses_correct_template(self):
        response = self.client.get(reverse("books_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books_list.html")

    def test_pagination(self):
        response = self.client.get(reverse("books_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(len(response.context["object_list"]) == 25)

    def test_lists_all_books(self):
        response = self.client.get(reverse("books_list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(len(response.context["object_list"]) == 3)

    def test_filter_text(self):
        response = self.client.get(reverse("books_list") + "?title=test_21")
        self.assertEqual(response.status_code, 200)
        book = response.context["object_list"][0]
        self.assertEqual(book.title, "test_21")

    def test_filter_date_for_all_results(self):
        response = self.client.get(
            reverse("books_list") + "?publication_date_start=2021-01-05"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(len(response.context["object_list"]) == 25)

    def test_filter_date_for_no_results(self):
        response = self.client.get(
            reverse("books_list") + "?publication_date_end=2021-01-05"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["object_list"]), 0)


class TestBooksListREST(TestCase):
    @classmethod
    def setUpTestData(cls):
        books_number = 10
        for book_id in range(books_number):
            Book.objects.create(
                isbn_number=book_id,
                title=f"test_{book_id}",
                author="author",
                publication_date="2021-01-06",
                number_of_pages=220,
                cover_link="link",
                publication_language="test",
            )

    def test_books_rest_view_url(self):
        response = self.client.get("/v1/books/")
        self.assertEqual(response.status_code, 200)

    def test_get_all_books_rest(self):
        response = self.client.get(reverse("books_list_REST"))
        self.assertEqual(response.status_code, 200)
        books = json.loads(response.content)
        self.assertEqual(len(books), 10)

    def test_rest_filter_text(self):
        response = self.client.get(reverse("books_list_REST") + "?title=test_8")
        self.assertEqual(response.status_code, 200)
        book = json.loads(response.content)
        self.assertEqual(len(book), 1)
        self.assertEqual(book[0]["title"], "test_8")

    def test_rest_filter_date_for_all_results(self):
        response = self.client.get(
            reverse("books_list_REST") + "?publication_date_start=2021-01-05"
        )
        self.assertEqual(response.status_code, 200)
        books = json.loads(response.content)
        self.assertEqual(len(books), 10)

    def test_rest_filter_date_for_no_results(self):
        response = self.client.get(
            reverse("books_list_REST") + "?publication_date_end=2021-01-05"
        )
        self.assertEqual(response.status_code, 200)
        books = json.loads(response.content)
        self.assertEqual(len(books), 0)


class TestAddBooksGoogleAPI(TestCase):
    def test_add_books_google_api_view_url(self):
        response = self.client.get("/books/add_book_using_api")
        self.assertEqual(response.status_code, 200)

    def test_add_books_google_api_view_uses_correct_template(self):
        response = self.client.get(reverse("add_books_using_api"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_books_using_api.html")

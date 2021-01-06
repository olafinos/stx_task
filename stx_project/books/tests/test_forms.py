from django.test import TestCase
from ..forms import GoogleBooksAPIForm, BookSearchForm


class TestGoogleBooksAPIForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = GoogleBooksAPIForm()

    def test_q_max_length(self):
        self.assertEqual(self.form.fields["q"].max_length, 150)

    def test_q_required(self):
        self.assertEqual(self.form.fields["q"].required, False)

    def test_intitle_max_length(self):
        self.assertEqual(self.form.fields["intitle"].max_length, 150)

    def test_intitle_required(self):
        self.assertEqual(self.form.fields["intitle"].required, False)

    def test_inauthor_max_length(self):
        self.assertEqual(self.form.fields["inauthor"].max_length, 150)

    def test_inauthor_required(self):
        self.assertEqual(self.form.fields["inauthor"].required, False)

    def test_inpublisher_max_length(self):
        self.assertEqual(self.form.fields["inpublisher"].max_length, 150)

    def test_inpublisher_required(self):
        self.assertEqual(self.form.fields["inpublisher"].required, False)

    def test_subject_max_length(self):
        self.assertEqual(self.form.fields["subject"].max_length, 150)

    def test_subject_required(self):
        self.assertEqual(self.form.fields["subject"].required, False)

    def test_isbn_max_length(self):
        self.assertEqual(self.form.fields["isbn"].max_length, 13)

    def test_isbn_required(self):
        self.assertEqual(self.form.fields["isbn"].required, False)

    def test_lccn_max_length(self):
        self.assertEqual(self.form.fields["lccn"].max_length, 13)

    def test_lccn_required(self):
        self.assertEqual(self.form.fields["lccn"].required, False)

    def test_oclc_required(self):
        self.assertEqual(self.form.fields["oclc"].required, False)


class TestBookSearchForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = BookSearchForm()

    def test_title_max_length(self):
        self.assertEqual(self.form.fields["title"].max_length, 150)

    def test_title_required(self):
        self.assertEqual(self.form.fields["title"].required, False)

    def test_author_max_length(self):
        self.assertEqual(self.form.fields["author"].max_length, 150)

    def test_author_required(self):
        self.assertEqual(self.form.fields["author"].required, False)

    def test_publication_date_start_required(self):
        self.assertEqual(self.form.fields["publication_date_start"].required, False)

    def test_publication_date_end_required(self):
        self.assertEqual(self.form.fields["publication_date_end"].required, False)

    def test_publication_language_max_length(self):
        self.assertEqual(self.form.fields["publication_language"].max_length, 150)

    def test_publication_language_required(self):
        self.assertEqual(self.form.fields["publication_language"].required, False)

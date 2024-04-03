from django.test import TestCase
from books_service.models import Book


class BookModelTestCase(TestCase):
    def setUp(self):
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'cover': 'HARD',
            'inventory': 10,
            'daily_fee': 5.99
        }

    def test_create_book(self):
        book = Book.objects.create(**self.book_data)
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.cover, 'HARD')
        self.assertEqual(book.inventory, 10)
        self.assertEqual(book.daily_fee, 5.99)

    def test_book_string_representation(self):
        book = Book.objects.create(**self.book_data)
        self.assertEqual(str(book), 'Test Book Test Author 5.99')

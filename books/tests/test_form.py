from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from books.models import Author, Book
from books.forms import BookForm, AuthorForm, OrderForm, BookReviewForm


class BookFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.author = Author.objects.create(name='Author Name')
        self.request = RequestFactory().get('/')
        self.request.user = self.user

    def test_form_valid_data(self):
        form_data = {
            'title': 'Test Book',
            'author': self.author.id,
            'description': 'A short description.',
            'price': 19.99,
            'number_pages': 200,
            'year': 2024
        }
        form = BookForm(data=form_data, request=self.request)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            'title': 'Test Book',
            'author': self.author.id,
            'description': 'x' * 501,
            'price': 19.99,
            'number_pages': 200,
            'year': 2024
        }
        form = BookForm(data=form_data, request=self.request)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_form_save(self):
        form_data = {
            'title': 'Test Book',
            'author': self.author.id,
            'description': 'A short description.',
            'price': 19.99,
            'number_pages': 200,
            'year': 2024
        }
        form = BookForm(data=form_data, request=self.request)
        if form.is_valid():
            book = form.save()
            self.assertEqual(book.title, 'Test Book')
            self.assertEqual(book.created_by, self.user)


class AuthorFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.request = RequestFactory().get('/')
        self.request.user = self.user

    def test_form_valid_data(self):
        form_data = {
            'name': 'New Author'
        }
        form = AuthorForm(data=form_data, request=self.request)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form_data = {
            'name': 'New Author'
        }
        form = AuthorForm(data=form_data, request=self.request)
        if form.is_valid():
            author = form.save()
            self.assertEqual(author.name, 'New Author')
            self.assertEqual(author.created_by, self.user)


class OrderFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.request = RequestFactory().get('/')
        self.request.user = self.user

    def test_form_valid_data(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'country': 'USA',
            'city': 'Any town',
            'postal_code': '12345',
            'card_number': '4111111111111111',
            'card_cvv': '123',
            'expiry_date': '12/25'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'country': 'USA',
            'city': 'Any town',
            'postal_code': '12345',
            'card_number': '4111111111111111',
            'card_cvv': '123',
            'expiry_date': '12/25'
        }
        form = OrderForm(data=form_data)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = self.user
            order.save()
            self.assertEqual(order.first_name, 'John')
            self.assertEqual(order.user, self.user)


class BookReviewFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.author = Author.objects.create(name='Author Name')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            description='A short description.',
            price=19.99,
            number_pages=200,
            year=2024,
            created_by=self.user
        )
        self.request = RequestFactory().get('/')
        self.request.user = self.user

    def test_form_valid_data(self):
        form_data = {
            'rating': 5,
            'comment': 'Excellent book!'
        }
        form = BookReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form_data = {
            'rating': 5,
            'comment': 'Excellent book!'
        }
        form = BookReviewForm(data=form_data)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = self.user
            review.book = self.book
            review.save()
            self.assertEqual(review.rating, 5)
            self.assertEqual(review.book, self.book)
            self.assertEqual(review.user, self.user)

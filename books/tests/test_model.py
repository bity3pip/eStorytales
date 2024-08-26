from django.test import TestCase
from django.contrib.auth.models import User
from books.models import Author, Book, BookReview, Order, OrderItem, CardItem, Card


class AuthorModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.author = Author.objects.create(name='Author Name', created_by=self.user)

    def test_author_str(self):
        self.assertEqual(str(self.author), 'Author Name')

    def test_author_creation(self):
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(self.author.name, 'Author Name')
        self.assertEqual(self.author.created_by, self.user)


class BookModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.author = Author.objects.create(name='Author Name', created_by=self.user)
        self.book = Book.objects.create(
            title='Test Book',
            description='A short description.',
            author=self.author,
            created_by=self.user,
            year=2024,
            number_pages=200,
            price=19.99
        )

    def test_book_str(self):
        self.assertEqual(str(self.book), f'Book Test Book: {self.book.id}')

    def test_get_absolute_url(self):
        self.assertEqual(self.book.get_absolute_url(), '/')

    def test_book_creation(self):
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.created_by, self.user)


class BookReviewModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.author = Author.objects.create(name='Author Name', created_by=self.user)
        self.book = Book.objects.create(
            title='Test Book',
            description='A short description.',
            author=self.author,
            created_by=self.user,
            year=2024,
            number_pages=200,
            price=19.99
        )
        self.review = BookReview.objects.create(
            book=self.book,
            user=self.user,
            rating=5,
            comment='Excellent book!'
        )

    def test_review_str(self):
        self.assertEqual(str(self.review), f'Test Book - test_user')

    def test_review_creation(self):
        self.assertEqual(BookReview.objects.count(), 1)
        self.assertEqual(self.review.book, self.book)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Excellent book!')


class OrderModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.author = Author.objects.create(name='Author Name', created_by=self.user)

        self.book = Book.objects.create(
            title='Test Book',
            description='A short description.',
            author=self.author,
            created_by=self.user,
            year=2024,
            number_pages=200,
            price=19.99
        )

        self.order = Order.objects.create(user=self.user,
                                          first_name='John',
                                          last_name='Doe',
                                          address='123 Main St',
                                          country='Country',
                                          city='City',
                                          postal_code='12345')

        self.order_item = OrderItem.objects.create(
            order=self.order,
            book=self.book,
            quantity=3
        )

    def test_order_item_creation(self):
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.book, self.book)
        self.assertEqual(self.order_item.quantity, 3)


class OrderItemModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.author = Author.objects.create(name='Author Name', created_by=self.user)

        self.book = Book.objects.create(
            title='Test Book',
            description='A short description.',
            author=self.author,
            created_by=self.user,
            year=2024,
            number_pages=200,
            price=19.99
        )

        self.order = Order.objects.create(
            user=self.user,
            product=self.book,
            first_name='John',
            last_name='Doe',
            address='123 Main St',
            country='USA',
            city='Any town',
            postal_code='12345',
            card_number='4111111111111111',
            card_cvv='123',
            expiry_date='12/25'
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            book=self.book,
            quantity=3
        )

    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), '3 of Test Book')

    def test_order_item_creation(self):
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.book, self.book)
        self.assertEqual(self.order_item.quantity, 3)


class CardModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.author = Author.objects.create(name='Author Name', created_by=self.user)

        self.book = Book.objects.create(
            title='Test Book',
            description='A short description.',
            author=self.author,
            created_by=self.user,
            year=2024,
            number_pages=200,
            price=19.99
        )

        self.card = Card.objects.create(user=self.user)
        self.card_item = CardItem.objects.create(
            card=self.card,
            book=self.book,
            quantity=2
        )
        self.card.items.add(self.card_item)

    def test_card_total_price(self):
        self.assertEqual(self.card.total_price, 19.99 * 2)

    def test_card_total_items(self):
        self.assertEqual(self.card.total_items, 2)

    def test_update_quantity(self):
        self.card.update_quantity(self.book, 5)
        self.card.refresh_from_db()
        self.assertEqual(self.card.items.count(), 1)
        self.assertEqual(self.card.items.first().quantity, 5)

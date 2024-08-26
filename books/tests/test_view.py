from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from books.models import Book, Author, Card, CardItem, Order, OrderItem


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.author = Author.objects.create(name='Author Name', created_by=cls.user)

        cls.book = Book.objects.create(
            title='Test Book',
            description='Description for Test Book',
            author=cls.author,
            created_by=cls.user,
            year=2024,
            number_pages=200,
            price=19.99
        )

    def test_book_str(self):
        self.assertEqual(str(self.book), f'Book {self.book.title}: {self.book.id}')


class BookListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.author = Author.objects.create(name='Author Name', created_by=cls.user)

        cls.book1 = Book.objects.create(
            title='Test Book 1',
            description='Description for Test Book 1',
            author=cls.author,
            created_by=cls.user,
            year=2024,
            number_pages=200,
            price=19.99
        )
        cls.book2 = Book.objects.create(
            title='Test Book 2',
            description='Description for Test Book 2',
            author=cls.author,
            created_by=cls.user,
            year=2024,
            number_pages=300,
            price=29.99
        )

    def test_book_list_view(self):
        response = self.client.get(reverse('books-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertContains(response, self.book1.title)
        self.assertContains(response, self.book2.title)

        if self.book1.image:
            self.assertContains(response, self.book1.image.url)
        if self.book2.image:
            self.assertContains(response, self.book2.image.url)


class BookDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.author = Author.objects.create(name='Author Name', created_by=cls.user)

        cls.book = Book.objects.create(
            title='Test Book',
            description='Description for Test Book',
            author=cls.author,
            created_by=cls.user,
            year=2024,
            number_pages=200,
            price=19.99
        )

    def test_book_detail_view(self):
        response = self.client.get(reverse('books-detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.book.description)

        if self.book.image:
            self.assertContains(response, self.book.image.url)


class CreateBookViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')

    def test_create_book(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('books-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_book.html')

        data = {
            'title': 'New Book',
            'description': 'New Book Description',
            'author': Author.objects.create(name='New Author', created_by=self.user).id,
            'year': 2024,
            'number_pages': 150,
            'price': 15.99
        }
        response = self.client.post(reverse('books-create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title='New Book').exists())


class CreateAuthorViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')

    def setUp(self):
        self.client.login(username='test_user', password='test_password')

    def test_create_author(self):
        response = self.client.get(reverse('books-create-author'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_author.html')

        data = {
            'name': 'New Author',
            'created_by': self.user.id
        }
        response = self.client.post(reverse('books-create-author'), data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(Author.objects.filter(name='New Author').exists())


class CardViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.author = Author.objects.create(name='Author Name', created_by=cls.user)
        cls.book = Book.objects.create(
            title='Test Book',
            description='Description for Test Book',
            author=cls.author,
            created_by=cls.user,
            year=2024,
            number_pages=200,
            price=19.99
        )

    def test_add_to_card(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.post(reverse('add-to-card', kwargs={'book_id': self.book.id}), {'quantity': 1})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CardItem.objects.filter(book=self.book, quantity=1).exists())

    def test_card_view(self):
        self.client.login(username='test_user', password='test_password')
        card, created = Card.objects.get_or_create(user=self.user)
        CardItem.objects.create(card=card, book=self.book, quantity=1)

        response = self.client.get(reverse('card-view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'card.html')
        self.assertContains(response, self.book.title)


class CheckoutViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.author = Author.objects.create(name='Author Name', created_by=cls.user)
        cls.book = Book.objects.create(
            title='Test Book',
            description='Description for Test Book',
            author=cls.author,
            created_by=cls.user,
            year=2024,
            number_pages=200,
            price=19.99
        )

    def setUp(self):
        self.client.login(username='test_user', password='test_password')

    def test_checkout_view(self):
        card, created = Card.objects.get_or_create(user=self.user)
        CardItem.objects.create(card=card, book=self.book, quantity=1)

        card_items = CardItem.objects.filter(card=card)
        print(f"CardItem count for card: {card_items.count()}")
        for item in card_items:
            print(f"CardItem: Book - {item.book.title}, Quantity - {item.quantity}")

        response = self.client.get(reverse('books-checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout.html')

        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'country': 'USA',
            'city': 'Any town',
            'postal_code': '12345',
            'card_number': '1234567812345678',
            'card_cvv': '123',
            'expiry_date': '12/25',
        }
        response = self.client.post(reverse('books-checkout'), data)

        if response.status_code != 302:
            form = response.context['form']
            print("Form errors:", form.errors)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('complete-order'))

        self.assertTrue(Order.objects.filter(user=self.user).exists())
        order = Order.objects.filter(user=self.user).first()
        print(f"Order ID: {order.id}")

        order_items = OrderItem.objects.filter(order=order)
        print(f"OrderItems count: {order_items.count()}")
        for item in order_items:
            print(f"OrderItem: Book - {item.book.title}, Quantity - {item.quantity}")

        self.assertTrue(order_items.filter(book=self.book).exists())
        if not order_items.filter(book=self.book).exists():
            print(f"No OrderItem found for book: {self.book.title}")


class OrderConfirmationViewTest(TestCase):

    def test_order_confirmation_view(self):
        response = self.client.get(reverse('complete-order'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_confirmation.html')


class BookReviewFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.author = Author.objects.create(name='Author Name', created_by=cls.user)
        cls.book = Book.objects.create(
            title='Test Book',
            description='Description for Test Book',
            author=cls.author,
            created_by=cls.user,
            year=2024,
            number_pages=200,
            price=19.99
        )

    def test_valid_form_submission(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.post(reverse('books-detail', kwargs={'pk': self.book.pk}), {
            'rating': 5,
            'review_text': 'Great book!'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(self.book.reviews.filter(rating=5).exists())

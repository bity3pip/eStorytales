from django.db import models
from django.db.models.functions import Now
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings


class Author(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='books_created')
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    year = models.IntegerField()
    number_pages = models.IntegerField()
    rating = models.IntegerField(default=0)
    price = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'book'
        ordering = ['title']

    def __str__(self):
        return f'Book {self.title}: {self.id}'

    def get_absolute_url(self):
        return reverse('books-list')


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    rating = models.IntegerField(choices=[(i, i) for i in range(6)], default=0)
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(db_default=Now())

    class Meta:
        db_table = 'book_review'

    def __str__(self):
        return f'{self.book.title} - {self.user.username}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Book)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    card_cvv = models.CharField(max_length=3, null=True, blank=True)
    expiry_date = models.CharField(max_length=5, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.first_name} {self.last_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} of {self.book.title}'


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('CardItem', related_name='cards', blank=True)

    @property
    def total_price(self):
        return sum(item.book.price * item.quantity for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def update_quantity(self, book, quantity):
        card_item, created = CardItem.objects.get_or_create(card=self, book=book)
        if quantity <= 0:
            card_item.delete()
        else:
            card_item.quantity = quantity
            card_item.save()


class CardItem(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, default=1, related_name='card_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} {self.book.title}'

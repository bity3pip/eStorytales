from django.db import models
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
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        db_table = 'book_review'


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = 'comment'
        ordering = ['book', 'text']


class Order(models.Model):
    product = models.ForeignKey(Book, max_length=200, null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

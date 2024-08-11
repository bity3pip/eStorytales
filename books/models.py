from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books_created', default=1)
    image = models.ImageField(upload_to='books', null=True, blank=True)
    year = models.IntegerField()
    number_pages = models.IntegerField()
    rating = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'book'
        ordering = ['title']

    def __str__(self):
        return f'Book {self.title}: {self.id}'

    def get_absolute_url(self):
        return reverse('books')


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

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/books', null=True, blank=True)
    year = models.IntegerField()
    number_pages = models.IntegerField()
    rating = models.FloatField()
    price = models.IntegerField()

    class Meta:
        db_table = 'books'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'pk': self.pk})


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        db_table = 'book_review'

from django import forms
from django.contrib.auth.models import User

from books.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)
        self.instance.author = User.objects.get(username='author')
        self.instance.save()
        return instance

    def clean(self):
        text = self.cleaned_data.get('text')
        if text and len(text) > 500:
            return self.add_error('text', 'Text too long')
        return text

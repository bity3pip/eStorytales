from django import forms
from django.contrib.auth.models import User

from books.models import Book, Author


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.all()

    class Meta:
        model = Book
        exclude = ['rating', 'created_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)
        self.instance.author = User.objects.get(username='user')
        self.instance.save()
        return instance

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text and len(text) > 500:
            return self.add_error('text', 'Text too long')
        return text


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

    def save(self, commit=True):
        instance = super(AuthorForm, self).save(commit=False)
        self.instance.author = User.objects.get(username='user')
        self.instance.save()
        return instance

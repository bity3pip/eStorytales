from django import forms
from django.core.exceptions import ValidationError
from books.models import Book, Author


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.all()

    class Meta:
        model = Book
        exclude = ['rating', 'created_by']

    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)
        if self.request:
            instance.created_by = self.request.user
        if commit:
            instance.save()
        return instance

    def clear_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 500:
            raise ValidationError('Description too long')
        return description


class AuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AuthorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Author
        fields = ['name']

    def save(self, commit=True):
        instance = super(AuthorForm, self).save(commit=False)
        if self.request:
            instance.created_by = self.request.user
        if commit:
            instance.save()
        return instance

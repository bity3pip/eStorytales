from django import forms
from django.core.exceptions import ValidationError
from books.models import Book, Author, Order, BookReview


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

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 1000:
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


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'country',
                  'city', 'postal_code', 'card_number', 'card_cvv', 'expiry_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'card_number': forms.NumberInput(attrs={
                'class': 'form-control', 'maxlength': '16', 'placeholder': 'Card Number'}),
            'card_cvv': forms.NumberInput(attrs={'class': 'form-control', 'maxlength': '3', 'placeholder': 'CVV'}),
            'expiry_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}),
        }


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, '★' * i) for i in range(1, 6)],
                attrs={'class': 'rating-stars'}
            ),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Leave your comment here'}),
        }

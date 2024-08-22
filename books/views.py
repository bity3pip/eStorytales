from django.views.generic import ListView, DeleteView, DetailView
from books.models import Book, Author, Order
from books.forms import BookForm, AuthorForm
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
import json


class BookListView(ListView):
    model = Book
    template_name = 'list.html'


class BookDetailView(DetailView):
    model = Book
    template_name = 'detail.html'


class SearchResultsListView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(Q(title__icontains=query) | Q(author__book__title__icontains=query))


class BookCheckoutView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'checkout.html'
    login_url = 'login'


def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    product = Book.objects.get(id=body['product_id'])
    Order.objects.create(
        product=product)
    return JsonResponse('Payment Complete!', safe=False)


def books_list(request):
    filter_price = request.GET.get('price')
    filter_author = request.GET.get('author')
    filter_name = request.GET.get('name')

    list_books = Book.objects.all()

    if filter_price:
        list_books = Book.objects.filter(price__gte=filter_price)

    if filter_author:
        list_books = Author.objects.filter(name=filter_author)

    if filter_name:
        list_books = Book.objects.filter(title__contains=filter_name)

    context = {'books_list': list_books}
    return render(request, 'list.html', context=context)


@login_required
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            form.save()
            return redirect('books-list')
        else:
            return render(request, 'create_book.html', {'form': form})
    else:
        form = BookForm(request=request)
        return render(request, 'create_book.html', {'form': form})


# class BookCreateFormView(FormView):
#     model = Book
#     form_class = BookForm
#     template_name = 'create_book.html'
#     success_url = '/books'


# class AuthorCreateView(CreateView):
#     model = Author
#     form_class = AuthorForm
#     template_name = 'create_author.html'


@login_required
def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('create-book')
        else:
            return render(request, 'create_author.html', {'form': form})
    else:
        form = AuthorForm(request=request)
        return render(request, 'create_author.html', {'form': form})

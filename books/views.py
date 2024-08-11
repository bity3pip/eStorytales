from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from books.forms import BookForm
from books.models import Book


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def books_list(request):
    list_books = Book.objects.all()
    context = {'books_list': list_books}
    return render(request, 'list.html', context=context)


def books_add(request):
    if request.method == 'POST':
        create_form = BookForm(request.POST, request.FILES)
        if create_form.is_valid():
            book = create_form.save(commit=False)
            book.created_by = request.user
            book.save()
            return redirect('books')
        else:
            return JsonResponse(create_form.errors)
    else:
        form = BookForm()
        return render(request, 'create.html', {'form': form})


def book_delete(request, book_id):
    book = Book.objects.get(pk=book_id)
    book.delete()
    return JsonResponse({"text": "Post deleted successfully."})


class BookListView(ListView):
    model = Book
    template_name = 'list.html'

    def get_queryset(self):
        filter_name = self.request.GET.get('name')
        if filter_name:
            return Book.objects.filter(title__contains=filter_name)
        else:
            return Book.objects.all()


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'create.html'

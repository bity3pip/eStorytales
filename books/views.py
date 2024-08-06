from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from books.forms import BookForm
from books.models import Book

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def books_list(request):
    context = {'books_list': [{'title': 'Hello world',
                               'text': 'Books here'},
                              {'title': 'Hello world',
                               'text': 'Books here'},
                              {'title': 'Hello world',
                               'text': 'Books here'},
                              {'title': 'Hello world',
                               'text': 'Books here'}]}
    return render(request, 'list.html', context=context)


def books_add(request):
    if request.method == 'POST':
        print(request.POST)
        create_form = BookForm(request.POST, request.FILES)
        if create_form.is_valid():
            create_form.save()
            return JsonResponse({"text": "Post created successfully."})
        else:
            return JsonResponse(create_form.errors)
    else:
        form = BookForm()
        return render(request, 'create.html', {'form': form})


def book_delete(request, post_id):
    book = Book.objects.get(pk=post_id)
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

from django.db import transaction
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from books.models import Book, Card, CardItem, OrderItem
from books.forms import BookForm, AuthorForm, OrderForm, BookReviewForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.db.models import Q, Avg


class BookListView(ListView):
    model = Book
    template_name = 'list.html'


class BookDetailView(DetailView):
    model = Book
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        rounded_average_rating = round(average_rating)
        review_form = BookReviewForm()

        context.update({
            'reviews': reviews,
            'average_rating': rounded_average_rating,
            'review_form': review_form,
        })

        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = BookReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = self.object
            review.user = request.user
            review.save()
            return redirect('books-detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(review_form=form))


class UpdateQuantityView(View):
    def post(self, request, book_id, *args, **kwargs):
        card = get_object_or_404(Card, user=request.user)
        book = get_object_or_404(Book, id=book_id)
        quantity = int(request.POST.get('quantity', 1))

        card.update_quantity(book, quantity)

        return redirect('card-view')


class SearchResultsListView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(Q(title__icontains=query))


class BookCheckoutView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'checkout.html'
    login_url = 'login'


@login_required
def checkout_view(request):
    card, created = Card.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                print(f"Order created with ID: {order.id}")

                for card_item in card.items.all():
                    OrderItem.objects.create(
                        order=order,
                        book=card_item.book,
                        quantity=card_item.quantity
                    )

                    print(f"OrderItem created for book: {card_item.book.title}")
                card.items.all().delete()
                return redirect('complete-order')
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Form errors:", form.errors)
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form, 'card': card})


def order_confirmation(request):
    return render(request, 'order_confirmation.html')


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


@login_required
def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('books-create')
        else:
            return render(request, 'create_author.html', {'form': form})
    else:
        form = AuthorForm(request=request)
        return render(request, 'create_author.html', {'form': form})


class AboutStore(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store_name'] = 'eStorytales'
        context['store_description'] = 'You can find your dream book.'
        context['store_address'] = 'Manhattan, NY 10036'
        context['store_phone'] = '+4777890123'
        context['store_hours'] = 'Mon-Sun, 10:00 a.m. to 9:00 p.m.'
        return context


class ContactView(TemplateView):
    template_name = 'contact.html'


class DeliveryView(TemplateView):
    template_name = 'delivery.html'


class PaymentView(TemplateView):
    template_name = 'payment.html'


def card_view(request):
    if request.user.is_authenticated:
        card, created = Card.objects.get_or_create(user=request.user)
        return render(request, 'card.html', {'card': card})
    return redirect('login')


def add_to_card(request, book_id):
    if request.user.is_authenticated:
        card, created = Card.objects.get_or_create(user=request.user)
        book = Book.objects.get(id=book_id)

        with transaction.atomic():
            card_item, created = CardItem.objects.get_or_create(card=card, book=book)
            if not created:
                card_item.quantity += 1
            else:
                card_item.quantity = 1
            card_item.save()
            card.items.add(card_item)

        return redirect('card-view')
    return redirect('login')


def remove_from_card(request, book_id):
    if request.user.is_authenticated:
        card, created = Card.objects.get_or_create(user=request.user)
        book = get_object_or_404(Book, id=book_id)
        card_item = get_object_or_404(CardItem, card=card, book=book)

        card.items.remove(card_item)
        card_item.delete()
        return redirect('card-view')
    return redirect('login')

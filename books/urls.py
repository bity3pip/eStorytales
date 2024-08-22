from .views import (BookListView, BookDetailView, BookCheckoutView, paymentComplete, SearchResultsListView, create_book,
                    create_author)
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('', BookListView.as_view(), name='books-list'),
    path('create/', create_book, name='books-create'),
    path('create/author', create_author, name='books-create-author'),
    path('<int:pk>/', BookDetailView.as_view(), name='books-detail'),
    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name='books-checkout'),
    path('complete/', paymentComplete, name='payment-complete'),
    path('search/', SearchResultsListView.as_view(), name='search-results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

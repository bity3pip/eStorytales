from .views import (BookListView, BookDetailView, checkout_view, order_confirmation, SearchResultsListView, AboutStore,
                    create_book, create_author, ContactView, DeliveryView, PaymentView, card_view, add_to_card,
                    remove_from_card, UpdateQuantityView)
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

urlpatterns = [
                  path('', BookListView.as_view(), name='books-list'),
                  path('create/', create_book, name='books-create'),
                  path('create/author', create_author, name='books-create-author'),
                  path('<int:pk>/', BookDetailView.as_view(), name='books-detail'),
                  path('checkout/', checkout_view, name='books-checkout'),
                  path('complete/', order_confirmation, name='complete-order'),
                  path('search/', SearchResultsListView.as_view(), name='search-results'),
                  path('about/', AboutStore.as_view(), name='about'),
                  path('contact/', ContactView.as_view(), name='contact'),
                  path('delivery/', DeliveryView.as_view(), name='delivery'),
                  path('payment/', PaymentView.as_view(), name='payment'),
                  path('card/', card_view, name='card-view'),
                  path('card/update_quantity/<int:book_id>/', UpdateQuantityView.as_view(), name='update-quantity'),
                  path('card/add/<int:book_id>', add_to_card, name='add-to-card'),
                  path('card/remove/<int:book_id>', remove_from_card, name='remove-from-card'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

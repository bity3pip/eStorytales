from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path
from books.views import books_list, books_add, book_delete, BookListView, BookCreateView


urlpatterns = ([
    path('admin/', admin.site.urls),
    path('books/', books_list, name='general'),
    path('books/create', BookCreateView.as_view(), name='books_create'),
    path('books/delete/<int:pk>', book_delete, name='books_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls())
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from django.urls import path, include
from books.views import books_list, books_add, book_delete, BookListView, BookCreateView, AuthorCreateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', books_list, name='books'),
    path('books/create', BookCreateView.as_view(), name='books_create'),
    path('authors/create', AuthorCreateView.as_view(), name='authors_create'),
    path('books/delete/<int:pk>', book_delete, name='books_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('__debug__/', include(debug_toolbar.urls)),]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \

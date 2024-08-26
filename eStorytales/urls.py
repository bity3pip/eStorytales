from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
import debug_toolbar

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('books.urls')),
                  path('', include("accounts.urls")),
                  path('accounts/', include('django.contrib.auth.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
                  path('__debug__/', include(debug_toolbar.urls)), ]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

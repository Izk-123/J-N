from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('products/', include('products.urls')),
    path('services/', include('services.urls')),
    path('projects/', include('projects.urls')),
    path('gallery/', include('gallery.urls')),
    path('contact/', include('contacts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

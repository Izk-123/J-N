from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── Group landing page (root)
    path('', include('core.urls')),

    # ── Subsidiary websites
    path('products/',     include('products.urls')),      # Blue Rock Wall Putty
    path('construction/', include('construction.urls')),  # Construction Company
    path('mining/',       include('mining.urls')),        # Mining Company
    path('timber/',       include('timber.urls')),        # Timber Company

    # ── Shared utilities
    path('gallery/',  include('gallery.urls')),
    path('contact/',  include('contacts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

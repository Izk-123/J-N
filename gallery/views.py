from django.views.generic import ListView
from .models import GalleryImage


class GalleryView(ListView):
    model = GalleryImage
    template_name = 'gallery/gallery.html'
    context_object_name = 'images'

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)
        category = self.request.GET.get('category', '')
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_category'] = self.request.GET.get('category', '')
        return context
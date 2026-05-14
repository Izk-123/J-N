from django.shortcuts import render
from .models import GalleryImage


def gallery(request):
    category = request.GET.get('category', '')
    images = GalleryImage.objects.filter(is_active=True)
    if category:
        images = images.filter(category=category)
    return render(request, 'gallery/gallery.html', {'images': images, 'active_category': category})

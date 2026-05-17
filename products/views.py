from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from core.models import Testimonial
from .models import Product, Category, BuildingSettings

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True).select_related('category')
        category_slug = self.request.GET.get('category', '')
        search = self.request.GET.get('q', '').strip()

        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(description__icontains=search)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.request.GET.get('category', '')
        search = self.request.GET.get('q', '').strip()

        context['categories'] = Category.objects.all()
        context['active_category'] = Category.objects.filter(slug=category_slug).first()
        context['search'] = search
        context['site'] = BuildingSettings.get()   # ✅ dynamic site settings
        context['testimonials'] = Testimonial.objects.filter(
            is_active=True, 
            source='products'      # only show testimonials for this sub‑site
        )[:6]

        # HTMX partial response detection
        if self.request.headers.get('HX-Request') == 'true':
            self.template_name = 'products/_product_grid.html'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['related'] = Product.objects.filter(
            category=product.category, is_active=True
        ).exclude(pk=product.pk)[:4]
        context['site'] = BuildingSettings.get()   # ✅ dynamic site settings
        return context
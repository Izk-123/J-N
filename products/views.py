from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)
        category_slug = self.request.GET.get('category')
        if category_slug:
            self.active_category = get_object_or_404(Category, slug=category_slug)
            qs = qs.filter(category=self.active_category)
        else:
            self.active_category = None
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['active_category'] = self.active_category
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
        return context
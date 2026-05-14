from django.views.generic import TemplateView, ListView
from .models import TimberSettings, TimberProduct, TimberCategory, TimberProject


class TimberMixin:
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tsite'] = TimberSettings.get()
        return ctx


class TimberHomeView(TimberMixin, TemplateView):
    template_name = 'timber/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['featured_products'] = TimberProduct.objects.filter(is_featured=True, is_active=True)[:6]
        ctx['featured_projects'] = TimberProject.objects.filter(is_featured=True)[:3]
        ctx['categories'] = TimberCategory.objects.all()
        return ctx


class TimberAboutView(TimberMixin, TemplateView):
    template_name = 'timber/about.html'


class TimberProductsView(TimberMixin, ListView):
    template_name = 'timber/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = TimberProduct.objects.filter(is_active=True)
        cat = self.request.GET.get('category')
        if cat:
            qs = qs.filter(category__slug=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = TimberCategory.objects.all()
        ctx['active_category'] = self.request.GET.get('category', '')
        return ctx


class TimberProjectsView(TimberMixin, ListView):
    template_name = 'timber/projects.html'
    context_object_name = 'projects'
    queryset = TimberProject.objects.all()


class TimberContactView(TimberMixin, TemplateView):
    template_name = 'timber/contact.html'

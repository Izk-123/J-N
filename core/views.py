from django.views.generic import TemplateView
from products.models import Product
from services.models import Service
from projects.models import Project
from core.models import Testimonial


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(
            is_featured=True, is_active=True
        )[:6]
        context['featured_services'] = Service.objects.filter(
            is_featured=True, is_active=True
        )[:4]
        context['featured_projects'] = Project.objects.filter(
            is_featured=True, is_active=True
        )[:3]
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:4]
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
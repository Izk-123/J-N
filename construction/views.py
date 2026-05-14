from django.views.generic import TemplateView, DetailView, ListView
from django.shortcuts import get_object_or_404

from core.models import Testimonial

from .models import (
    ConstructionConfig, ConstructionFact, ConstructionService,
    ConstructionProject, TeamMember
)

class ConstructionMixin:
    """Injects ConstructionConfig into every view's context."""
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['csite'] = ConstructionConfig.get()
        return ctx


class ConstructionHomeView(ConstructionMixin, TemplateView):
    template_name = 'construction/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['featured_services'] = ConstructionService.objects.filter(is_featured=True)[:6]
        ctx['featured_projects'] = ConstructionProject.objects.filter(is_featured=True)[:3]
        ctx['team'] = TeamMember.objects.filter(is_active=True)[:4]
        ctx['testimonials'] = Testimonial.objects.filter(is_active=True)[:5]
        ctx['facts'] = ConstructionFact.objects.filter(is_active=True)
        return ctx


class ConstructionAboutView(ConstructionMixin, TemplateView):
    template_name = 'construction/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['team'] = TeamMember.objects.filter(is_active=True)
        return ctx


class ConstructionServicesView(ConstructionMixin, ListView):
    template_name = 'construction/services.html'
    context_object_name = 'services'
    queryset = ConstructionService.objects.all().order_by('order')


class ConstructionProjectsView(ConstructionMixin, ListView):
    template_name = 'construction/projects.html'
    context_object_name = 'projects'
    queryset = ConstructionProject.objects.all()


class ConstructionProjectDetailView(ConstructionMixin, DetailView):
    template_name = 'construction/project_detail.html'
    context_object_name = 'project'
    model = ConstructionProject
    slug_field = 'slug'


class ConstructionContactView(ConstructionMixin, TemplateView):
    template_name = 'construction/contact.html'

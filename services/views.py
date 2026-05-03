from django.views.generic import ListView, DetailView
from .models import Service


class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
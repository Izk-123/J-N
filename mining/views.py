from django.views.generic import TemplateView, DetailView, ListView

from .models import (
    MiningConfig, MineralProduct, MineralCategory,
    MiningEquipment, MiningOperation
)


class MiningMixin:
    """Injects MiningConfig into every view's context."""
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['msite'] = MiningConfig.get()
        return ctx


class MiningHomeView(MiningMixin, TemplateView):
    template_name = 'mining/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['featured_minerals'] = MineralProduct.objects.filter(is_featured=True, is_active=True)[:6]
        ctx['operations'] = MiningOperation.objects.filter(is_active=True)[:3]
        ctx['equipment'] = MiningEquipment.objects.filter(is_active=True)[:4]
        ctx['categories'] = MineralCategory.objects.all()
        return ctx


class MiningAboutView(MiningMixin, TemplateView):
    template_name = 'mining/about.html'


class MiningMineralsView(MiningMixin, ListView):
    template_name = 'mining/minerals.html'
    context_object_name = 'minerals'

    def get_queryset(self):
        qs = MineralProduct.objects.filter(is_active=True)
        cat = self.request.GET.get('category')
        if cat:
            qs = qs.filter(category__slug=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = MineralCategory.objects.all()
        ctx['active_category'] = self.request.GET.get('category', '')
        return ctx


class MiningOperationsView(MiningMixin, ListView):
    template_name = 'mining/operations.html'
    context_object_name = 'operations'
    queryset = MiningOperation.objects.filter(is_active=True)


class MiningContactView(MiningMixin, TemplateView):
    template_name = 'mining/contact.html'

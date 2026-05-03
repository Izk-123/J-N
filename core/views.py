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
    

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import WhatsAppClick

@csrf_exempt
def log_whatsapp_click(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        page_path = data.get('path', '')
        product_id = data.get('product_id')
        contact_id = data.get('contact_id')
        ip = request.META.get('REMOTE_ADDR')

        click = WhatsAppClick.objects.create(
            page_path=page_path,
            product_id=product_id or None,
            contact_message_id=contact_id or None,
            ip_address=ip,
        )
        return JsonResponse({'status': 'ok', 'id': click.id})
    return JsonResponse({'status': 'error'}, status=400)
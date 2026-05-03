from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import TemplateView
from datetime import timedelta

from contacts.models import ContactMessage
from products.models import Product, Category
from services.models import Service
from projects.models import Project
from gallery.models import GalleryImage
from core.models import Testimonial


@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'admin/jn_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        last_30 = now - timedelta(days=30)
        last_7 = now - timedelta(days=7)

        stats = {
            'products': Product.objects.count(),
            'services': Service.objects.count(),
            'projects': Project.objects.count(),
            'gallery': GalleryImage.objects.count(),
            'testimonials': Testimonial.objects.count(),
            'categories': Category.objects.count(),
            'messages_total': ContactMessage.objects.count(),
            'messages_new': ContactMessage.objects.filter(status='new').count(),
            'messages_week': ContactMessage.objects.filter(created_at__gte=last_7).count(),
            'messages_month': ContactMessage.objects.filter(created_at__gte=last_30).count(),
        }

        recent_messages = ContactMessage.objects.order_by('-created_at')[:10]

        alerts = []
        if stats['messages_new'] > 0:
            alerts.append({
                'type': 'warning',
                'text': f"You have {stats['messages_new']} unread enquir{'y' if stats['messages_new'] == 1 else 'ies'} waiting for a reply."
            })
        if stats['products'] == 0:
            alerts.append({'type': 'info', 'text': 'No products added yet. Add your first product to show on the website.'})
        if stats['services'] == 0:
            alerts.append({'type': 'info', 'text': 'No services added yet. Add your construction services.'})

        context['title'] = 'J&N Dashboard'
        context['stats'] = stats
        context['recent_messages'] = recent_messages
        context['alerts'] = alerts
        return context
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from datetime import timedelta

from contacts.models import ContactMessage
from products.models import Product
from services.models import Service
from projects.models import Project
from gallery.models import GalleryImage
from core.models import Testimonial, Visitor, WhatsAppClick

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Only allow staff users
        if self.scope['user'].is_staff:
            await self.channel_layer.group_add('dashboard', self.channel_name)
            await self.accept()
            # Send initial data
            await self.send_dashboard_data()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('dashboard', self.channel_name)

    async def send_dashboard_data(self):
        data = await self.get_dashboard_data()
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def get_dashboard_data(self):
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)

        # Card stats
        stats = {
            'messages_new':    ContactMessage.objects.filter(status='new').count(),
            'messages_month':  ContactMessage.objects.filter(created_at__gte=now - timedelta(days=30)).count(),
            'products':        Product.objects.count(),
            'services':        Service.objects.count(),
            'projects':        Project.objects.count(),
            'gallery':         GalleryImage.objects.count(),
            'testimonials':    Testimonial.objects.count(),
            'visitors_today':  Visitor.objects.filter(created_at__date=today).count(),
            'visitors_week':   Visitor.objects.filter(created_at__gte=week_ago).count(),
            'whatsapp_today':  WhatsAppClick.objects.filter(created_at__date=today).count(),
            'whatsapp_week':   WhatsAppClick.objects.filter(created_at__gte=week_ago).count(),
        }

        # Charts data
        days = []
        enquiries_per_day = []
        visitors_per_day = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            days.append(day.strftime('%a'))
            enquiries_per_day.append(ContactMessage.objects.filter(created_at__date=day).count())
            visitors_per_day.append(Visitor.objects.filter(created_at__date=day).count())

        chart_data = {
            'weekdays': days,
            'enquiries': enquiries_per_day,
            'visitors': visitors_per_day,
            'content_labels': ['Products','Services','Projects','Gallery','Testimonials'],
            'content_values': [
                Product.objects.count(),
                Service.objects.count(),
                Project.objects.count(),
                GalleryImage.objects.count(),
                Testimonial.objects.count(),
            ]
        }

        # Recent messages (last 8)
        messages = []
        for msg in ContactMessage.objects.order_by('-created_at')[:8]:
            messages.append({
                'id': msg.id,
                'name': msg.name,
                'phone': msg.phone,
                'subject': msg.subject or 'General enquiry',
                'status': msg.status,
                'created_at': msg.created_at.strftime('%d %b'),
            })

        # Recent visitors (last 10)
        visitors = []
        for v in Visitor.objects.order_by('-created_at')[:10]:
            visitors.append({
                'path': v.path,
                'ip': v.ip_address,
                'device': v.device_type,
                'browser': v.browser,
                'time': v.created_at.strftime('%H:%M'),
            })

        return {
            'stats': stats,
            'chart': chart_data,
            'messages': messages,
            'visitors': visitors,
        }

    # Receives broadcast from a signal to refresh (you can call group_send from a model signal, etc.)
    async def dashboard_update(self, event):
        await self.send_dashboard_data()
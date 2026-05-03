# core/dashboard.py
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta

from contacts.models import ContactMessage
from products.models import Product
from services.models import Service
from projects.models import Project
from gallery.models import GalleryImage
from core.models import Testimonial, Visitor, WhatsAppClick


def dashboard_callback(request, context):
    """Called by Unfold to inject data into the admin index template."""
    now = timezone.now()
    today = now.date()
    week_ago = now - timedelta(days=7)

    # ── Core stats ─────────────────────────────────────────
    context['dash_stats'] = {
        'messages_new':   ContactMessage.objects.filter(status='new').count(),
        'messages_month': ContactMessage.objects.filter(created_at__gte=now - timedelta(days=30)).count(),
        'products':       Product.objects.count(),
        'services':       Service.objects.count(),
        'projects':       Project.objects.count(),
        'gallery':        GalleryImage.objects.count(),
        'testimonials':   Testimonial.objects.count(),
        'visitors_today':     Visitor.objects.filter(created_at__date=today).count(),
        'visitors_week':      Visitor.objects.filter(created_at__gte=week_ago).count(),
        'whatsapp_today':     WhatsAppClick.objects.filter(created_at__date=today).count(),
        'whatsapp_week':      WhatsAppClick.objects.filter(created_at__gte=week_ago).count(),
    }

    # ── Recent messages ────────────────────────────────────
    context['recent_messages'] = ContactMessage.objects.order_by('-created_at')[:8]
    context['alerts'] = _get_alerts()

    # ── Chart data (no ellipsis!) ──────────────────────────
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
        'enquiries_per_day': enquiries_per_day,
        'visitors_per_day': visitors_per_day,
        'content_labels': ['Products', 'Services', 'Projects', 'Gallery', 'Testimonials'],
        'content_values': [
            Product.objects.count(),
            Service.objects.count(),
            Project.objects.count(),
            GalleryImage.objects.count(),
            Testimonial.objects.count(),
        ]
    }
    context['chart_data'] = chart_data

    return context


def _get_alerts():
    alerts = []
    new = ContactMessage.objects.filter(status='new').count()
    if new:
        alerts.append({
            'type': 'warning',
            'icon': '📩',
            'text': f'{new} unread enquir{"y" if new == 1 else "ies"} waiting for a reply.'
        })
    if not Product.objects.filter(is_featured=True).exists():
        alerts.append({
            'type': 'info',
            'icon': '📦',
            'text': 'No featured products yet — tick "Is featured" on a product to show it on the homepage.'
        })
    if not Service.objects.filter(is_featured=True).exists():
        alerts.append({
            'type': 'info',
            'icon': '🔧',
            'text': 'No featured services — tick "Is featured" on a service to display it on the homepage.'
        })
    return alerts


# ── HTMX Endpoints ─────────────────────────────────────────────
@staff_member_required
def htmx_mark_message_read(request, pk):
    """Mark a contact message as read and return updated status badge."""
    if request.method == 'POST' and request.htmx:
        msg = get_object_or_404(ContactMessage, pk=pk)
        msg.status = 'read'
        msg.save()
        return HttpResponse(
            f'<span style="background:#e0e7ff;color:#3730a3;padding:2px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;">READ</span>'
        )
    return HttpResponse(status=405)


@staff_member_required
def htmx_mark_message_replied(request, pk):
    """Mark a message as replied."""
    if request.method == 'POST' and request.htmx:
        msg = get_object_or_404(ContactMessage, pk=pk)
        msg.status = 'replied'
        msg.save()
        return HttpResponse(
            f'<span style="background:#d1fae5;color:#065f46;padding:2px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;">REPLIED</span>'
        )
    return HttpResponse(status=405)


@staff_member_required
def htmx_toggle_featured(request, model, pk):
    """Toggle is_featured on product/service/project."""
    if request.method == 'POST' and request.htmx:
        MODEL_MAP = {'product': Product, 'service': Service, 'project': Project}
        Model = MODEL_MAP.get(model)
        if not Model:
            return HttpResponse(status=400)
        obj = get_object_or_404(Model, pk=pk)
        obj.is_featured = not obj.is_featured
        obj.save()
        label = 'Featured ★' if obj.is_featured else 'Not featured'
        colour = '#057a55' if obj.is_featured else '#6b7280'
        return HttpResponse(
            f'<span style="color:{colour};font-weight:600;font-size:0.82rem;">{label}</span>'
        )
    return HttpResponse(status=405)


# ── Dashboard data APIs (for HTMX auto‑refresh) ────────────────
# core/dashboard.py  (place at the bottom of the file)

@staff_member_required
def dashboard_stats_api(request):
    """HTMX – returns the full stat‑card grid (11 cards) as HTML."""
    now = timezone.now()
    today = now.date()
    week_ago = now - timedelta(days=7)

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
    return render(request, 'admin/snippets/dashboard_stats_grid.html', {'dash_stats': stats})


@staff_member_required
def dashboard_messages_api(request):
    """HTMX – returns the recent messages table as HTML."""
    recent = ContactMessage.objects.order_by('-created_at')[:8]
    return render(request, 'admin/snippets/dashboard_messages.html', {'recent_messages': recent})


@staff_member_required
def dashboard_visitors_api(request):
    """HTMX – returns the recent visitors table as HTML."""
    recent_visitors = Visitor.objects.order_by('-created_at')[:15]
    return render(request, 'admin/snippets/visitors_table.html', {'recent_visitors': recent_visitors})
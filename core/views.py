from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from products.models import Product
from .models import Testimonial, WhatsAppClick, SiteSettings, GroupConfig
from contacts.models import ContactMessage


# ── Shared contact base ───────────────────────────────────────────────
class GenericContactView(View):
    template_name = 'contacts/contact.html'
    source = 'general'
    redirect_url_name = 'contact'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name    = request.POST.get('name', '').strip()
        phone   = request.POST.get('phone', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        msg     = request.POST.get('message', '').strip()
        source  = request.POST.get('source', self.source)
        if name and phone and msg:
            ContactMessage.objects.create(
                name=name, phone=phone, email=email,
                subject=subject, message=msg, source=source
            )
            messages.success(request, f'Thank you {name}! We will contact you shortly.')
            return redirect(request.path)
        messages.error(request, 'Please fill in name, phone and message.')
        return render(request, self.template_name)


# ── Group landing ─────────────────────────────────────────────────────
class HomeView(TemplateView):
    template_name = 'group/landing.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['gcfg'] = GroupConfig.get()
        ctx['testimonials_list'] = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:6]
        ctx['industry_cards'] = ctx['gcfg'].get_industry_cards()
        return ctx


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['settings_obj'] = SiteSettings.get_settings()
        return ctx


# ── WhatsApp click tracker ────────────────────────────────────────────
@csrf_exempt
@require_POST
def log_whatsapp_click(request):
    try:
        page_path  = request.POST.get('page_path', '/')
        product_id = request.POST.get('product_id')
        ip = (request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
              or request.META.get('REMOTE_ADDR'))
        product = Product.objects.filter(pk=product_id).first() if product_id else None
        WhatsAppClick.objects.create(page_path=page_path, product=product, ip_address=ip)
        return JsonResponse({'status': 'ok'})
    except Exception:
        return JsonResponse({'status': 'error'}, status=500)

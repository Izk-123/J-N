from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from .models import ContactMessage


class ContactView(View):
    template_name = 'contacts/contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        msg = request.POST.get('message', '').strip()

        if name and phone and msg:
            ContactMessage.objects.create(
                name=name, phone=phone, email=email,
                subject=subject, message=msg
            )

            try:
                admin_email = getattr(settings, 'ADMIN_EMAIL', None)
                if admin_email:
                    send_mail(
                        subject=f'[J&N Website] New Enquiry from {name}',
                        message=(
                            f'You have a new enquiry from your website.\n\n'
                            f'Name:    {name}\n'
                            f'Phone:   {phone}\n'
                            f'Email:   {email or "Not provided"}\n'
                            f'Subject: {subject or "General enquiry"}\n\n'
                            f'Message:\n{msg}\n\n'
                            f'---\nReply directly to this person or call them on {phone}.'
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[admin_email],
                        fail_silently=True,
                    )
            except Exception:
                pass

            messages.success(
                request,
                f'Thank you, {name}! Your message has been sent. We will contact you soon.'
            )
            return redirect('contact')

        messages.error(request, 'Please fill in your name, phone number, and message.')
        return render(request, self.template_name)
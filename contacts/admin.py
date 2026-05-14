from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ('name', 'display_phone', 'display_subject', 'source', 'display_status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('name', 'phone', 'email', 'subject', 'message', 'created_at', 'display_whatsapp_link')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('📨 From', {'fields': ('name', 'phone', 'email', 'display_whatsapp_link', 'created_at')}),
        ('💬 Message', {'fields': ('subject', 'message')}),
        ('📋 Status', {'fields': ('status', 'source')}),
    )

    @display(description='Phone')
    def display_phone(self, obj):
        return format_html('<a href="tel:{}" style="color:inherit;">{}</a>', obj.phone, obj.phone)

    @display(description='Subject')
    def display_subject(self, obj):
        return obj.subject or format_html('<em style="color:#aaa;">General enquiry</em>')

    @display(description='Status')
    def display_status(self, obj):
        colours = {'new': '#92400e|#fef3c7', 'read': '#3730a3|#e0e7ff', 'replied': '#065f46|#d1fae5'}
        fg, bg = colours.get(obj.status, '#333|#eee').split('|')
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;">{}</span>',
            bg, fg, obj.get_status_display().upper()
        )

    @display(description='WhatsApp')
    def display_whatsapp_link(self, obj):
        number = obj.phone.replace(' ', '').replace('+', '')
        return format_html(
            '<a href="https://wa.me/{}" target="_blank" style="background:#25D366;color:white;padding:4px 14px;border-radius:4px;text-decoration:none;font-size:0.82rem;">💬 Reply on WhatsApp</a>',
            number
        )

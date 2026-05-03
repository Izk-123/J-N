from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'subject', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status',)
    readonly_fields = ('name', 'phone', 'email', 'subject', 'message', 'created_at')

from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget
from django import forms

from .models import SiteSettings, Testimonial, Visitor, WhatsAppClick


class SiteSettingsForm(forms.ModelForm):
    about_text = forms.CharField(widget=WysiwygWidget(), required=False)
    hero_subheading = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    class Meta:
        model = SiteSettings
        fields = '__all__'


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    form = SiteSettingsForm
    compressed_fields = True
    warn_unsaved_form = True
    fieldsets = (
        ('🏢 Company Identity', {'fields': ('company_name', 'tagline')}),
        ('📞 Contact Details', {'fields': ('phone', 'email', 'address', 'whatsapp_number')}),
        ('📱 Social Media', {'classes': ('collapse',), 'fields': ('facebook_url', 'instagram_url', 'twitter_url')}),
        ('🏠 Homepage Content', {'fields': ('hero_heading', 'hero_subheading', 'about_text')}),
        ('📊 Statistics', {'fields': ('years_experience', 'projects_completed', 'happy_clients')}),
    )
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('name', 'role', 'display_rating', 'is_active', 'created_at')
    list_filter = ('is_active', 'rating')
    list_editable = ('is_active',)
    search_fields = ('name', 'role', 'message')
    fieldsets = (
        ('Client Info', {'fields': ('name', 'role')}),
        ('Review', {'fields': ('message', 'rating', 'is_active')}),
    )

    @display(description='Rating', ordering='rating')
    def display_rating(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        color = '#F5A623' if obj.rating >= 4 else '#aaa'
        return format_html('<span style="color:{};font-size:1rem;">{}</span>', color, stars)


# ─── NEW: Visitor & WhatsApp Click Admins ──────────────────────────────

@admin.register(Visitor)
class VisitorAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ('path', 'ip_address', 'device_type', 'browser', 'created_at')
    list_filter = ('device_type', 'browser', 'created_at')
    search_fields = ('path', 'ip_address', 'user_agent')
    date_hierarchy = 'created_at'
    readonly_fields = ('path', 'ip_address', 'user_agent', 'device_type', 'browser', 'referrer', 'created_at')
    fieldsets = (
        ('Page Visit', {'fields': ('path', 'referrer')}),
        ('Visitor Info', {'fields': ('ip_address', 'user_agent')}),
        ('Detected', {'fields': ('device_type', 'browser')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(WhatsAppClick)
class WhatsAppClickAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ('page_path', 'product', 'contact_message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('page_path',)
    date_hierarchy = 'created_at'
    readonly_fields = ('page_path', 'product', 'contact_message', 'ip_address', 'created_at')
    fieldsets = (
        ('Click Info', {'fields': ('page_path', 'ip_address')}),
        ('Linked To', {'fields': ('product', 'contact_message')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
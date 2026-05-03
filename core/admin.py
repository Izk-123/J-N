from django.contrib import admin
from .models import SiteSettings, Testimonial


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Company Info', {'fields': ('company_name', 'tagline', 'phone', 'email', 'address', 'whatsapp_number')}),
        ('Social Media', {'fields': ('facebook_url', 'instagram_url', 'twitter_url')}),
        ('Homepage Content', {'fields': ('hero_heading', 'hero_subheading', 'about_text')}),
        ('Statistics', {'fields': ('years_experience', 'projects_completed', 'happy_clients')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'rating')

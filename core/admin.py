from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget
from django import forms

from .models import SiteSettings, Testimonial, Visitor, WhatsAppClick, GroupConfig


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
        # Inside SiteSettingsAdmin.fieldsets, update the Homepage Content tuple:
        ('🏠 Homepage Content', {
            'fields': (
                'hero_badge_text',
                'hero_heading_prefix',
                'hero_heading_highlight',
                'hero_heading_suffix',
                'hero_subheading',
                'hero_image',
                'about_text',
            )
        }),
        ('🏠 About Page Content', {
            'classes': ('collapse',),
            'fields': (
                'about_image',
                'about_mission',
                'about_vision',
                ('about_value1_title', 'about_value1_desc', 'about_value1_icon'),
                ('about_value2_title', 'about_value2_desc', 'about_value2_icon'),
                ('about_value3_title', 'about_value3_desc', 'about_value3_icon'),
            )
        }),
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
    list_display = ('name', 'role', 'display_rating', 'source', 'is_active', 'created_at')
    list_filter = ('is_active', 'rating', 'source')
    list_editable = ('is_active',)
    search_fields = ('name', 'role', 'message', 'source')
    fieldsets = (
        ('Client Info', {'fields': ('name', 'role')}),
        ('Review', {'fields': ('message', 'rating', 'is_active', 'source')}),
    )
    
        # inside TestimonialAdmin
    @display(description='Source', ordering='source')
    def display_source(self, obj):
        return obj.get_source_display()

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


class GroupConfigForm(forms.ModelForm):
    story_text = forms.CharField(widget=WysiwygWidget(), required=False)
    hero_title = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    
    class Meta:
        model = GroupConfig
        fields = '__all__'

@admin.register(GroupConfig)
class GroupConfigAdmin(ModelAdmin):
    form = GroupConfigForm
    compressed_fields = True
    warn_unsaved_form = True
    
    fieldsets = (
        ('🏢 Group Brand', {
            'fields': ('group_name', 'tagline', 'sub_tagline', 'logo', 'hero_image', 'hero_video_url')
        }),
        ('📝 Hero Content', {
            'fields': ('hero_title', 'hero_subheading'),
            'description': 'Use HTML <br> and <span class="orange-text"> for styling.'
        }),
        ('🔴 Building Products Button', {
            'fields': ('btn1_label', 'btn1_url', 'btn1_icon', 'card1_description', 'card1_bg_image')
        }),
        ('🔵 Construction Button', {
            'fields': ('btn2_label', 'btn2_url', 'btn2_icon', 'card2_description', 'card2_bg_image')
        }),
        ('🟡 Mining Button', {
            'fields': ('btn3_label', 'btn3_url', 'btn3_icon', 'card3_description', 'card3_bg_image')
        }),
        ('🌲 Timber Button', {
            'fields': ('btn4_label', 'btn4_url', 'btn4_icon', 'card4_description', 'card4_bg_image')
        }),
        ('💎 Core Values (4 items)', {
            'fields': (
                ('value1_title', 'value1_desc', 'value1_icon'),
                ('value2_title', 'value2_desc', 'value2_icon'),
                ('value3_title', 'value3_desc', 'value3_icon'),
                ('value4_title', 'value4_desc', 'value4_icon'),
            )
        }),
        ('📖 Group Story', {
            'fields': ('story_heading', 'story_text')
        }),
        ('📊 Statistics Counters', {
            'fields': (
                ('stat1_number', 'stat1_label'),
                ('stat2_number', 'stat2_label'),
                ('stat3_number', 'stat3_label'),
            )
        }),
        ('🎯 Parallax Divider', {
            'fields': ('divider_title', 'divider_subtitle')
        }),
        ('📞 Contact Details', {
            'fields': ('phone', 'email', 'address', 'whatsapp')
        }),
        ('📱 Social Media', {
            'classes': ('collapse',),
            'fields': ('facebook', 'linkedin')
        }),
        ('📄 Footer', {
            'fields': ('footer_copyright',)
        }),
    )
    
    def has_add_permission(self, request):
        return not GroupConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
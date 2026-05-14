from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget
from django import forms

from .models import (
    ConstructionConfig, ConstructionFact, ConstructionService,
    ConstructionProject, ConstructionProjectImage, TeamMember
)


class ConstructionConfigForm(forms.ModelForm):
    about_text  = forms.CharField(widget=WysiwygWidget(), required=False)
    class Meta:
        model = ConstructionConfig
        fields = '__all__'


@admin.register(ConstructionConfig)
class ConstructionConfigAdmin(ModelAdmin):
    form = ConstructionConfigForm
    compressed_fields = True
    warn_unsaved_form = True
    fieldsets = (
        ('🏗️ Brand', {
            'fields': ('company_name', 'tagline', 'logo', 'favicon')
        }),
        ('🎨 Colours', {
            'fields': ('primary_color', 'accent_color'),
            'description': 'Hex colour codes used throughout the construction sub-site'
        }),
        ('📞 Contact', {
            'fields': ('phone', 'email', 'address', 'whatsapp')
        }),
        ('📱 Social Media', {
            'classes': ('collapse',),
            'fields': ('facebook', 'instagram', 'linkedin')
        }),
        ('🖼️ Hero Section', {
            'fields': ('hero_heading', 'hero_sub', 'hero_image', 'hero_video_url')
        }),
        ('📄 Page Header Background', {    # <-- new group
            'fields': ('page_header_image',),
            'description': 'Image used for inner page headers (About, Services, etc.)'
        }),
        ('📖 About Section', {
            'fields': ('about_text', 'about_image', 'years_exp', 'projects_done', 'clients')
        }),
        ('🔍 SEO', {
            'classes': ('collapse',),
            'fields': ('meta_description',)
        }),
    )

    def has_add_permission(self, request):
        return not ConstructionConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ConstructionService)
class ConstructionServiceAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('display_icon', 'title', 'is_featured', 'order')
    list_display_links = ('display_icon', 'title')
    list_editable = ('is_featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

    @display(description='Icon')
    def display_icon(self, obj):
        return format_html('<i class="{}" style="font-size:1.3rem;color:#1A56DB;"></i>', obj.icon)


class ConstructionProjectImageInline(TabularInline):
    model = ConstructionProjectImage
    extra = 3
    fields = ('image', 'caption', 'order')


@admin.register(ConstructionProject)
class ConstructionProjectAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('display_cover', 'title', 'location', 'completion_date', 'is_featured')
    list_display_links = ('display_cover', 'title')
    list_editable = ('is_featured',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'location')
    date_hierarchy = 'completion_date'
    inlines = [ConstructionProjectImageInline]

    @display(description='Cover')
    def display_cover(self, obj):
        if obj.cover_image and obj.cover_image.name:
            return format_html('<img src="{}" style="height:40px;width:60px;object-fit:cover;border-radius:4px;">', obj.cover_image.url)
        return '—'


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ('display_photo', 'name', 'role', 'is_active', 'order')
    list_display_links = ('display_photo', 'name')
    list_editable = ('is_active', 'order')

    @display(description='Photo')
    def display_photo(self, obj):
        if obj.photo and obj.photo.name:
            return format_html('<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:50%;">', obj.photo.url)
        return '👤'


@admin.register(ConstructionFact)
class ConstructionFactAdmin(ModelAdmin):
    list_display = ('number', 'title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fields = ('number', 'title', 'description', 'image', 'link_url', 'link_text', 'order', 'is_active')
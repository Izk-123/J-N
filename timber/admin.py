from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget
from django import forms

from .models import TimberSettings, TimberCategory, TimberProduct, TimberProject


class TimberSettingsForm(forms.ModelForm):
    about_text = forms.CharField(widget=WysiwygWidget(), required=False)
    class Meta:
        model = TimberSettings
        fields = '__all__'


@admin.register(TimberSettings)
class TimberSettingsAdmin(ModelAdmin):
    form = TimberSettingsForm
    compressed_fields = True
    warn_unsaved_form = True
    fieldsets = (
        ('🌲 Brand',    {'fields': ('company_name', 'tagline', 'logo', 'favicon')}),
        ('🎨 Colours',  {'fields': ('primary_color', 'accent_color')}),
        ('📞 Contact',  {'fields': ('phone', 'email', 'address', 'whatsapp')}),
        ('📱 Social',   {'classes': ('collapse',), 'fields': ('facebook', 'linkedin')}),
        ('🖼️ Hero',     {'fields': ('hero_heading', 'hero_sub', 'hero_image')}),
        ('📖 About',    {'fields': ('about_text', 'about_image', 'years_exp', 'trees_processed', 'clients')}),
        ('🔍 SEO',      {'classes': ('collapse',), 'fields': ('meta_description',)}),
    )
    def has_add_permission(self, request):
        return not TimberSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TimberCategory)
class TimberCategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TimberProduct)
class TimberProductAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('display_image', 'name', 'category', 'is_featured', 'is_active')
    list_display_links = ('display_image', 'name')
    list_editable = ('is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    @display(description='Image')
    def display_image(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="height:40px;width:50px;object-fit:cover;border-radius:4px;">', obj.image.url)
        return '🌲'


@admin.register(TimberProject)
class TimberProjectAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ('display_cover', 'title', 'location', 'is_featured')
    list_display_links = ('display_cover', 'title')
    list_editable = ('is_featured',)
    prepopulated_fields = {'slug': ('title',)}

    @display(description='Cover')
    def display_cover(self, obj):
        if obj.cover_image and obj.cover_image.name:
            return format_html('<img src="{}" style="height:38px;width:56px;object-fit:cover;border-radius:4px;">', obj.cover_image.url)
        return '🌲'

from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget
from django import forms

from .models import Service


class ServiceForm(forms.ModelForm):
    description = forms.CharField(widget=WysiwygWidget(), required=True)
    short_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    class Meta:
        model = Service
        fields = '__all__'


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    form = ServiceForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('display_image', 'title', 'display_icon', 'is_featured', 'is_active', 'order')
    list_display_links = ('display_image', 'title')
    list_editable = ('is_featured', 'is_active', 'order')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    readonly_fields = ('display_image_preview',)
    fieldsets = (
        ('Service Info', {'fields': ('title', 'slug', 'icon', 'short_description', 'order', 'is_featured', 'is_active')}),
        ('Image', {'fields': ('image', 'display_image_preview')}),
        ('Full Description', {'fields': ('description',)}),
    )

    @display(description='Image')
    def display_image(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="height:40px;width:50px;object-fit:cover;border-radius:4px;">', obj.image.url)
        return format_html('<span style="color:#ccc;font-size:0.75rem;">No image</span>')

    @display(description='Icon')
    def display_icon(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size:1.2rem;color:#D62828;"></i> <code style="font-size:0.7rem;">{}</code>', obj.icon, obj.icon)
        return '—'

    @display(description='Preview')
    def display_image_preview(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="max-height:180px;border-radius:8px;">', obj.image.url)
        return 'No image uploaded yet.'

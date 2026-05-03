from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ('display_image', 'title', 'category', 'is_active', 'created_at')
    list_display_links = ('display_image', 'title')
    list_editable = ('is_active',)
    list_filter = ('category', 'is_active')
    search_fields = ('title',)
    fieldsets = (
        ('Image Details', {'fields': ('image', 'title', 'category', 'is_active')}),
    )

    @display(description='Preview')
    def display_image(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="height:50px;width:70px;object-fit:cover;border-radius:4px;">', obj.image.url)
        return format_html('<span style="color:#ccc;font-size:0.75rem;">No image</span>')

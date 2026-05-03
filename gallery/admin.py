from django.contrib import admin
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('category', 'is_active')

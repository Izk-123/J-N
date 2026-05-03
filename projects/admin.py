from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget
from django import forms

from .models import Project, ProjectImage


class ProjectImageInline(TabularInline):
    model = ProjectImage
    extra = 3
    fields = ('image', 'caption', 'order')
    readonly_fields = ('display_thumb',)

    @display(description='Preview')
    def display_thumb(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;">', obj.image.url)
        return '—'


class ProjectForm(forms.ModelForm):
    description = forms.CharField(widget=WysiwygWidget(), required=True)
    class Meta:
        model = Project
        fields = '__all__'


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    form = ProjectForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('display_cover', 'title', 'location', 'completion_date', 'is_featured', 'is_active')
    list_display_links = ('display_cover', 'title')
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'location', 'description')
    date_hierarchy = 'completion_date'
    readonly_fields = ('display_cover_preview',)
    inlines = [ProjectImageInline]
    fieldsets = (
        ('Project Info', {'fields': ('title', 'slug', 'location', 'client_name', 'completion_date', 'is_featured', 'is_active')}),
        ('Cover Image', {'fields': ('cover_image', 'display_cover_preview')}),
        ('Description', {'fields': ('description',)}),
    )

    @display(description='Cover')
    def display_cover(self, obj):
        if obj.cover_image and obj.cover_image.name:
            return format_html('<img src="{}" style="height:40px;width:60px;object-fit:cover;border-radius:4px;">', obj.cover_image.url)
        return format_html('<span style="color:#ccc;font-size:0.75rem;">No image</span>')

    @display(description='Cover Preview')
    def display_cover_preview(self, obj):
        if obj.cover_image and obj.cover_image.name:
            return format_html('<img src="{}" style="max-height:180px;border-radius:8px;">', obj.cover_image.url)
        return 'No image uploaded yet.'

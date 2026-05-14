from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget
from django import forms

from .models import Category, Product, BuildingSettings


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=WysiwygWidget(), required=True)
    specifications = forms.CharField(widget=WysiwygWidget(), required=False)
    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    form = ProductForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('display_image', 'name', 'category', 'display_price', 'is_featured', 'is_active', 'created_at')
    list_display_links = ('display_image', 'name')
    list_filter = ('category', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('display_image_preview',)
    fieldsets = (
        ('Product Info', {'fields': ('name', 'slug', 'category', 'is_featured', 'is_active')}),
        ('Image', {'fields': ('image', 'display_image_preview')}),
        ('Content', {'fields': ('description', 'specifications')}),
        ('Pricing', {'fields': ('price',)}),
    )

    @display(description='Image')
    def display_image(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="height:40px;width:50px;object-fit:cover;border-radius:4px;">', obj.image.url)
        return format_html('<span style="color:#ccc;font-size:0.75rem;">No image</span>')

    @display(description='Preview')
    def display_image_preview(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;">', obj.image.url)
        return 'No image uploaded yet.'

    @display(description='Price', ordering='price')
    def display_price(self, obj):
        if obj.price:
            return format_html('<span style="color:#057a55;font-weight:600;">MK {:,.0f}</span>', obj.price)
        return format_html('<span style="color:#aaa;font-size:0.8rem;">—</span>')

@admin.register(BuildingSettings)
class BuildingSettingsAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    fieldsets = (
        ('🔴 Brand',    {'fields': ('company_name', 'tagline', 'logo')}),
        ('🎨 Colours',  {'fields': ('primary_color', 'secondary_color')}),
        ('📞 Contact',  {'fields': ('phone', 'email', 'address', 'whatsapp')}),
        ('📱 Social',   {'classes': ('collapse',), 'fields': ('facebook', 'instagram')}),
        ('🖼️ Hero',     {'fields': ('hero_heading', 'hero_subheading', 'hero_badge_text', 'hero_image')}),
        ('📖 About',    {'fields': ('about_text',)}),
        ('🔍 SEO',      {'classes': ('collapse',), 'fields': ('meta_description',)}),
    )
    def has_add_permission(self, request):
        return not BuildingSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False

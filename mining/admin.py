from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget
from django import forms

from .models import (
    MiningConfig, MineralCategory, MineralProduct,
    MiningEquipment, MiningOperation
)


class MiningConfigForm(forms.ModelForm):
    about_text = forms.CharField(widget=WysiwygWidget(), required=False)
    compliance_text = forms.CharField(widget=WysiwygWidget(), required=False)
    class Meta:
        model = MiningConfig
        fields = '__all__'


@admin.register(MiningConfig)
class MiningConfigAdmin(ModelAdmin):
    form = MiningConfigForm
    compressed_fields = True
    warn_unsaved_form = True
    fieldsets = (
        ('⛏️ Brand', {'fields': ('company_name', 'tagline', 'logo', 'favicon')}),
        ('🎨 Colours', {'fields': ('primary_color', 'accent_color')}),
        ('📞 Contact', {'fields': ('phone', 'email', 'address', 'whatsapp')}),
        ('📱 Social', {'classes': ('collapse',), 'fields': ('facebook', 'linkedin')}),
        ('🖼️ Hero', {'fields': ('hero_heading', 'hero_sub', 'hero_image')}),
        ('📖 About', {'fields': ('about_text', 'about_image', 'years_exp', 'tonnes_mined', 'sites')}),
        ('📋 Compliance', {'fields': ('compliance_text',)}),
        ('🔍 SEO', {'classes': ('collapse',), 'fields': ('meta_description',)}),
    )

    def has_add_permission(self, request):
        return not MiningConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MineralCategory)
class MineralCategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MineralProduct)
class MineralProductAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('display_image', 'name', 'category', 'is_featured', 'is_active')
    list_display_links = ('display_image', 'name')
    list_editable = ('is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    @display(description='Image')
    def display_image(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="height:40px;width:50px;object-fit:cover;border-radius:4px;">', obj.image.url)
        return '⛏️'


@admin.register(MiningEquipment)
class MiningEquipmentAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MiningOperation)
class MiningOperationAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ('display_image', 'name', 'location', 'is_active')
    list_display_links = ('display_image', 'name')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('minerals',)

    @display(description='Image')
    def display_image(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="height:40px;width:50px;object-fit:cover;border-radius:4px;">', obj.image.url)
        return '🏔️'

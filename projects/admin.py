from django.contrib import admin
from .models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'completion_date', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]

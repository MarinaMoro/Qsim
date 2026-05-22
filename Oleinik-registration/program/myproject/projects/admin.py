from django.contrib import admin
from .models import Project, ProjectFile

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'project_type', 'created_at', 'updated_at')
    list_filter = ('project_type', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'

@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'project', 'uploaded_at', 'file_size')
    list_filter = ('uploaded_at',)
    search_fields = ('filename',)
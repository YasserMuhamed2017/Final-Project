from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'total_target', 'current_amount', 'start_time', 'end_time')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'project__title')
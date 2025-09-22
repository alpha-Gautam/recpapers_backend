from django.contrib import admin
from recpaper_app.models import  Project, Project_log, Comment, Files

# Register your models here.

# admin.site.register(Project)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("user", "mentor", 'title', 'created_at','semester','verified',)
    search_fields = ('title', 'user__username', 'mentor__username')
    # list_filter = ("user")
    
    
    
    
admin.site.register(Project_log)
admin.site.register(Comment)
admin.site.register(Files)

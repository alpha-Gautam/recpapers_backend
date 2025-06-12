from django.contrib import admin
from recpaper_app.models import User,Mentor, Project, Project_log, Comment, Files,Faculty,Student

# Register your models here.

# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','mobile', 'college', 'department', 'role', 'active', 'verified_by_admin','created_at')
    search_fields = ('username', 'email', 'mobile', 'college', 'department')
    list_filter = ('role', 'active', 'verified_by_admin')


# admin.site.register(Project)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("user", "mentor", 'title', 'created_at','semester','verified',)
    search_fields = ('title', 'user__username', 'mentor__username')
    # list_filter = ("user")
    
    
    
# admin.site.register(Mentor)
@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile', 'college')
    search_fields = ('username', 'email', 'mobile', 'college')

# @class Project_logAdmin(admin.ModelAdmin):
#     list_display = ('project', 'log_date', 'log_description')
#     search_fields = ('project__title', 'log_description')
    
    
admin.site.register(Project_log)
admin.site.register(Comment)
admin.site.register(Files)
admin.site.register(Faculty)
admin.site.register(Student)
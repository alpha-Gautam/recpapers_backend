from django.contrib import admin
from recpaper_app.models import User, Project, Platform, Keyword, Project_log, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Platform)
admin.site.register(Keyword)
admin.site.register(Project_log)
admin.site.register(Comment)
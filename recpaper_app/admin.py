from django.contrib import admin
from recpaper_app.models import User,Mentor, Project, Project_log, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Mentor)
admin.site.register(Project_log)
admin.site.register(Comment)
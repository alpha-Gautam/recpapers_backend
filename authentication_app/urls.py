from django.urls import path, include

from .views import StudentLogin, MentorLogin

urlpatterns = [
    path('student/', StudentLogin.as_view(), name='studentLogin'),
    path('mentor/', MentorLogin.as_view(), name='mentorLogin'),
]

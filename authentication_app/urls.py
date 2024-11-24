from django.urls import path, include

from .views import StudentLogin, MentorLogin,StudentListView,MentorListView

urlpatterns = [
    path('student/list/', StudentListView.as_view(), name='StudentListView'),
    path('mentor/list/', MentorListView.as_view(), name='MentorListView'),
    path('student/login/', StudentLogin.as_view(), name='studentLogin'),
    path('mentor/login', MentorLogin.as_view(), name='mentorLogin'),
]

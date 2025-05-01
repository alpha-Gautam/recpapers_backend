from django.urls import path, include

from recpaper_app.api.views import project_view, user_view, project_detail, user_login, user_ragister
from recpaper_app.api.views import porject_log, Project_comments,mentor_view,project_create

urlpatterns = [
   
    path('login/', user_login.as_view(), name='user_login'),
    path('ragister/', user_ragister.as_view(), name='user_ragister'),
    
    
    path('user/', user_view.as_view(), name='user_list'),
    path('mentor/', mentor_view.as_view(), name='mentor_list'),
    # path('platform/', platform_view.as_view(), name='platform_list'),
    
    
    path('project/', project_view.as_view(), name='paper_list'),
    path('project/<str:pk>/', project_detail.as_view(), name='project_detail'),
    path('project_create/', project_create.as_view(), name='project_create'),
    
    
    path('log/<str:pk>/', porject_log.as_view(), name='Project_Log'),
    path('commnets/', Project_comments.as_view(), name='Project_comments'),
    
    
    
]

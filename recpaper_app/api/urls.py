from django.urls import path, include

from recpaper_app.api.views import project_view, user_view,keyword_view, project_detail, user_login, user_ragister
from recpaper_app.api.views import porject_log, Project_comments

urlpatterns = [
   
    path('login/', user_login.as_view(), name='user_login'),
    path('user/', user_view.as_view(), name='user_list'),
    path('ragister/', user_ragister.as_view(), name='user_ragister'),
    
    
    path('project/', project_view.as_view(), name='paper_list'),
    path('project/<str:pk>/', project_detail.as_view(), name='project_detail'),
    path('key/', keyword_view.as_view(), name='paper_list'),
    
    
    path('log/<str:pk>/', porject_log.as_view(), name='Project_Log'),
    path('commnets/', Project_comments.as_view(), name='Project_comments'),
    
    
    
]

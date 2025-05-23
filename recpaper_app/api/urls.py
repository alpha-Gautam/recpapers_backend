from django.urls import path, include

from recpaper_app.api.views import project_view, user_view, project_detail, user_login, user_ragister, User_project_view,verify_project
from recpaper_app.api.views import porject_log, Project_comments,mentor_view,project_create, file_upload


# from django.conf import settings
# from django.conf.urls.static import static
 


urlpatterns = [
   
    path('login/', user_login.as_view(), name='user_login'),
    path('ragister/', user_ragister.as_view(), name='user_ragister'),
    
    
    path('user/', user_view.as_view(), name='user_list'),
    path('mentor/', mentor_view.as_view(), name='mentor_list'),
    # path('platform/', platform_view.as_view(), name='platform_list'),
    
    
    path('project/', project_view.as_view(), name='paper_list'),
    path('user_project/', User_project_view.as_view(), name='paper_list'),
    path('project/<str:pk>/', project_detail.as_view(), name='project_detail'),
    path('project_create/', project_create.as_view(), name='project_create'),
    path('verify_project/',verify_project.as_view(), name='verify_project'),
    
    
    path('log/<str:pk>/', porject_log.as_view(), name='Project_Log'),
    path('log/', porject_log.as_view(), name='Project_Log'),
    
    path('commnets/', Project_comments.as_view(), name='Project_comments'),
    
    path('file/<str:pk>', file_upload.as_view(), name="file_operations")
    
]

# if settings.DEBUG:
#     urlpatterns+=static(settings.MEDIA_URL, documetn_root= settings.MEDIA_ROOT)


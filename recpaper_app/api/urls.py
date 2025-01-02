from django.urls import path, include

from recpaper_app.api.views import project_view, user_view,keyword_view, project_detail

urlpatterns = [
    # path('user/', UserListView.as_view(), name='user_list'),
    # path('project/', ProjectListView.as_view(), name='paper_list'),
    path('user/', user_view, name='paper_list'),
    path('project/', project_view, name='paper_list'),
    path('project/<str:pk>/', project_detail, name='project_detail'),
    path('key/', keyword_view, name='paper_list'),
    # path('project/<int:pk>/', ProjectDetail.as_view(), name='Project_detail'),
    # path('login/', user_login, name='user_detail'),
    # path('paper/', paper_list, name='paper_list'),
    
    # path('paper/<int:pk>/', paper_detail, name='paper_detail'),
]

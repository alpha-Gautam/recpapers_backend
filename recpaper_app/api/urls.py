from django.urls import path, include

from recpaper_app.api.views import UserListView, PaperListView, user_login, paper_list, paper_detail

urlpatterns = [
    path('list/', UserListView.as_view(), name='user_list'),
    path('paper/list/', PaperListView.as_view(), name='paper_list'),
    # path('<int:pk>/', user_detail, name='user_detail'),
    path('login/', user_login, name='user_detail'),
    # path('paper/', paper_list, name='paper_list'),
    
    # path('paper/<int:pk>/', paper_detail, name='paper_detail'),
]

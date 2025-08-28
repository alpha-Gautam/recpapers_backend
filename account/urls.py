

# Routers provide an easy way of automatically determining the URL conf.
from django.contrib import admin
from django.urls import include, path
from .views import UserRegisterView, UserLoginView


from django.http import HttpResponse

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),

    # path('api/', include('recpaper_app.api.urls')),
    # path('chatApi/', include('chat_app.api.urls')),
   
]


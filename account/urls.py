

# Routers provide an easy way of automatically determining the URL conf.
from django.contrib import admin
from django.urls import include, path
from .views import UserRegisterView, UserLoginView,GetCookies


from django.http import HttpResponse

urlpatterns = [
    path('get-cookies/', GetCookies.as_view(), name='get-cookies'),
    
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    

   \
   
]

